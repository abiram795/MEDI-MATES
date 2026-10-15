from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os
import uuid
from backend.utils.supabase_client import get_current_user, CurrentUser, supabase_admin, require_role

router = APIRouter(prefix="/api/documents", tags=["Documents"])

BUCKET_NAME = "medical-documents"

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(require_role("patient"))
):
    try:
        # 1. Upload file to Supabase Storage
        file_ext = file.filename.split('.')[-1]
        unique_filename = f"{current_user.id}/{uuid.uuid4()}.{file_ext}"

        file_content = await file.read()

        res = supabase_admin.storage.from_(BUCKET_NAME).upload(
            file=file_content,
            path=unique_filename,
            file_options={"content-type": file.content_type}
        )

        # 2. Insert record into medical_documents table
        doc_data = {
            "patient_id": current_user.id,
            "file_path": unique_filename,
            "file_name": file.filename,
            "file_size": len(file_content),
            "mime_type": file.content_type
        }

        db_res = supabase_admin.table('medical_documents').insert(doc_data).execute()

        return db_res.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/")
def get_documents(current_user: CurrentUser = Depends(require_role("patient"))):
    res = supabase_admin.table('medical_documents').select('*').eq('patient_id', current_user.id).order('uploaded_at', desc=True).execute()

    # Generate signed URLs for secure viewing
    docs = res.data
    for doc in docs:
        signed_url_res = supabase_admin.storage.from_(BUCKET_NAME).create_signed_url(doc['file_path'], 3600) # 1 hour
        doc['download_url'] = signed_url_res['signedURL']

    return docs

@router.delete("/{doc_id}")
def delete_document(doc_id: str, current_user: CurrentUser = Depends(require_role("patient"))):
    # Verify ownership
    doc_res = supabase_admin.table('medical_documents').select('file_path').eq('id', doc_id).eq('patient_id', current_user.id).execute()
    if not doc_res.data:
        raise HTTPException(status_code=404, detail="Document not found or unauthorized")

    file_path = doc_res.data[0]['file_path']

    # Delete from storage
    supabase_admin.storage.from_(BUCKET_NAME).remove([file_path])

    # Delete from DB
    supabase_admin.table('medical_documents').delete().eq('id', doc_id).execute()

    return {"message": "Document deleted successfully"}
