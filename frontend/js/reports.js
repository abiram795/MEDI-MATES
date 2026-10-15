import { request } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const docId = urlParams.get('doc_id');

    if (!docId) {
        document.getElementById('no-doc').style.display = 'block';
        return;
    }

    const loadingDiv = document.getElementById('loading');
    const contentDiv = document.getElementById('analysis-content');
    loadingDiv.style.display = 'block';

    try {
        // First try to fetch existing analysis
        let analysisData;
        try {
            const res = await request(`/reports/${docId}/analysis`);
            analysisData = res.analysis_result;
        } catch (err) {
            // If not found, trigger analysis
            const res = await request(`/reports/${docId}/analyze`, { method: 'POST' });
            analysisData = res.analysis_result;
        }

        renderAnalysis(analysisData);
        loadingDiv.style.display = 'none';
        contentDiv.style.display = 'block';

    } catch (error) {
        loadingDiv.innerHTML = `<p class="error">Failed to analyze report: ${error.message}</p>`;
    }
});

function renderAnalysis(data) {
    if (!data) return;

    document.getElementById('a-summary').textContent = data.summary || "No summary available.";

    document.getElementById('a-explanation-en').textContent = data.simple_explanation_en || "";
    document.getElementById('a-explanation-ta').textContent = data.simple_explanation_ta || "";

    const obsDiv = document.getElementById('a-observations');
    if (data.observations && data.observations.length > 0) {
        obsDiv.innerHTML = data.observations.map(obs => `
            <div class="observation-row">
                <div>
                    <strong>${obs.test}</strong><br>
                    <span style="font-size: 0.9rem; color: #666;">Range: ${obs.reference_range || 'N/A'}</span>
                </div>
                <div style="text-align: right;">
                    <strong>${obs.value}</strong><br>
                    <span class="status-badge status-${obs.status || 'Normal'}">${obs.status || 'Normal'}</span>
                </div>
            </div>
        `).join('');
    } else {
        obsDiv.innerHTML = "<p>No specific key findings extracted.</p>";
    }

    const qList = document.getElementById('a-questions');
    if (data.questions_for_doctor) {
        qList.innerHTML = data.questions_for_doctor.map(q => `<li>${q}</li>`).join('');
    }

    const fList = document.getElementById('a-followup');
    if (data.follow_up_notes) {
        fList.innerHTML = data.follow_up_notes.map(f => `<li>${f}</li>`).join('');
    }
}

window.setLang = function(lang) {
    const btns = document.querySelectorAll('.lang-btn');
    btns.forEach(b => b.classList.remove('active'));

    if (lang === 'en') {
        btns[0].classList.add('active');
        document.getElementById('a-explanation-en').style.display = 'block';
        document.getElementById('a-explanation-ta').style.display = 'none';
    } else {
        btns[1].classList.add('active');
        document.getElementById('a-explanation-en').style.display = 'none';
        document.getElementById('a-explanation-ta').style.display = 'block';
    }
}
