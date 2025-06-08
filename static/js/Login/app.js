// Inicializar la aplicación cuando se carga la página
        document.addEventListener('DOMContentLoaded', () => {
            // Instanciar ambas clases
            const traditionalLogin = new TraditionalLogin();
            const facialRecognition = new FacialRecognition();
            
            // Manejar redimensionamiento de ventana para reconocimiento facial
            window.addEventListener('resize', () => {
                facialRecognition.handleResize();
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

                @keyframes slideInRight {
                    from {
                        opacity: 0;
                        transform: translateX(30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
            `;
            document.head.appendChild(style);
            
            // Mostrar información de desarrollo en consola
            console.log(`
            ==========================================
            🚀 SISTEMA DE RECONOCIMIENTO FACIAL v2.0
            ==========================================
            
            ✨ Arquitectura modular:
            ✅ TraditionalLogin.js - Manejo de login tradicional
            ✅ FacialRecognition.js - Reconocimiento facial
            ✅ App.js - Coordinador principal
            
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
            • Redirección a página de éxito separada
            
            🔧 Controles de teclado:
            • ESC: Cancelar reconocimiento facial
            • Enter: Capturar imagen (cuando cámara activa)
            
            📱 Responsive:
            • Desktop: Paneles lado a lado
            • Mobile: Paneles apilados verticalmente
            `);
        });