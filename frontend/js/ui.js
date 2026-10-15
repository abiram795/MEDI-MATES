// Common UI utilities

export function showLoading(elementId) {
    const el = document.getElementById(elementId);
    if(el) {
        el.setAttribute('data-original', el.innerHTML);
        el.innerHTML = 'Loading...';
        el.disabled = true;
    }
}

export function hideLoading(elementId) {
    const el = document.getElementById(elementId);
    if(el && el.hasAttribute('data-original')) {
        el.innerHTML = el.getAttribute('data-original');
        el.disabled = false;
    }
}

export function renderList(containerId, data, renderFn, emptyMessage = 'No items found.') {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!data || data.length === 0) {
        container.innerHTML = `<p>${emptyMessage}</p>`;
        return;
    }

    container.innerHTML = data.map(renderFn).join('');
}

// Redirect if not logged in on protected pages
document.addEventListener('DOMContentLoaded', () => {
    const protectedRoutes = ['patient-dashboard.html', 'hospital-dashboard.html', 'admin-dashboard.html', 'report-analysis.html'];
    const currentPath = window.location.pathname.split('/').pop();

    if (protectedRoutes.includes(currentPath) && !localStorage.getItem('token')) {
        window.location.href = 'login.html';
    }
});
