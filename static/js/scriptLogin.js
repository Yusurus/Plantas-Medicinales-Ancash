class FaceRecognitionLogin {
    constructor() {
        this.video = document.getElementById('video');
        this.loginPanel = document.getElementById('loginPanel');
        this.cameraPanel = document.getElementById('cameraPanel');
        this.faceLoginBtn = document.getElementById('faceLoginBtn');
        this.captureBtn = document.getElementById('captureBtn');
        this.cancelBtn = document.getElementById('cancelBtn');
        this.loginForm = document.getElementById('loginForm');
        this.statusMessage = document.getElementById('statusMessage');
        this.loginSpinner = document.getElementById('loginSpinner');
        this.captureSpinner = document.getElementById('captureSpinner');
        this.stream = null;
        this.isProcessing = false;
        this.faceDetectionInterval = null;
        
        this.initializeEventListeners();
        this.initializeFormValidation();
    }

    initializeEventListeners() {
        this.faceLoginBtn.addEventListener('click', () => this.startFaceRecognition());
        this.captureBtn.addEventListener('click', () => this.captureAndVerify());
        this.cancelBtn.addEventListener('click', () => this.stopCamera());
        this.loginForm.addEventListener('submit', (e) => this.handleTraditionalLogin(e));
        
        // Eventos de teclado para mejor UX
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.cameraPanel && !this.cameraPanel.classList.contains('d-none')) {
                this.stopCamera();
            }
            if (e.key === 'Enter' && this.cameraPanel && !this.cameraPanel.classList.contains('d-none')) {
                if (!this.isProcessing) {
                    this.captureAndVerify();
                }
            }
        });
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

    async startFaceRecognition() {
        try {
            this.faceLoginBtn.disabled = true;
            this.showStatus('Iniciando cámara...', 'info');
            
            // Verificar soporte de cámara
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Tu navegador no soporta acceso a la cámara');
            }
            
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 640, max: 1280 },
                    height: { ideal: 480, max: 720 },
                    facingMode: 'user',
                    frameRate: { ideal: 30 }
                } 
            });
            
            this.video.srcObject = this.stream;
            
            // Esperar a que el video esté listo
            await new Promise((resolve) => {
                this.video.onloadedmetadata = () => {
                    resolve();
                };
            });
            
            this.showPanelTransition();
            this.startFaceDetection();
            this.showStatus('Cámara lista. Posiciona tu rostro en el marco y presiona "Capturar".', 'success');
            
        } catch (error) {
            console.error('Error al acceder a la cámara:', error);
            this.handleCameraError(error);
            this.faceLoginBtn.disabled = false;
        }
    }

    handleCameraError(error) {
        let errorMessage = 'Error: No se pudo acceder a la cámara.';
        
        switch(error.name) {
            case 'NotAllowedError':
                errorMessage = 'Permisos de cámara denegados. Por favor, permite el acceso a la cámara y recarga la página.';
                break;
            case 'NotFoundError':
                errorMessage = 'No se encontró una cámara en este dispositivo.';
                break;
            case 'NotReadableError':
                errorMessage = 'La cámara está siendo usada por otra aplicación.';
                break;
            case 'OverconstrainedError':
                errorMessage = 'No se pudo configurar la cámara con los parámetros solicitados.';
                break;
            case 'SecurityError':
                errorMessage = 'Error de seguridad. Asegúrate de estar usando HTTPS.';
                break;
            default:
                errorMessage = `Error de cámara: ${error.message}`;
        }
        
        this.showStatus(errorMessage, 'error', 10000);
    }

    showPanelTransition() {
        // Animar transición a layout de dos columnas
        this.loginPanel.classList.add('panel-transition');
        this.cameraPanel.classList.add('panel-transition');
        
        // En desktop, mostrar ambos paneles lado a lado
        if (window.innerWidth >= 992) {
            this.loginPanel.classList.remove('col-md-8', 'mx-auto');
            this.loginPanel.classList.add('col-lg-6');
            this.cameraPanel.classList.remove('col-md-8', 'mx-auto');
            this.cameraPanel.classList.add('col-lg-6');
        }
        
        // Mostrar panel de cámara
        setTimeout(() => {
            this.cameraPanel.classList.remove('d-none');
            this.cameraPanel.classList.add('panel-slide-in');
        }, 100);
    }

    startFaceDetection() {
        // Simulación básica de detección de rostro
        const faceFrame = document.querySelector('.face-frame');
        let pulseIntensity = 0.7;
        
        this.faceDetectionInterval = setInterval(() => {
            if (this.video.videoWidth > 0 && this.video.videoHeight > 0) {
                // Simular detección de rostro con variación de intensidad
                pulseIntensity = 0.7 + Math.random() * 0.3;
                faceFrame.style.opacity = pulseIntensity;
                
                // Cambiar color del marco basado en "calidad" de detección
                if (pulseIntensity > 0.9) {
                    faceFrame.style.borderColor = 'rgba(0, 255, 136, 0.8)';
                } else if (pulseIntensity > 0.8) {
                    faceFrame.style.borderColor = 'rgba(255, 255, 0, 0.8)';
                } else {
                    faceFrame.style.borderColor = 'rgba(255, 255, 255, 0.8)';
                }
            }
        }, 100);
    }

    async captureAndVerify() {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        this.captureSpinner.classList.remove('d-none');
        this.captureBtn.disabled = true;
        this.showStatus('Capturando y verificando rostro...', 'info', 0);

        try {
            // Verificar que el video esté activo
            if (!this.video.videoWidth || !this.video.videoHeight) {
                throw new Error('El video no está disponible');
            }

            // Capturar frame del video
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;
            
            // Aplicar efectos visuales durante la captura
            this.video.style.filter = 'brightness(1.2) contrast(1.1)';
            setTimeout(() => {
                this.video.style.filter = 'none';
            }, 200);
            
            context.drawImage(this.video, 0, 0);
            
            // Convertir a base64 con compresión optimizada
            const imageBase64 = canvas.toDataURL('image/jpeg', 0.85);
            
            // Validar tamaño de imagen
            if (imageBase64.length > 5000000) { // 5MB límite
                throw new Error('La imagen es demasiado grande');
            }
            
            // Enviar al servidor con timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 segundos timeout
            
            const response = await fetch('/api/verify-face', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageBase64,
                    timestamp: Date.now()
                }),
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                this.handleSuccessfulRecognition(result);
            } else {
                this.handleFailedRecognition(result);
            }
            
        } catch (error) {
            console.error('Error en la captura:', error);
            this.handleCaptureError(error);
        } finally {
            this.isProcessing = false;
            this.captureSpinner.classList.add('d-none');
            this.captureBtn.disabled = false;
        }
    }

    handleSuccessfulRecognition(result) {
        const confidence = result.confidence || 'N/A';
        this.showStatus(
            `${result.message} (Confianza: ${confidence}%)`, 
            'success'
        );
        
        this.captureBtn.classList.add('success');
        this.captureBtn.innerHTML = '<i class="fas fa-check me-2"></i>Verificación Exitosa';
        
        // Efectos visuales de éxito
        this.addSuccessEffects();
        
        setTimeout(() => {
            this.stopCamera();
            this.redirectToDashboard(result.user);
        }, 2000);
    }

    handleFailedRecognition(result) {
        this.showStatus(result.message || 'No se pudo verificar el rostro', 'error');
        this.captureBtn.classList.add('error');
        
        // Efectos visuales de error
        this.addErrorEffects();
        
        setTimeout(() => {
            this.captureBtn.classList.remove('error');
            this.captureBtn.innerHTML = '<i class="fas fa-camera-retro me-2"></i>Capturar y Verificar';
        }, 3000);
    }

    handleCaptureError(error) {
        let errorMessage = 'Error de conexión. Verifica tu conexión a internet.';
        
        if (error.name === 'AbortError') {
            errorMessage = 'La verificación tardó demasiado. Inténtalo de nuevo.';
        } else if (error.message.includes('servidor')) {
            errorMessage = 'Error del servidor. Inténtalo más tarde.';
        } else if (error.message) {
            errorMessage = error.message;
        }
        
        this.showStatus(errorMessage, 'error');
        this.captureBtn.classList.add('error');
        
        setTimeout(() => {
            this.captureBtn.classList.remove('error');
            this.captureBtn.innerHTML = '<i class="fas fa-camera-retro me-2"></i>Capturar y Verificar';
        }, 3000);
    }

    addSuccessEffects() {
        // Efecto de confeti o celebración
        const faceFrame = document.querySelector('.face-frame');
        faceFrame.style.borderColor = 'rgba(0, 255, 136, 1)';
        faceFrame.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.5)';
        
        // Animación de éxito
        faceFrame.style.animation = 'successPulse 0.5s ease-in-out';
    }

    addErrorEffects() {
        const faceFrame = document.querySelector('.face-frame');
        faceFrame.style.borderColor = 'rgba(255, 0, 0, 1)';
        faceFrame.style.animation = 'errorShake 0.5s ease-in-out';
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        if (this.faceDetectionInterval) {
            clearInterval(this.faceDetectionInterval);
            this.faceDetectionInterval = null;
        }
        
        // Restaurar layout original
        this.restorePanelLayout();
        
        // Limpiar estados
        this.faceLoginBtn.disabled = false;
        this.captureBtn.classList.remove('success', 'error');
        this.captureBtn.innerHTML = '<i class="fas fa-camera-retro me-2"></i>Capturar y Verificar';
        this.isProcessing = false;
    }

    restorePanelLayout() {
        this.cameraPanel.classList.add('d-none');
        this.cameraPanel.classList.remove('panel-slide-in');
        
        // Restaurar clases originales
        if (window.innerWidth >= 992) {
            this.loginPanel.classList.remove('col-lg-6');
            this.loginPanel.classList.add('col-md-8', 'mx-auto');
            this.cameraPanel.classList.remove('col-lg-6');
            this.cameraPanel.classList.add('col-md-8', 'mx-auto');
        }
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
                    this.redirectToDashboard(result.user);
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

    redirectToDashboard(username) {
        // Crear página de éxito mejorada con Bootstrap
        document.body.innerHTML = `
            <div class="min-vh-100 d-flex align-items-center justify-content-center" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            ">
                <div class="container">
                    <div class="row justify-content-center">
                        <div class="col-md-8 col-lg-6">
                            <div class="text-center text-white" style="
                                background: rgba(255, 255, 255, 0.1);
                                backdrop-filter: blur(15px);
                                padding: 60px 40px;
                                border-radius: 20px;
                                box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
                                border: 1px solid rgba(255, 255, 255, 0.2);
                                animation: successEntry 0.8s ease-out;
                            ">
                                <div style="font-size: 4em; margin-bottom: 20px; animation: bounce 2s ease-in-out infinite;">🎉</div>
                                <h2 class="mb-4 fw-light" style="font-size: 2.5em;">¡Acceso Concedido!</h2>
                                <p class="fs-5 mb-2 opacity-75">Bienvenido de vuelta,</p>
                                <p class="fs-2 mb-4 fw-bold" style="color: #ffd700;">${username}</p>
                                <p class="opacity-75 mb-4 fs-6">Has accedido exitosamente al sistema de reconocimiento facial</p>
                                
                                <div class="d-flex gap-3 justify-content-center flex-wrap">
                                    <button onclick="location.reload()" class="btn btn-outline-light btn-lg">
                                        <i class="fas fa-redo me-2"></i>
                                        Volver al Login
                                    </button>
                                    <a href="/registrar_planta" class="btn btn-success btn-lg">
                                        <i class="fas fa-tachometer-alt me-2"></i>
                                        Ir al Dashboard
                                    </a>
                                </div>
                                
                                <div class="mt-4 pt-4 border-top border-light border-opacity-25">
                                    <small class="opacity-75">
                                        <i class="fas fa-shield-alt me-1"></i>
                                        Sesión autenticada con tecnología de reconocimiento facial
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <style>
                    @keyframes successEntry {
                        from {
                            opacity: 0;
                            transform: scale(0.9) translateY(20px);
                        }
                        to {
                            opacity: 1;
                            transform: scale(1) translateY(0);
                        }
                    }
                    
                    @keyframes bounce {
                        0%, 20%, 60%, 100% {
                            transform: translateY(0);
                        }
                        40% {
                            transform: translateY(-15px);
                        }
                        80% {
                            transform: translateY(-8px);
                        }
                    }
                    
                    @keyframes successPulse {
                        0% { transform: scale(1); }
                        50% { transform: scale(1.1); }
                        100% { transform: scale(1); }
                    }
                    
                    @keyframes errorShake {
                        0%, 100% { transform: translateX(0); }
                        25% { transform: translateX(-5px); }
                        75% { transform: translateX(5px); }
                    }
                    
                    .btn:hover {
                        transform: translateY(-2px);
                        transition: all 0.3s ease;
                    }
                </style>
            </div>
        `;
    }

    // Método para manejar redimensionamiento de ventana
    handleResize() {
        if (this.stream && !this.cameraPanel.classList.contains('d-none')) {
            // Reajustar layout responsivo si es necesario
            this.restorePanelLayout();
            setTimeout(() => {
                this.showPanelTransition();
            }, 100);
        }
    }
}

// Inicializar la aplicación cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    const app = new FaceRecognitionLogin();
    
    // Manejar redimensionamiento de ventana
    window.addEventListener('resize', () => {
        app.handleResize();
    });
    
    // Agregar animaciones CSS adicionales
    const style = document.createElement('style');
    style.textContent = `
        @keyframes successPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        @keyframes errorShake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .panel-transition {
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .panel-slide-in {
            animation: slideInRight 0.6s ease-out;
        }
    `;
    document.head.appendChild(style);
    
    // Mostrar información de desarrollo en consola
    console.log(`
    ==========================================
    🚀 SISTEMA DE RECONOCIMIENTO FACIAL v2.0
    ==========================================
    
    ✨ Nuevas características:
    ✅ Layout responsivo con Bootstrap 5
    ✅ Transición suave entre paneles
    ✅ Cámara aparece a la derecha (desktop)
    ✅ Detección visual de rostro simulada
    ✅ Validación de formularios en tiempo real
    ✅ Manejo avanzado de errores
    ✅ Efectos visuales mejorados
    ✅ Navegación por teclado (ESC/Enter)
    
    🎯 Funcionalidades:
    • Login tradicional con validación
    • Reconocimiento facial con DeepFace
    • Interfaz responsive y moderna
    • Transiciones suaves entre estados
    • Manejo robusto de errores de cámara
    
    🔧 Controles de teclado:
    • ESC: Cancelar reconocimiento facial
    • Enter: Capturar imagen (cuando cámara activa)
    
    📱 Responsive:
    • Desktop: Paneles lado a lado
    • Mobile: Paneles apilados verticalmente
    `);
});