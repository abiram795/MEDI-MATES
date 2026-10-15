import { request } from './api.js';

let isLoginMode = true;

const authForm = document.getElementById('auth-form');
const toggleBtn = document.getElementById('toggle-auth');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const toggleText = document.getElementById('toggle-text');
const errorMsg = document.getElementById('error-message');

if (toggleBtn) {
    toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        isLoginMode = !isLoginMode;

        const registerFields = document.querySelectorAll('.register-only');
        registerFields.forEach(el => el.style.display = isLoginMode ? 'none' : 'block');

        formTitle.textContent = isLoginMode ? 'Login' : 'Register';
        submitBtn.textContent = isLoginMode ? 'Login' : 'Register';
        toggleText.innerHTML = isLoginMode
            ? `Don't have an account? <a href="#" id="toggle-auth">Register</a>`
            : `Already have an account? <a href="#" id="toggle-auth">Login</a>`;

        // Re-attach event listener to new toggle element
        document.getElementById('toggle-auth').addEventListener('click', toggleBtn.onclick);
        errorMsg.textContent = '';
    });
}

if (authForm) {
    authForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            if (isLoginMode) {
                const data = await request('/auth/login', {
                    method: 'POST',
                    body: JSON.stringify({ email, password })
                });
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('role', data.role);

                if (data.role === 'PATIENT') window.location.href = 'patient-dashboard.html';
                else if (data.role === 'HOSPITAL') window.location.href = 'hospital-dashboard.html';
                else if (data.role === 'ADMIN') window.location.href = 'admin-dashboard.html';
            } else {
                const role = document.getElementById('role').value;
                await request('/auth/register', {
                    method: 'POST',
                    body: JSON.stringify({ email, password, role })
                });
                alert('Registration successful! Please login.');
                window.location.reload();
            }
        } catch (error) {
            errorMsg.textContent = error.message;
        }
    });
}

export function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = 'login.html';
}

// Attach globally for inline HTML usage if needed
window.logout = logout;
