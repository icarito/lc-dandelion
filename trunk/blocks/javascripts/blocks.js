// jQuery extension
$.extend({
    sum: function(list_of_numbers){
        var value = 0;
        jQuery.each(list_of_numbers, function(){value += this});
        return value;
    },
    max: function(list_of_numbers){
        var value = 0;
        jQuery.each(list_of_numbers, function(){ if (this > value) value = this; });
        return value;
    },
    keys: function(obj){
        var k = [];
        for (key in obj){
            k.push(key);
        }
        return '[' + k.join(', ') + ']';
    }
});

// jQuery result set extend
$.fn.extend({
    // set or return position
    position: function(pos){
        if (pos){
            this.css({position: 'absolute', left: pos.left + 'px', top: pos.top + 'px'});
        }else{
            return this.offset();
        }
    },
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
    // go up the ancestor tree until an element matching expr is found
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
    // utility returning jQuery object containing only first matched element
    first: function(){
        return this.eq(0);
    },
    // blocks-specific function, return value of the block label (should be moved to block method)
    label: function(str){
        var e = $('label', this);
        if (str){
            e.text(str);
        }
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
            self.subsequent().wrapAll('<div class="drag_wrapper" id="' + id + '"></div>'); // moved to Loop ctor
            var handle = this;
            if (self.is('.loop')){
                handle = $('.top', self); // moved to Loop ctor
            }
                drag_wrapper.draggable({handle: $('.top', self), stop: stop_dragging, refreshPositions: true}); // moved to Block method
        });
    },
    // Add methods to elements, OO-style
    methods: function(obj){
        this.each($.extend(this, obj));
    }
});

var blocks = [];
var triggers = [];


function Block(){
    this.block = $('<div class="block"></div>');
    this.block.attr('id', 'id_' + $.data(this.block.get(0)));
    this.drag_wrapper = $('<div class="drag_wrapper"></div>');
    this.drag_wrapper.append(this.block);
    this.block.prepend($('<div class="drop_pointer"></div>'));
    this._label = $('<label></label>');
    this.drop_target = $('<div class="drop_target"></div>');
    this.block.append(this.drop_target);
    this.drag_handle = this;
    this.drop_target.droppable({over: drag_over, drop: drag_drop, accept: drop_accept, hoverClass: 'drop_ok'});
    blocks.push(this);
}

Block.prototype.label = function(str){
    if (str){
        this._label.text(str);
        return this;
    }else{
        return this._label.text();
    }
}

Block.prototype.position = function(x,y){
    this.drag_wrapper.css({position: 'absolute', left: x + 'px', top: y + 'px'});
    return this;
}

Block.prototype.relativize = function(){
    this.drag_wrapper.css({position: 'relative', left: '0px', top: '0px'});
    return this;
}

Block.prototype.append = function(block){
    if (this.next){
        this.next.drag_wrapper.before(block.drag_wrapper);
        block.append(this.next); // move current next to next of the block for drag purposes
    }else{
        this.drag_wrapper.append(block.drag_wrapper);
    }
    this.next = block;
    return this;
}

Block.prototype.makeDraggable = function(){
    this.drag_wrapper.draggable({handle: this.handle, stop: stop_dragging, refreshPositions: true});
    return this;
}

function Step(params){
    this.prototype = new Block(params);
    this.block.addClass('step containable');
    this.block.prepend('<div class="right"></div>');
}
Step.prototype = new Block();

function Trigger(params){
    this.block.addClass('trigger container');
    this.block.prepend('<div class="right"></div>');
    triggers.push(this);
}
Trigger.prototype = new Block();

function Loop(params){
    this.block.addClass('loop container containable');
    this.block.prepend('<div class="top_left"></div>' + 
        '<div class="top_right"></div>' + 
        '<div class="left"></div>' + 
        '<div class="bottom_left"></div>' + 
        '<div class="bottom"></div>' + 
        '<div class="bottom_right"></div>'
    );    
    this.handle = $('<div class="top"></div>');
    this.block.prepend(this.handle);
}
Loop.prototype = new Block();

Loop.prototype.appendLoop = function(block){
    if (this.nextInLoop){
        this.block.insertBefore(block.drag_wrapper, this.nextInLoop.drag_wrapper);
        block.append(this.nextInLoop); // move current next to next of the block for drag purposes
    }else{
        this.block.append(block.drag_wrapper);
    }
    this.nextInLoop = block;
}


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
    // all moved to block ctors
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
    // all moved to block ctors
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

function new_initialize(){
    var trigger = new Trigger().label('On event');
    $(document.body).append(trigger.drag_wrapper);
    var loop = new Loop().label('Forever');
    trigger.append(loop);
    loop.appendLoop(new Step().label('Step one'));
    loop.appendLoop(new Step().label('Step two'));
    loop.appendLoop(new Step().label('Step three'));
}

$(function(){
    // initialize everything
//    add_grouping_classes();
//    add_extraneous_elements_for_background_images();
//    setup_drag_and_drop();
    new_initialize();
});
