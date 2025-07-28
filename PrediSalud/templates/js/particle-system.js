// Sistema de Partículas Avanzado para PrediSalud
class ParticleSystem {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.options = {
            particleCount: options.particleCount || 50,
            particleSize: options.particleSize || 3,
            particleSpeed: options.particleSpeed || 0.5,
            particleColor: options.particleColor || '#ffffff',  // Partículas blancas
            particleOpacity: options.particleOpacity || 0.6,
            connectionDistance: options.connectionDistance || 150,
            connectionColor: options.connectionColor || '#ffffff',  // Conexiones blancas
            connectionOpacity: options.connectionOpacity || 0.3,
            ...options
        };
        
        this.init();
    }

    init() {
        this.resize();
        this.createParticles();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        for (let i = 0; i < this.options.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * this.options.particleSpeed,
                vy: (Math.random() - 0.5) * this.options.particleSpeed,
                size: Math.random() * this.options.particleSize + 1,
                opacity: Math.random() * this.options.particleOpacity + 0.2
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Actualizar y dibujar partículas
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Rebotar en los bordes
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
            
            // Dibujar partícula
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, -10, Math.PI * 2);
            this.ctx.fillStyle = `rgba(0, 123, 255, ${particle.opacity})`;  // Azul
            this.ctx.fill();
        });
        
        // Dibujar conexiones
        this.drawConnections();
        
        requestAnimationFrame(() => this.animate());
    }

    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < this.options.connectionDistance) {
                    const opacity = (this.options.connectionDistance - distance) / this.options.connectionDistance * this.options.connectionOpacity;
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.strokeStyle = `rgba(0, 123, 255, ${opacity})`;  // Azul
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        }
    }
}

// Inicializar sistema de partículas cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    const particleCanvas = document.getElementById('particle-canvas');
    if (particleCanvas) {
        new ParticleSystem(particleCanvas, {
            particleCount: 40,         // Más partículas
            particleSize: 2,           // Partículas más pequeñas y sutiles
            particleSpeed: 0.2,        // Movimiento más lento
            connectionDistance: 80,    // Menor distancia para más conexiones
            particleOpacity: 0.6,      // Más sutiles
            connectionOpacity: 0.3     // Conexiones sutiles
        });
    }
}); 