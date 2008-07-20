// jQuery extension
$.extend({
    makeSelect: function(list){
        var sel = ['<select class="blocks_menu">'];
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
        for (var i = 0; i< parts.length; i++){
            part = parts[i];
            if ($.isInteger(part)){
                parts[i] = $('<input type="text" class="int" value="'  + part + '" />');
            }else if (part[0] === '{'){
                parts[i] = application.images[part.slice(1,-1)].clone().css('vertical-align','middle');
            }else if (part == 'true' || part == 'false'){
                parts[i] = $('<input type="text" class="bool" value="' + part + '" />');
            }else if(part == 'bool'){
                parts[i] = $('<input type="text" class="bool" value="" readonly="readonly" />');
            }else if(part == 'int'){
                parts[i] = $('<input type="text" class="int" value="" />');
            }else if(part == 'color'){
                parts[i] = $.colorPicker();
            }else if(part == 'key'){
                parts[i] = $.keyList();
            }else if(part == 'sprite'){
                parts[i] = $.makeSelect(['Sprite 1']);
            }else if(part == 'sound'){
                parts[i] = $.makeSelect(['pop']);
            }else if(part == 'message'){
                parts[i] = $.makeSelect(['Add a new message...']);
            }else if(part == 'costume'){
                parts[i] = $.makeSelect(['Costume 1']);
            }else if(part == 'effect'){
               parts[i] = $.makeSelect(['fisheye']);
            }else if (part[0] == '"'){
                parts[i] = $('<input type="text" class="string_input" value="' + part.slice(1,-1) + '" />'); 
            }else if (part == 'check'){ 
                parts[i] = $('<input type="checkbox" />');
            }else if (part == 'checked'){ 
                parts[i] = $('<input type="checkbox" checked="checked" />');
            }else{ 
                if (part){
                    parts[i] = $('<span>' + part + '</span>');
                }else{
                    parts[i] = null; // no need to wrap empty strings
                }
            }
        }
        return parts;
    }
});

// jQuery result set extend
$.fn.extend({
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
    // drag-and-drop helper to find the element to match intersections with
    // Either .drop_pointer or .block (wrapped or not)
    intersection_shape: function(){
        if (this.is('.expression')){
            //console.log('intersection of an expression: ' + this.info());
            return this; // it is an expression
        }
        var shape = this.find('.drop_pointer');
        if (shape.length > 0){
            //console.log('intersection of a wrapped droppable: ' + this.info());
            return shape; // it is a wrapped droppable
        }
        //console.log('intersection of a wrapped Trigger: ' + this.info());
        return this.find('.block'); // it is wrapped, but not droppable (a Trigger, for instance)
    },
    block: function(){
        if (this.is('.block') || this.is('.expression')){
            return this;
        }
        return this.find('.block');
    }
});

var triggers = [];

function Block(){
}

Block.prototype.blocktype = function(){
    return this.constructor.name;
}

Block.prototype.clone = function(){
    // This is very experimental and a work in progress!
    return new this.constructor(this.initial_params);
}

Block.prototype.label = function(str){
    if (str){
        var label_elements = $.parseSpec(str);
        for (var i = 0; i < label_elements.length; i++){
            if (label_elements[i]){ // don't try to append nulls
                try{
                    this._label.append(label_elements[i]);
                }catch(e){
                    console.log('problem adding element ' + label_elements[i].get(0).nodeName + ' to block label');
                }
            }
        }
        return this;
    }else{
        return this._label.text();
    }
}

Block.prototype.toString = function(){
    return this.blocktype() + '(' + this.label() + ')';
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

Block.prototype.make_draggable_factory = function(){
    var factory = this;
    var get_helper = function(){
        if (!factory.current_helper){
            factory.current_helper = factory.drag_wrapper.clone(true);
            $(document.body).append(factory.current_helper);
        }
        return factory.current_helper;
    };
    var drag_fun = function(e, ui){
        
    };
    var start_fun = function(e, ui){
    };
    var stop_fun = function(e, ui){
        stop_dragging_factory(e, ui, factory);
        if (factory.current_helper){
            factory.current_helper.hide();
        }
    };
    this.drag_wrapper.draggable({start: start_fun, drag: drag_fun, helper: get_helper, handle: this.handle, stop: stop_fun, refreshPositions: true});
    return this;
}

Block.prototype.make_draggable_instance = function(){
    var factory = this;
    var start_fun = function(e, ui){
    };
    var stop_fun = function(e, ui){
        stop_dragging_instance(e, ui, factory);
    }
    this.drag_wrapper.draggable({start: start_fun, handle: this.handle, stop: stop_fun, refresh_positions: true});
}

Block.prototype.make_draggable = function(){
    if (this.isInstance){
        this.make_draggable_instance();
    }else{
        this.make_draggable_factory();
    }
}

Block.prototype.make_containable = function(){
    this.block.prepend($('<div class="drop_pointer"></div>'));
}

Block._last_uniq = 0;

Block.prototype.uniq = function(){
    if (! this._uniq){
        Block._last_uniq++;
        this._uniq = Block._last_uniq;
    }
    return this._uniq;
};

Block.prototype.block_init = function(params){
    // all blocks inherit this
    this.initial_params = params;
    this.isInstance = params.instance || false;
    this.initial_params.instance = true;
    this.register();
};

Block.blocks = [];

Block.prototype.register = function(){
    Block.blocks.push(this);
};

Block.prototype.dom_init = function(params){
    //customize for each type of block
};

Block.prototype.init = function(params){
};

Block.prototype.initialize = function(params){
    // Block-level initialialization, all blocks
    //console.log('name: ' + this.constructor.name);
    this.block_init(params); // block-level, do not over-ride
    this.block_dom_init(params); // DOM initialization to own method
    /// 3. Move DOM properties to jq_propertyname for code clarity
    // Individual initialiation, over-ride for each type of block
    this.init(params); // class-specific initialization, customize for each class
    this.dom_init(params);
    this.make_draggable();
    this.make_droppable();
};

Block.prototype.block_dom_init = function(params){
    // all blocks inherit this, except Expressions
    this.next = null;
    this.block = $('<div class="block"></div>');
    this.block.attr('id', 'id_' + this.uniq());
    this._label = $('<span class="label"></span>');
    this.block.append(this._label);
    this.block.addClass(params.color);
    this.block.addClass(this.blocktype().toLowerCase());
    this.drag_handle = this.block;
    this.make_nestable();
    if (params.x && params.y){
        this.position(params.x, params.y);
    }
    if (params.label){
        this.label(params.label);
    }
};

Block.prototype.make_nestable = function(params){
    this.drag_wrapper = $('<div class="drag_wrapper"></div>');
    var width = this.block.css('width');
    var left = this.block.css('left');
    var top = this.block.css('top');
    this.drag_wrapper.css({position: 'absolute', width: width, left: left, top: top});
    this.drag_wrapper.append(this.block);
};

Block.prototype.make_droppable = function(){
    this.drop_target = $('<div class="drop_target"></div>');
    this.block.append(this.drop_target);
    this.drop_target.droppable({accept: drop_accept});
};

function Expression(){
}
Expression.prototype = new Block();

Expression.expressions = [];
Expression.prototype.register = function(){
    Expression.expressions.push(this);
};

Expression.prototype.init = function(params){
    this.block.addClass('expression').removeClass('block');
}

Expression.prototype.dom_init = function(params){
    this.block.prepend('<div class="right"></div>');
}

Expression.prototype.make_nestable = function(params){
    this.drag_wrapper = this.block;
};

function Step(params){
    this.initialize(params);
    this.make_containable();
}
Step.prototype = new Block();
Step.prototype.constructor = Step;

Step.prototype.dom_init = function(params){
    this.block.addClass('step containable');
    this.block.prepend('<div class="right"></div>');
};

function IntExpr(params){
    this.initialize(params);
}
IntExpr.prototype = new Expression();
IntExpr.prototype.constructor = IntExpr;

function IntValue(params){
    this.initialize(params);
}
IntValue.prototype = new Expression();
IntValue.prototype.constructor = IntValue;

IntValue.prototype.dom_init = function(params){
    this.block.prepend('<div class="right"></div>');
    this.block.css('margin-left', '20px');
    this._checkbox = $('<input type="checkbox" />');
    this.block.prepend(this._checkbox);
    this._checkbox.css({position: 'absolute', top: '3px', left: '-20px'});
}

function BoolExpr(params){
    this.initialize(params);
}
BoolExpr.prototype = new Expression();
BoolExpr.prototype.constructor = BoolExpr;

function BoolValue(params){
    this.initialize(params);
    this.block.css('margin-left', '20px');
    this._checkbox = $('<input type="checkbox" />');
    this.block.prepend(this._checkbox);
    this._checkbox.css({position: 'absolute', top: '3px', left: '-20px'});
}
BoolValue.prototype = new Expression();
BoolValue.prototype.constructor = BoolValue;

function Trigger(params){
    this.initialize(params);
    this.block.addClass('trigger container');
    this.block.prepend('<div class="right"></div>');
    triggers.push(this);
}
Trigger.prototype = new Block();
Trigger.prototype.constructor = Trigger;

function Loop(params){
    this.initialize(params);
    this.next_in_loop = null;
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
    this.make_containable();
}
Loop.prototype = new Block();
Loop.prototype.constructor = Loop;

Loop.prototype.appendLoop = function(block){
    if (this.next_in_loop){
        try{
            this.next_in_loop.append(block);
        }catch(e){
            console.log('Here I am, trying to append a simple block: ' + e.message);
            console.log('next in loop: ' + this.next_in_loop.toString());
            console.log('appending block: ' + block.toString());
        }
    }else{
        this.block.append(block.drag_wrapper);
        this.next_in_loop = block;
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

function stop_dragging_factory(e, ui, factory){
    //console.log('stop dragging factory: ' + factory.constructor.name);
    //console.log('stop dragging factory helper: ' + ui.helper.block().info());
    //console.log(ui.helper);
    var drop = $.ui.ddmanager.last_droppable;
    if (drop){
        //console.log('stop dragging drop: ' + drop.up('.block').info());
    }
    if (drop && drop.intersects($('.drop_pointer', ui.helper))){
        //console.log('appending ' + $('.block', ui.helper).info() + ' to ' + drop.up('.block').info());
        ui.helper.css({position: 'relative', left: '0px', top: '0px'});
        drop.up('.drag_wrapper').append(ui.helper);
    }else{
        var script_canvas = $('#scripts_container');
        if (script_canvas.intersects(ui.helper.intersection_shape())){
            //console.log('appending ' + ui.helper.block().info() + ' to script block body');
            var offset = script_canvas.offset();
            //console.log('script canvas offset: ' + offset.left + ', ' + offset.top);
            var instance = factory.clone();
//            console.log(instance);
            var x = parseInt(ui.helper.css('left')) - offset.left;
            var y = parseInt(ui.helper.css('top')) - offset.top;
            //console.log('new block: ' + x + ', ' + y);
            instance.drag_wrapper.css({left: x, top: y});
            script_canvas.append(instance.drag_wrapper);
        }else{
            console.log('no match for dragging: ' + factory.drag_wrapper.info());
        }
    }
}

function stop_dragging_instance(e, ui, instance){
//    console.log('stop dragging helper: ' + ui.helper.info());
    var script_canvas = $('#scripts_container');
    if (! script_canvas.intersects(ui.helper.intersection_shape())){
        console.log('outside of canvas, delete');
        instance.remove();
    }
    var drop = $.ui.ddmanager.last_droppable;
    if (drop && drop.intersects($('.drop_pointer', ui.helper))){
        console.log('appending ' + $('.block', ui.helper).info() + ' to ' + drop.up('.block').info());
        ui.helper.css({position: 'relative', left: '0px', top: '0px'});
        drop.up('.drag_wrapper').append(ui.helper);
    }else{
        console.log('positioning in canvas (remove from parent?)');
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

