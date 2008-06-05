// jQuery extension
$.extend({
    contains: function(obj, array){
        var i;
        var len = array.length;
        for (i = 0; i < len; i++){
            if (array[i] === obj) return true;
        }
        return false;
    },
    isInteger: function(str){
        return (str.toString().search(/^-?[0-9]+$/) == 0);
    },
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
    },
    upcap: function(str){
        return str[0].toUpperCase() + str.slice(1);
    },
    makeSelect: function(list){
        var sel = ['<select>'];
        $.each(list, function(){
            sel.push('<option value="' + this + '">' + this + '</option>');
        });
        sel.push('</select>');
        return $(sel.join(''));
    },
    keyList: function(str){
        var keys = ['up arrow', 'down arrow', 'right arrow', 'left arrow', 'space'].concat('abcdefghijklmnopqrstuvwxyz0123456789'.split(''));
        return $.makeSelect(keys);
    },
    colorPicker: function(str){
        return $('<span></span>').addClass('color_picker').css({backgroundColor: 'green', border: '1px solid black'}).click(function(){alert('show color picker')});
    },
    parseSpec: function(str){
        // Handle label strings with embedded content notation
        // [] is used for element content
        // [#] where # is some numeral: create an IntExpr hole with a default value of #
        // [{flag}] double brackets insert a named graphic
        // [true] or [false]: create a BoolExpr hold with a default value
        // [int]: create an IntExpr hole with no default value
        // [bool]: create a BoolExpr hole with no default value
        // [color]: create a color picker control
        // [key]: create a keypress drop-down list
        // [sprite]: create a list of sprites (besides the current sprite)
        // [sound]: create a list of available sounds (default + added)
        // [check]: make a checkbox, [checked] make a checkbox that defaults to selected
        // ["Hello"] or ["Hmm..."]: make a string control from quoted content (type "string")
        // [message] add a list of available messages
        // [costume] adds a list available costumes
        // [effect] list of graphic effects
        // the remaining content of the label is type "text"
        var parts = str.split(/\]|\[/g);
        var part = null;
        console.log('parseSpec found ' + parts.length + ' parts: "' + parts.join(", ") + '"');
        for (var i = 0; i< parts.length; i++){
            part = parts[i];
            if ($.isInteger(part)){
                console.log(part + ' is an integer');
                parts[i] = $('<input type="text" class="int" value="'  + part + '" />');
            }else if (part[0] === '{'){
                console.log(part + ' is an image');
                parts[i] = application.images[part.slice(1,-1)];
            }else if (part == 'true' || part == 'false'){
                console.log(part + ' is a boolean');
                parts[i] = $('<input type="text" class="bool" value="' + part + '" />');
            }else if(part == 'bool'){
                console.log(part + ' is a boolean');
                parts[i] = $('<input type="text" class="bool" value="" />');
            }else if(part == 'int'){
                console.log(part + ' is an integer');
                parts[i] = $('<input type="text" class="int" value="" />');
            }else if(part == 'color'){
                console.log(part + ' is a color');
                parts[i] = $.colorPicker();
            }else if(part == 'key'){
                console.log(part + ' is a key');
                parts[i] = $.keyList();
            }else if(part == 'sprite'){
                console.log(part + ' is a sprite');
                parts[i] = $.makeSelect(['Sprite 1']);
            }else if(part == 'sound'){
                console.log(part + ' is a sound');
                parts[i] = $.makeSelect(['pop']);
            }else if(part == 'message'){
                console.log(part + ' is a message');
                parts[i] = $.makeSelect(['Add a new message...']);
            }else if(part == 'costume'){
                console.log(part + ' is a costume');
                parts[i] = $.makeSelect(['Costume 1']);
            }else if(part == 'effect'){
                console.log(part + ' is an effect');
               parts[i] = $.makeSelect(['fisheye']);
            }else if (part[0] == '"'){
                console.log(part + ' is a string');
                parts[i] = $('<input type="text" class="string_input" value="' + part.slice(1,-1) + '" />'); 
            }else if (part == 'check'){ 
                console.log(part + ' is a checkbox');
                parts[i] = $('<input type="checkbox" />');
            }else if (part == 'checked'){ 
                console.log(part + ' is a checkbox');
                parts[i] = $('<input type="checkbox" checked="checked" />');
            }else{ 
                console.log(part + ' is a run of text');
                parts[i] = $('<span>' + part + '</span>');
            }
        }
        console.log('parseSpec built ' + parts.length + ' parts: "' + $.map(parts, function(e){return e.get(0).nodeName}).join(", ") + '"');
        return parts;
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
        var e = $('.label', this);
        if (str){
            e.text(str);
        }
        if (!e.length){
            e = $('.label', this.parent());
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
    // Add methods to elements, OO-style (expando version)
    methods: function(obj){
        this.each(function(){
            $.extend(this, obj);
        });
    },
});

var blocks = [];
var triggers = [];
var expressions = [];

function Block(){
}

Block.prototype.initialize = function(params){
    this.block = $('<div class="block"></div>');
    this.next = null;
    this.block.attr('id', 'id_' + $.data(this.block.get(0)));
    this.drag_wrapper = $('<div class="drag_wrapper"></div>');
    this.drag_wrapper.append(this.block);
    this._label = $('<span class="label"></span>');
    this.block.append(this._label);
    this.block.addClass(params.color);
    this.drag_handle = this.block;
    if (params.x && params.y){
        this.position(params.x, params.y);
    }
    if (params.label){
        this.label(params.label);
    }
    this.drop_target = $('<div class="drop_target"></div>');
    this.block.append(this.drop_target);
    this.drop_target.droppable({accept: drop_accept});
    blocks.push(this);
}

Block.prototype.label = function(str){
    if (str){
//        this._label remove children ???
//        this._label.text($.parseSpec(str));
//        try{
//            console.log('spec: "' + str + '" parsed becomes: ' + $.parseSpec(str));
//        }catch(e){
//            console.log('parseSpec failed for ' + str + ' with error ' + e.description);
//        }
        var label_elements = $.parseSpec(str);
        for (var i = 0; i < label_elements.length; i++){
            try{
                this._label.append(label_elements[i]);
            }catch(e){
                console.log('problem adding element ' + label_elements[i].get(0).nodeName + ' to block label');
            }
        }
//        this._label.text(str);
        return this;
    }else{
        return this._label.text();
    }
}

Block.prototype.toString = function(){
    return this.type + '(' + this.label() + ')';
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
        this.next.append(block);
    }else{
        this.drag_wrapper.append(block.drag_wrapper);
        this.next = block;
    }
    return this;
}

Block.prototype.makeDraggable = function(){
    this.drag_wrapper.draggable({handle: this.handle, stop: stop_dragging, refreshPositions: true});
    return this;
}

Block.prototype.makeContainable = function(){
    this.block.prepend($('<div class="drop_pointer"></div>'));
}

function Expression(){
}
Expression.prototype = new Block();

Expression.prototype.initialize = function(params){
    this.block = $('<div class="expression"></div>');
    this.block.attr('id', 'id_' + $.data(this.block.get(0)));
    this._label = $('<label></label>');
    this.block.append(this._label);
    this.block.prepend('<div class="right"></div>');
    this.block.addClass(params.color);
    this.drag_handle = this.block;
    this.drag_wrapper = this.block;
    if (params.x && params.y){
        this.position(params.x, params.y);
    }
    if (params.label){
        this.label(params.label);
    }
    this.makeDraggable();
    expressions.push(this);
}

function Step(params){
    this.initialize(params);
    this.type = 'Step';
    this.block.addClass('step containable');
    this.block.prepend('<div class="right"></div>');
    this.makeContainable();
    this.makeDraggable();
}
Step.prototype = new Block();

function IntExpr(params){
    this.initialize(params);
    this.type = 'IntExpr';
    this.block.addClass('intexpr');
}
IntExpr.prototype = new Expression();

function IntValue(params){
    this.initialize(params);
    this.block.addClass('intexpr');
    this.block.css('margin-left', '20px');
    this.type = 'IntValue';
    this._checkbox = $('<input type="checkbox" />');
    this.block.prepend(this._checkbox);
    this._checkbox.css({position: 'absolute', top: '3px', left: '-20px'});
}
IntValue.prototype = new Expression();

function BoolExpr(params){
    this.initialize(params);
    this.type = 'BoolExpr';
    this.block.addClass('boolexpr');
}
BoolExpr.prototype = new Expression();

function BoolValue(params){
    this.initialize(params);
    this.block.addClass('boolexpr');
    this.block.css('margin-left', '20px');
    this.type = 'BoolValue';
    this._checkbox = $('<input type="checkbox" />');
    this.block.prepend(this._checkbox);
    this._checkbox.css({position: 'absolute', top: '3px', left: '-20px'});
}
BoolValue.prototype = new Expression();

function Trigger(params){
    this.initialize(params);
    this.type = 'Trigger';
    this.block.addClass('trigger container');
    this.block.prepend('<div class="right"></div>');
    triggers.push(this);
    this.makeDraggable();
}
Trigger.prototype = new Block();

function Loop(params){
    this.initialize(params);
    this.type = 'Loop';
    this.nextInLoop = null;
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
    this.makeContainable();
    this.makeDraggable();
}
Loop.prototype = new Block();

Loop.prototype.appendLoop = function(block){
    if (this.nextInLoop){
        try{
            this.nextInLoop.append(block);
        }catch(e){
            console.log('Here I am, trying to append a simple block: ' + e.message);
            console.log('next in loop: ' + this.nextInLoop.toString());
            console.log('appending block: ' + block.toString());
        }
    }else{
        this.block.append(block.drag_wrapper);
        this.nextInLoop = block;
        //console.log('setting next in loop: ' + block.toString());
    }
    return this;
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
//    console.log('stop dragging helper: ' + ui.helper.info());
    var drop = $.ui.ddmanager.last_droppable;
    if (drop){
        console.log('stop dragging drop: ' + drop.up('.block').info());
    }
    if (drop && drop.intersects($('.drop_pointer', ui.helper))){
//        console.log('appending ' + $('.block', ui.helper).info() + ' to ' + drop.up('.block').info());
        ui.helper.css({position: 'relative', left: '0px', top: '0px'});
        drop.up('.drag_wrapper').append(ui.helper);
    }else{
        console.log('appending ' + $('.block', ui.helper).info() + ' to document body');
    //    $.ui.ddmanager.prepareOffsets(ui.helper, e);
        $(document.body).append(ui.helper);
    }
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
//    console.log(ui.draggable.info() + ' is over ' + ui.element.info());
    this.css('background-color', 'red');
}

function drag_out(e, ui){
//    console.log('out');
    this.css('background-color', 'transparent');
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
        this.css('background-color', 'transparent');
        $.ui.ddmanager.last_droppable = null;
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

function initialize_test(){
    var trigger = new Trigger({label: 'On event', color: 'gold'});
    $(document.body).append(trigger.drag_wrapper);
    var loop = new Loop({label: 'Forever', color: 'blueviolet'});
    trigger.append(loop);
    loop.appendLoop(new Step({label: 'Step one', color: 'lawngreen'}));
    loop.appendLoop(new Step({label: 'Step two', color: 'magenta'}));
    var loop2 = new Loop({label: 'While true', color: 'orangered'});
    loop.appendLoop(loop2);
    loop2.appendLoop(new Step({label: 'Step A', color: 'blue'}));
    loop2.appendLoop(new Step({label: 'Step B', color: 'cyan'}));
    loop.appendLoop(new Step({label: 'Step three', color: 'seagreen'}));
    trigger.append(new Step({label: 'Step i', color: 'green'}));
    trigger.append(new Step({label: 'Step ii', color: 'mediumblue'}));
}

