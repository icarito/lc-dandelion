// jQuery extension

$.fn.extend({
    // positioning helper, returns {left, top, right, bottom}
    box: function(){
        var pos = this.offset();
        return {left: pos.left, top: pos.top, right: pos.left + this.width(), bottom: pos.top + this.height()};
    },
    // positioning helper, returns boolean
    contains: function(other){
        var b1 = this.box();
        var b2 = $(other).box();
        if (b2.left < b1.left) return false;
        if (b2.top < b1.top) return false;
        if (b2.right > b1.right) return false;
        if (b2.bottom > b1.bottom) return false;
        return true;
    },
    // positioning helper, returns intersects
    intersects: function(other){
        var b1 = this.box();
        var b2 = $(other).box();
        if (b2.left > b1.right){ this.log('other is to the right of this'); return false; }
        if (b2.top > b1.bottom){ this.log('other is below this'); return false; }
        if (b2.right < b1.left){ this.log('other is to the left of this'); return false; }
        if (b2.bottom < b1.top){ this.log('other is above this'); return false; }
        this.log('other intersects this');
        return true;
    },
    // debug helper
    log: function(str){
        console.log(str);
        return this;
    },
    // debug helper
    loginfo: function(){
        //debug function
        this.log('matched ' + this.length + ' elements: ');
        this.each(function(){console.log('\t' + this.nodeName + '#' + this.id + '.' + this.className.split().join('.'))});
        return this;
    },
    // blocks method, when a block is removed from its container
    deparent: function(){
        // remove from parent element
        this.each(document.body.appendChild(this));
        return this;
    },
    // block method, when a block is added to a container
    reparent: function(){
        // add to parent element in a specific position. If parent already has a child, it gets inserted as 
        // a child of this element, and an existing child of this element is made the child of that element, and so on.
        // there's got to be a simpler way!
    },
    // utility, add a unique id to each element
    uniqify: function(){
        if (!document.uniq_id_idx){
            document.uniq_id_idx = 1;
        }
        this.each(function(){if (!this.id){this.id = 'id_' + document.uniq_id_idx++}});
        return this;
    },
    // utility, return this node and all siblings that come after it
    subsequent: function(){
        var id = this.get(0).id;
        return $('#' + id + ', #' + id + ' ~ ' + '.block');
    },
    // block method, turn logically structured blocks into visually structured blocks to support drag and drop
    wrap_for_dragging: function(){
        this.each(function(){
            var self = $(this);
            var id = this.id + '_drag_wrapper';
            self.subsequent().wrapAll('<div class="drag_wrapper" id="' + id + '"></div>');
            $('#' + id).draggable({handle: self});
        });
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
    document.body.appendChild(ui.draggable.get(0));
    console.log('out');
}

function drag_drop(e, ui){
    console.log('drop: ' + ui.instance + ', ' + ui.draggable);
    ui.instance.appendChild(ui.draggable);
    ui.draggable.get(0).style.position = 'relative';
    show_structure(document.documentElement, 0);
}

function drag_over(e, ui){
    console.log('over');
}

function drag_activate(e, ui){
    console.log('activate (' + this.length + ')');
}

function drag_helper(e, ui){
    return this.parentNode;
}

function drop_accept(draggable){
    return this.intersects($('.drop_pointer', draggable));
}

// Make this a utility method
function show_structure(e, level){
    e = $(e);
    if (e.is('.trigger,.block,.loop')){
        var output = [];
        for (var i = 0; i < level; i++){
            output.push('    ');
        }
        output.push(e.get(0).className);
        console.log(output.join(''));
    }
    e.children().each(function(){show_structure(this, level + 1);});
}


function add_grouping_classes(){
    $('.step, .trigger, .loop').addClass('block').uniqify();
    $('.step, .loop').addClass('containable');
    $('.loop, .trigger').addClass('container');
}

// make this a block method?
function add_extraneous_elements_for_background_images(){
    $('.loop').prepend(
        '<div class="top_left"></div>' + 
        '<div class="top"></div>' + 
        '<div class="top_right"></div>' + 
        '<div class="left"></div>' + 
        '<div class="bottom_left"></div>' + 
        '<div class="bottom"></div>' + 
        '<div class="bottom_right"></div>'
    );
    $('.step, .trigger').prepend('<div class="right"></div>');
}

function setup_drag_and_drop(){
    $('.block').wrap_for_dragging();
    // elements for drag-and-drop (subject to radical change)
//    $('.containable').prepend('<div class="drop_pointer"></div>');
//    $('.block').append('<div class="drop_target"></div>');
//    $('.trigger').draggable();
//    $('.containable').draggable();
//    $('.block').droppable({accept: '.block, .loop', hoverClass: 'drop_ok', out: drag_out, drop: drag_drop, over: drag_over, tolerance: 'pointer'});
//      $('.containable').mousedown(function(){console.log(this.nodeName);$(this).subsequent().wrapAll('<div></div>').draggable({handle: this});});
}

$(function(){
    // initialize everything
    add_grouping_classes();
    add_extraneous_elements_for_background_images();
    setup_drag_and_drop();
});
