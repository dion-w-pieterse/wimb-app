$(document).ready(function () { 
    checkScroll(); 
    $(window).scroll(checkScroll); 
});

function checkScroll() { 
    if ($(window).scrollTop() >= 300) { 
        $('.navbar').addClass('solid'); 
    } else { 
        $('.navbar').removeClass('solid'); 
    }
}


$('.navbar-toggler').click(function () { 
    if ($(window).scrollTop() <= 300) { 
        $("nav.navbar").toggleClass("solid-toggle"); 
    }
});



$(document).on('click', 'a[href^="#"]', function (event) {
    event.preventDefault();
    $('.navbar-toggler').addClass('collapsed');
    $('#navbarResponsive').removeClass('show');

    setTimeout(function () {
        $('nav.navbar').removeClass('solid-toggle');
    }, 300);

    $('html, body').animate({
        scrollTop: $($.attr(this, 'href')).offset().top
    }, 1000);
});


$(document).ready(function () {
    $(window).scroll(function () {
        $('.bouncing-book').css('opacity', 1 - $(window).scrollTop() / 250);
    });
});

$(document).ready(function () {
    $('.counter').counterUp({
        delay: 10,
        time: 3000,
        beginAt: 0
    });
});

//Original Resource: https://www.oxygenna.com/tutorials/scroll-animations-using-waypoints-js-animate-css
$(function () { 
    function onScrollInit(items, trigger) { 
        items.each(function () { 
            var osElement = $(this), 
                osAnimationClass = osElement.attr('data-animation'), 
                osAnimationDelay = osElement.attr('data-delay'); 

            osElement.css({ 
                '-webkit-animation-delay': osAnimationDelay, 
                '-moz-animation-delay': osAnimationDelay, 
                'animation-delay': osAnimationDelay 
            });

            var osTrigger = (trigger) ? trigger : osElement; 

            osTrigger.waypoint(function () { 
                osElement.addClass('animated').addClass(osAnimationClass); 
            }, {
                triggerOnce: true, 
                offset: '70%' 
            });
        });
    }

    onScrollInit($('.os-animation')); 
    onScrollInit($('.staggered-animation'), $('.staggered-animation-container')); 
});
