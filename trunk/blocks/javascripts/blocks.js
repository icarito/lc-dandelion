// jQuery extension

$.fn.extend({
    // positioning helper, returns {left, top, right, bottom}
    box: function(){
        var pos = this.offset();
        return {left: pos.left, 
                top: pos.top, 
                right: pos.left + this.width(), 
                bottom: pos.top + this.height(),
                intersects:function(box2){
                    if (this.left > box2.right) return false;
                    if (this.right < box2.left) return false;
                    if (this.top > box2.bottom) return false;
                    if (this.bottom < box2.top) return false;
                    return true;
                },
                toString: function(){
                    return 'box{left: ' + this.left + ', top: ' + this.top + ', right: ' + this.right + ', bottom: ' + this.bottom + '}';
                }
            };
                
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
    // positioning helper, returns boolean
    intersects: function(other){
        return this.box().intersects(other.box());
    },
    up: function(expr){
        var elem = this;
//        console.log('up from ' + this.info() + ' to ' + expr);
        while(true){
            elem = elem.parent();
//            console.log('up testing ' + elem.info() + ' against ' + expr);
            if (elem.is(expr)){
                return elem;
            }else if(elem.is('body')){
                return $();
            }
        }
    },
    // debug helper
    log: function(str){
        console.log(str);
        return this;
    },
    first: function(){
        return $(this.get(0));
    },
    label: function(){
        var e = $('label', this);
        if (!e.length){
            e = $('label', this.parent());
        }
        return $.trim(e.first().text());
    },
    // debug helper
    info: function(){
        var self = this.get(0);
        return self.nodeName + '#' + self.id + '.' + self.className.split(' ').join('.') + ' (' + this.label() + ')';
    },
    // debug helper
    infoall: function(){
        var output = ['matched ' + this.length + ' elements: '];
        this.each(function(){output.push('\t' + $(this).info())});
        return output.join('\n');
    },
    // debug helper
    loginfo: function(){
        this.log(this.info());
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
            if (self.is('.loop')){
                $('#' + id).draggable({handle: $('.top', self), stop: stop_dragging, refreshPositions: true});
            }else{
                $('#' + id).draggable({stop: stop_dragging, refreshPositions: true});
            }
        });
    }
});


//  Structure of a block
//
//  .drag_wrapper
//      .block (drag handle, if not a loop)
//          .drop_pointer (if not a trigger)
//          label
//          [style holders] (drag handle is in here if a loop)
//          [contained block .drag_wrappers]
//          .drop_target
//      .drag_wrapper for next block(s)
//

function stop_dragging(e, ui){
    console.log('stop dragging helper: ' + ui.helper.info());
    var drop = $.ui.ddmanager.last_droppable;
    if (drop){
        console.log('stop dragging drop: ' + drop.up('.block').info());
    }
    if (drop && drop.intersects($('.drop_pointer', ui.helper))){
        console.log('appending ' + $('.block', ui.helper).info() + ' to ' + drop.up('.block').info());
        ui.helper.css({position: 'relative', left: '0px', top: '0px'});
        drop.up('.drag_wrapper').append(ui.helper);
    }else{
        console.log('appending ' + $('.block', ui.helper).info() + ' to document body');
        $.ui.ddmanager.prepareOffsets(ui.helper, e);
        $(document.body).append(ui.helper);
    }
}

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
    var drop_elem = ui.element.get(0);
    var drag_elem = ui.draggable.get(0);
    console.log('dropped ' + ui.draggable.info() + ' on ' + ui.element.info());
    try{
        ui.element.append(ui.draggable);
    }catch(e){
        console.log('DOM exception when adding ' + ui.element.info() + ' to ' + ui.draggable.info());
    }
    try{
        ui.element.css({position: 'relative', top: '0', left: '0'});
    }catch(e){
        console.log('DOM exception when setting styles');
    }
//    show_structure(document.documentElement, 0);
}

function drag_over(e, ui){
    console.log(ui.draggable.info() + ' is over ' + ui.element.info());
}

function drag_activate(e, ui){
    console.log('activate (' + this.nodeName + ')');
}

function drag_helper(e, ui){
    return this.parentNode;
}

function drop_accept(draggable){
    if (!draggable) return false;
    var val = this.intersects($('.drop_pointer', draggable));
    if (val){
//        console.log(this.info() + ' will accept a drop of ' + draggable.info() + '?');
        this.css('background-color', 'red');
        $.ui.ddmanager.last_droppable = this;
    }else{
        this.css('background-color', 'yellow');
//        $.ui.ddmanager.last_droppable = null;
    }
    return val;
}

// Make this a utility method
function show_structure(e, level){
    e = $(e);
    if (e.is('.block')){
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
    $('.containable').prepend('<div class="drop_pointer"></div>');
    $('.block').append('<div class="drop_target"></div>');
//    $('.trigger').draggable();
//    $('.containable').draggable();
//    $('.block').droppable({accept: '.block, .loop', hoverClass: 'drop_ok', out: drag_out, drop: drag_drop, over: drag_over, tolerance: 'pointer'});
//      $('.containable').mousedown(function(){console.log(this.nodeName);$(this).subsequent().wrapAll('<div></div>').draggable({handle: this});});
//    $('.block').droppable({out: drag_out, drop: drag_drop, over: drag_over, activate: drag_activate});
    // Note, since this keeps tripping me up:
    // there are no callbacks fired unless there is an accept defined.  None.  And, of course, the accept has to match the actual draggable(s)
//    $('.block .drop_target').droppable({over: drag_over, drop: drag_drop, accept: '.drag_wrapper', hoverClass: 'drop_ok'});
    $('.block .drop_target').droppable({over: drag_over, drop: drag_drop, accept: drop_accept, hoverClass: 'drop_ok'});
    
}

$(function(){
    // initialize everything
    add_grouping_classes();
    add_extraneous_elements_for_background_images();
    setup_drag_and_drop();
});
