function add_extraneous_elements(){
    $('.container').prepend(
        '<div class="top_left"></div>' + 
        '<div class="top"></div>' + 
        '<div class="top_right"></div>' + 
        '<div class="left"></div>' + 
        '<div class="bottom_left"></div>' + 
        '<div class="bottom"></div>' + 
        '<div class="bottom_right"></div>'
    );
    $('.block').prepend('<div class="right"></div>');
    $('.trigger').prepend('<div class="right"></div>');
}

$(add_extraneous_elements);
