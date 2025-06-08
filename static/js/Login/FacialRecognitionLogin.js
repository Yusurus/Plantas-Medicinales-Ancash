class FacialRecognition {
    constructor() {
        this.video = document.getElementById('video');
        this.loginPanel = document.getElementById('loginPanel');
        this.cameraPanel = document.getElementById('cameraPanel');
        this.faceLoginBtn = document.getElementById('faceLoginBtn');
        this.captureBtn = document.getElementById('captureBtn');
        this.cancelBtn = document.getElementById('cancelBtn');
        this.statusMessage = document.getElementById('statusMessage');
        this.captureSpinner = document.getElementById('captureSpinner');
        this.stream = null;
        this.isProcessing = false;
        this.faceDetectionInterval = null;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.faceLoginBtn.addEventListener('click', () => this.startFaceRecognition());
        this.captureBtn.addEventListener('click', () => this.captureAndVerify());
        this.cancelBtn.addEventListener('click', () => this.stopCamera());
        
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
        // AGREGAR ESTOS LOGS PARA DEBUG
        console.log('Resultado completo:', result);
        console.log('Usuario:', result.user);
        console.log('Mensaje:', result.message);
        
        const confidence = result.confidence || 'N/A';
        const message = result.message || `¡Bienvenido, ${result.user}!`;
        
        this.showStatus(
            `${message} (Confianza: ${confidence}%)`, 
            'success'
        );
        
        this.captureBtn.classList.add('success');
        this.captureBtn.innerHTML = '<i class="fas fa-check me-2"></i>Verificación Exitosa';
        
        // Efectos visuales de éxito
        this.addSuccessEffects();
        
        setTimeout(() => {
            this.stopCamera();
            // USAR result.user o un valor por defecto
            const username = result.user || 'Usuario';
            console.log('Redirigiendo con usuario:', username);
            this.redirectToSuccess(username, 'facial');
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

    // MÉTODO CORREGIDO - Este es el cambio principal
    redirectToSuccess(username, method) {
        // Crear los parámetros de la URL
        const params = new URLSearchParams({
            username: username || 'Usuario',
            method: method || 'facial'
        });
        
        // Redirigir usando la URL completa
        const successUrl = `/Acceso?${params.toString()}`;
        
        console.log('Redirigiendo a:', successUrl); // Para debug
        
        // Usar window.location.href para la redirección
        window.location.href = successUrl;
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