var amountScrolled = 600;
$(window).scroll(function() {
    location.pathname.replace(/^\//, '')
    if ($(window).scrollTop() > amountScrolled) {
        $('a.back-to-top').fadeIn('slow');
    } else {
        $('a.back-to-top').fadeOut('slow');
    }
});
