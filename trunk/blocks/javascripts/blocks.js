function drag_out(e, ui){
    // ui.instance = droppable
    // ui.options 
    // ui.position
    // ui.absolute_position
    // ui.draggable
    // ui.helper
    
    // use to disconnect blocks
    console.log('out');
}

function drag_drop(e, ui){
    console.log('drop');
}

function drag_over(e, ui){
    console.log('over');
}

function drag_activate(e, ui){
    console.log('activate');
}

function drag_helper(e, ui){
    return this.parentNode;
}


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
    $('.block, .trigger').prepend('<div class="right"></div>');
    $('.block, .container').prepend('<div class="drop_pointer"></div>');
    $('.block, .container, .trigger').append('<div class="drop_target"></div>');
//    $('.trigger').draggable();
    $('.drop_pointer').draggable({handle: this.parentNode});
//    $('.block, .trigger, .container').draggable({helper: drag_helper});
//    $('.drop_target').droppable({activate: drag_activate});
    $('.drop_target').droppable({accept: '.drop_pointer', hoverClass: 'drop_ok', out: drag_out, drop: drag_drop, over: drag_over});
}

$(add_extraneous_elements);
