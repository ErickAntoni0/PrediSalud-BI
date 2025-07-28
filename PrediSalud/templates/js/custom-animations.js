// Inicializar AOS (Animate On Scroll)
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true,
    offset: 100
});

// Animación para contadores
$(document).ready(function() {
    // Animación de contadores cuando están en vista
    $('.counter-stat').each(function() {
        $(this).waypoint(function() {
            $(this.element).addClass('animated');
        }, {
            offset: '90%'
        });
    });

    // Efecto hover para botones
    $('.btn').hover(
        function() {
            $(this).addClass('pulse');
        },
        function() {
            $(this).removeClass('pulse');
        }
    );

    // Animación para iconos de servicios
    $('.feature-icon i').hover(
        function() {
            $(this).addClass('bounce');
        },
        function() {
            $(this).removeClass('bounce');
        }
    );

    // Smooth scroll para enlaces internos
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Animación para formularios
    $('input, textarea').focus(function() {
        $(this).parent().addClass('focused');
    }).blur(function() {
        if ($(this).val() === '') {
            $(this).parent().removeClass('focused');
        }
    });

    // Efecto parallax para imágenes de fondo
    $(window).scroll(function() {
        var scrolled = $(this).scrollTop();
        $('.banner').css('transform', 'translateY(' + (scrolled * 0.5) + 'px)');
    });
});

// Función para mostrar notificaciones
function showNotification(message, type = 'success') {
    const notification = $(`
        <div class="notification notification-${type}">
            <div class="notification-content">
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        </div>
    `);
    
    $('body').append(notification);
    
    setTimeout(() => {
        notification.addClass('show');
    }, 100);
    
    setTimeout(() => {
        notification.removeClass('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
    
    notification.find('.notification-close').click(function() {
        notification.removeClass('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
} 