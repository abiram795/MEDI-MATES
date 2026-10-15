import { request } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const role = localStorage.getItem('role');

    if (role === 'PATIENT') {
        try {
            const profile = await request('/patients/me');
            document.getElementById('welcome-msg').textContent = `Good Morning, ${profile.full_name || 'Patient'}`;

            // Load stats
            const docs = await request('/documents/');
            document.getElementById('stats-docs').textContent = docs.length;

            // Since AI analyses map 1:1 to documents now, reports count could just be docs with an analysis.
            // For simplicity, we just show document count in both for this mock or hide reports count.
            document.getElementById('stats-reports').textContent = docs.length;

            // Load recent activity from document uploads since medical_history table doesn't exist
            const activityDiv = document.getElementById('recent-activity');
            if (docs.length > 0) {
                activityDiv.innerHTML = docs.slice(0,3).map(d => `
                    <div class="card">
                        <p><strong>${new Date(d.uploaded_at).toLocaleDateString()}</strong></p>
                        <p>Document Uploaded: ${d.file_name}</p>
                    </div>
                `).join('');
            } else {
                activityDiv.innerHTML = '<p>No recent activity. Upload a document to start your timeline.</p>';
            }

        } catch (error) {
            console.error('Failed to load patient dashboard', error);
        }
    } else if (role === 'HOSPITAL') {
        try {
            const profile = await request('/hospitals/me');
            if (!profile.approved) {
                document.getElementById('approval-status').style.display = 'block';
            }
        } catch (error) {
            console.error('Failed to load hospital dashboard', error);
        }
    } else if (role === 'ADMIN') {
        try {
            const users = await request('/admin/users');
            const hospitals = await request('/admin/hospitals');

            document.getElementById('admin-users').textContent = users.length;

            const pending = hospitals.filter(h => !h.approved);
            document.getElementById('admin-hospitals').textContent = pending.length;

            const listDiv = document.getElementById('pending-list');
            if (pending.length > 0) {
                listDiv.innerHTML = pending.map(h => `
                    <div class="card">
                        <h3>${h.hospital_name}</h3>
                        <p>Status: Pending</p>
                        <button onclick="window.approveHospital('${h.id}')" class="btn btn-success">Approve</button>
                    </div>
                `).join('');
            } else {
                listDiv.innerHTML = '<p>No pending approvals.</p>';
            }
        } catch (error) {
            console.error('Failed to load admin dashboard', error);
        }
    }
});

window.approveHospital = async function(id) {
    try {
        await request(`/admin/hospitals/${id}/approve`, { method: 'PUT' });
        alert('Hospital approved');
        window.location.reload();
    } catch (e) {
        alert('Error approving: ' + e.message);
    }
}
