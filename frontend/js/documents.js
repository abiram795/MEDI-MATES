import { request } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    loadDocuments();

    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('file-input');
            const file = fileInput.files[0];
            if (!file) return;

            const btn = document.getElementById('upload-btn');
            const originalText = btn.textContent;
            btn.textContent = 'Uploading...';
            btn.disabled = true;

            const formData = new FormData();
            formData.append('file', file);

            try {
                await request('/documents/upload', {
                    method: 'POST',
                    body: formData
                });
                alert('Document uploaded successfully!');
                fileInput.value = '';
                loadDocuments();
            } catch (error) {
                document.getElementById('upload-error').textContent = error.message;
            } finally {
                btn.textContent = originalText;
                btn.disabled = false;
            }
        });
    }
});

async function loadDocuments() {
    const listDiv = document.getElementById('documents-list');
    if (!listDiv) return;

    try {
        const docs = await request('/documents/');
        if (docs.length > 0) {
            listDiv.innerHTML = docs.map(doc => `
                <div class="card">
                    <h3>${doc.file_name}</h3>
                    <p>Uploaded: ${new Date(doc.uploaded_at).toLocaleDateString()}</p>
                    <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                        <a href="${doc.download_url}" target="_blank" class="btn btn-secondary" style="font-size: 0.8rem;">View</a>
                        <button onclick="window.analyzeDoc('${doc.id}')" class="btn btn-primary" style="font-size: 0.8rem;">AI Analysis</button>
                        <button onclick="window.deleteDoc('${doc.id}')" class="btn btn-secondary" style="font-size: 0.8rem; color: var(--danger); border-color: var(--danger);">Delete</button>
                    </div>
                </div>
            `).join('');
        } else {
            listDiv.innerHTML = '<p>No documents found.</p>';
        }
    } catch (error) {
        listDiv.innerHTML = `<p class="error">Error loading documents: ${error.message}</p>`;
    }
}

window.deleteDoc = async function(id) {
    if (!confirm('Are you sure you want to delete this document?')) return;
    try {
        await request(`/documents/${id}`, { method: 'DELETE' });
        loadDocuments();
    } catch (e) {
        alert('Delete failed: ' + e.message);
    }
};

window.analyzeDoc = function(id) {
    window.location.href = `report-analysis.html?doc_id=${id}`;
};
