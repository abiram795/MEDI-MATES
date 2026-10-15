from fastapi import APIRouter, Depends, HTTPException
import fitz # PyMuPDF
import os
import tempfile
from backend.utils.supabase_client import get_current_user, CurrentUser, supabase_admin, require_role
from backend.services.ai_service import analyze_medical_text

router = APIRouter(prefix="/api/reports", tags=["Reports"])
BUCKET_NAME = "medical-documents"

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

@router.post("/{doc_id}/analyze")
def analyze_report(doc_id: str, current_user: CurrentUser = Depends(require_role("patient"))):
    # Verify ownership
    doc_res = supabase_admin.table('medical_documents').select('*').eq('id', doc_id).eq('patient_id', current_user.id).execute()
    if not doc_res.data:
        raise HTTPException(status_code=404, detail="Document not found")

    doc = doc_res.data[0]

    # Download file temporarily
    file_bytes = supabase_admin.storage.from_(BUCKET_NAME).download(doc['file_path'])

    extracted_text = ""
    if doc['file_name'].lower().endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        extracted_text = extract_text_from_pdf(tmp_path)
        os.unlink(tmp_path)
    else:
        extracted_text = "Image OCR not fully implemented in this demo. Assume some extracted text."

    analysis_result = analyze_medical_text(extracted_text)
    if not analysis_result:
        raise HTTPException(status_code=500, detail="AI Analysis failed")

    # Save to ai_analysis
    ai_data = {
        "document_id": doc_id,
        "analysis_result": analysis_result
    }

    res = supabase_admin.table('ai_analysis').insert(ai_data).execute()
    return res.data[0]

@router.get("/{doc_id}/analysis")
def get_analysis(doc_id: str, current_user: CurrentUser = Depends(require_role("patient"))):
    # Verify ownership indirectly
    doc_res = supabase_admin.table('medical_documents').select('id').eq('id', doc_id).eq('patient_id', current_user.id).execute()
    if not doc_res.data:
        raise HTTPException(status_code=404, detail="Document not found")

    res = supabase_admin.table('ai_analysis').select('*').eq('document_id', doc_id).order('created_at', desc=True).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return res.data[0]
