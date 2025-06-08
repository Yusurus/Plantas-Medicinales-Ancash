class TraditionalLogin {
    constructor() {
        this.loginForm = document.getElementById('loginForm');
        this.statusMessage = document.getElementById('statusMessage');
        this.loginSpinner = document.getElementById('loginSpinner');
        
        this.initializeEventListeners();
        this.initializeFormValidation();
    }

    initializeEventListeners() {
        this.loginForm.addEventListener('submit', (e) => this.handleTraditionalLogin(e));
    }

    initializeFormValidation() {
        const inputs = this.loginForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => this.validateInput(input));
            input.addEventListener('blur', () => this.validateInput(input));
        });
    }

    validateInput(input) {
        const value = input.value.trim();
        
        if (input.hasAttribute('required') && !value) {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        }
        
        if (input.type === 'password' && value.length < 3) {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        }
        
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        return true;
    }

    showStatus(message, type = 'info', duration = 5000) {
        this.statusMessage.textContent = message;
        this.statusMessage.className = `status-message status-${type}`;
        this.statusMessage.style.display = 'block';
        
        // Añadir icono según el tipo
        const icon = this.getStatusIcon(type);
        this.statusMessage.innerHTML = `${icon} ${message}`;
        
        if (duration > 0) {
            setTimeout(() => {
                this.statusMessage.style.display = 'none';
            }, duration);
        }
    }

    getStatusIcon(type) {
        const icons = {
            success: '<i class="fas fa-check-circle me-2"></i>',
            error: '<i class="fas fa-exclamation-triangle me-2"></i>',
            info: '<i class="fas fa-info-circle me-2"></i>',
            warning: '<i class="fas fa-exclamation-circle me-2"></i>'
        };
        return icons[type] || icons.info;
    }

    async handleTraditionalLogin(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        
        // Validar campos
        const usernameValid = this.validateInput(document.getElementById('username'));
        const passwordValid = this.validateInput(document.getElementById('password'));
        
        if (!usernameValid || !passwordValid) {
            this.showStatus('Por favor, completa todos los campos correctamente.', 'error');
            return;
        }
        
        this.loginSpinner.classList.remove('d-none');
        const submitBtn = this.loginForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    timestamp: Date.now()
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showStatus(result.message, 'success');
                submitBtn.classList.add('success');
                submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Acceso Concedido';
                
                setTimeout(() => {
                    this.redirectToSuccess(result.user, 'traditional');
                }, 1500);
            } else {
                this.showStatus(result.message, 'error');
                submitBtn.classList.add('error');
                setTimeout(() => {
                    submitBtn.classList.remove('error');
                    submitBtn.innerHTML = '<i class="fas fa-sign-in-alt me-2"></i>Iniciar Sesión';
                }, 2000);
            }
            
        } catch (error) {
            console.error('Error en login:', error);
            this.showStatus('Error de conexión. Verifica tu conexión a internet.', 'error');
        } finally {
            this.loginSpinner.classList.add('d-none');
            submitBtn.disabled = false;
        }
    }

    redirectToSuccess(username, method) {
        // Redirigir al HTML de éxito
        const params = new URLSearchParams({
            username: username,
            method: method
        });
        window.location.href = `/Acceso?${params.toString()}`;
    }
}