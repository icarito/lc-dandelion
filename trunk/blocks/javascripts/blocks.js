// jQuery extension

$.fn.extend({
    box: function(){
        var pos = this.offset();
        return {left: pos.left, top: pos.top, right: pos.left + this.width(), bottom: pos.top + this.height()};
    },
    contains: function(other){
        var b1 = this.box();
        var b2 = $(other).box();
        if (b2.left < b1.left) return false;
        if (b2.top < b1.top) return false;
        if (b2.right > b1.right) return false;
        if (b2.bottom > b1.bottom) return false;
        return true;
    },
    intersects: function(other){
        var b1 = this.box();
        var b2 = $(other).box();
        if (b2.left > b1.right) return false;
        if (b2.top > b1.bottom) return false;
        if (b2.right < b1.left) return false;
        if (b2.bottom < b1.top) return false;
        return true;
    }
});

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

function drop_accept(draggable){
    this.each(function(){ return this.intersects($('.drop_pointer', draggable))});
    return this;
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
    $('.block, .container').draggable();
//    $('.block, .trigger, .container').draggable({helper: drag_helper});
//    $('.drop_target').droppable({activate: drag_activate});
    $('.drop_target').droppable({accept: drop_accept, hoverClass: 'drop_ok', out: drag_out, drop: drag_drop, over: drag_over});
}

$(add_extraneous_elements);
