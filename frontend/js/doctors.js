import { request, showLoading, hideLoading, renderList } from './api.js'; // Note: update ui import

document.addEventListener('DOMContentLoaded', async () => {
    await loadSpecialties();
    searchDoctors();
});

async function loadSpecialties() {
    try {
        const specs = await request('/doctors/specialties/all');
        const select = document.getElementById('search-spec');
        if (specs && select) {
            specs.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.textContent = s.name;
                select.appendChild(opt);
            });
        }
    } catch (e) {
        console.error("Failed to load specialties", e);
    }
}

window.searchDoctors = async function() {
    const name = document.getElementById('search-name').value;
    const spec = document.getElementById('search-spec').value;

    let url = '/doctors/';
    const params = new URLSearchParams();
    if (name) params.append('search', name);
    if (spec) params.append('specialty_id', spec);
    if (params.toString()) url += '?' + params.toString();

    const listDiv = document.getElementById('doctors-list');
    listDiv.innerHTML = '<p>Loading doctors...</p>';

    try {
        const doctors = await request(url);
        if (doctors.length > 0) {
            listDiv.innerHTML = doctors.map(d => `
                <div class="card">
                    <h3>Dr. ${d.name}</h3>
                    <p><strong>Specialty:</strong> ${d.specialties ? d.specialties.name : 'General'}</p>
                    <p><strong>Experience:</strong> ${d.experience ? d.experience + ' years' : 'N/A'}</p>
                    <p><strong>Hospital:</strong> ${d.hospital ? d.hospital.hospital_name : 'N/A'}</p>
                    <p><strong>Contact:</strong> ${d.contact_info || 'N/A'}</p>
                </div>
            `).join('');
        } else {
            listDiv.innerHTML = '<p>No doctors found matching your criteria.</p>';
        }
    } catch (error) {
        listDiv.innerHTML = `<p class="error">Error loading doctors: ${error.message}</p>`;
    }
}
