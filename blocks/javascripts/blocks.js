/**
 * Blocks Utilities 0.1 (http://livingcode.org/blocks)
 * Copyright (c) 2008-2009 Dethe Elza (http://livingcode.org/)
 * 
 * Licensed under the MIT (MIT-LICENSE.txt)
 *
 */
 
 /**
 * @fileOverview Functionality of the blocks themselves
 * @name blocks
 * @author Dethe Elza
 */
var DEBUG = true;

/**
 * @class
 * @name BlockUtil
 * @description BlockUtil is a documentation alias for jQuery methods which are used by the blocks objects
 */
$.extend(/** @lends BlockUtil */{
    /**
     * @static
     * @description creates a select control, using list for the contents of the control, returns the select
     * @returns jQuery
     */ 
    makeSelect: function(list){
        var sel = ['<select class="blocks_menu">'];
        $.each(list, function(idx){
            if (idx == 0){
                sel.push('<option value="' + this + '" selected="selected">' + this + '</option>');
            }else{
                sel.push('<option value="' + this + '">' + this + '</option>');
            }
        });
        sel.push('</select>');
        return $(sel.join(''));
    },
    /**
     * @description creates and returns a select element for the various keys
     * @returns jQuery
     */ 
    keyList: function(str){
        var keys = ['up arrow', 'down arrow', 'right arrow', 'left arrow', 'space', 'caps lock', 'delete', 'tab', 'control', 'shift', 'enter', 'option', 'function'].concat(',./\\\'-=`abcdefghijklmnopqrstuvwxyz0123456789'.split(''));
        return $.makeSelect(keys);
    },
    /**
     * @description creates and returns a colour picker [Placeholder, not implemented yet]
     * @returns jQuery
     */
    colorPicker: function(str){
        return $('<span></span>').addClass('color_picker').css({backgroundColor: 'green', border: '1px solid black'}).click(function(){alert('show color picker')});
    },
    /**
     * @description parses the spec for a block label and returns the parts, including embedded expression slots
     * @returns jQuery
     */
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
$.fn.extend(/** @lends BlockUtil.prototype */{

    // blocks-specific function, return value of the block label (should be moved to block method)
    /**
     * @description parses the spec for a block label and returns the parts, including embedded expression slots
     * @returns jQuery
     */
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
    /**
     * @description drag-and-drop helper to find the element to match intersections with either .drop_pointer or .block (wrapped or not)
     * @returns jQuery
     */
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
    /**
     * @description finds the block wrapper within an element
     * @returns jQuery
     */
    block: function(){
        if (this.is('.block') || this.is('.expression')){
            return this;
        }
        return this.find('.block');
    },
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

/**
 * @class
 * @name Block
 */
function Block(){
}

/**
 * @returns String
 */
Block.prototype.blocktype = function(){
    return this.constructor.name;
}

/**
 * @returns Block
 */
Block.prototype.clone = function(){
    // This is very experimental and a work in progress!
    var instance = new this.constructor(this.initial_params);
    instance.drag_wrapper.css('left', this.current_helper.css('left'));
    instance.drag_wrapper.css('top', this.current_helper.css('top'));
    if (! instance instanceof Expression){
        instance.drag_wrapper.width(this.current_helper.width());
    }
    return instance;
}

/**
 * @param {String} [str] label string is optional
 * @description if str param is given, sets the label value and returns block, otherwise returns text of the block's label
 * @returns {Block|String} depending on presence of str param
 */
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

/**
 * @description Returns string representation of block: blocktype and label
 * @returns {String} 
 */
Block.prototype.toString = function(){
    return this.blocktype() + '(' + this.label() + ')';
}

/**
 * @param {Number} x horizontal coordinate
 * @param {Number} y vertical coordinate
 * @description Sets the position of the block by it's top left corner
 * @returns {Block}
 */
Block.prototype.position = function(x,y){
        this.drag_wrapper.css({position: 'absolute', left: x + 'px', top: y + 'px'});
    return this;
};

/**
 * @param {Block} block
 * @description Adds a block to this block, as the next in a sequence
 * @returns {Block}
 */
Block.prototype.append = function(block){
//    this.drag_wrapper.css('border', '1px solid red');
//    $.print('trying to append ' + block + ' to ' + this);
    if (this == block) return;
    block.drag_wrapper.css({left: 0, top: 0, position: 'relative'});
    if (this.next){
        block.append(this.next);
    }
    this.drag_wrapper.append(block.drag_wrapper);
    block.drag_parent = this;
    this.next = block;
    return this;
};

/**
 * @description Gets the current position of the block on the page and places it as a child of the script canvas element, with offsets adjusted to appear in the same location
 * @returns {Block}
 */
Block.prototype.moveToScriptCanvas = function(){
    var canvas = $('#scripts_container');
    var elem = this.drag_wrapper;
    var off = elem.offset();
    var coff = canvas.offset();
    canvas.append(elem);
    elem.css({position: 'absolute', left: off.left - coff.left, top: off.top - coff.top});
    return this;
}

/**
 * @param {Block} other
 * @description Tests to see if the either blocks' drop pointer interesects the other's drop target. Highlights the drop target if so, and returns true, otherwise returns false.
 * @returns {Boolean}
 */
Block.prototype.test_snapping = function(other){
    if (this.drop_intersects(other)){
        this.highlight_drop_pointer(true, other);
        return true;
    }else if(other.drop_intersects(this)){
        other.highlight_drop_pointer(true, this);
        return true;
    }else{
        other.highlight_drop_target(false, other);
        return false;
    }
};

/**
 * @description At the beginning of a drag, clear drag_parent and drag_parent.next, set cancelHelperRemoval to true (why?)
 * @returns {null}
 */
Block.prototype.ondragstart = function(){
    $.ui.ddmanager.current.cancelHelperRemoval = true;
    if (this.drag_parent){
        this.drag_parent.next = null;
        this.drag_parent = null;
    }
}

/**
 * @description during a drag, test to see if this block should snap to any other block.
 * @returns {null}
 */
Block.prototype.ondrag = function(){
    var self = this;
    if (!Block.blocks.length) return;
    var matched = false
    $.each(Block.blocks, function(idx, block){
        matched = self.test_snapping(block);
        if (matched){
            self.snap_target = block;
            return false // stop the iteration
        }
    });
    if (!matched){
        self.highlight_drop_target(false, self);
    }
};

/**
 * @description At the end of a drag, if we are outside script canvas, remove block. Otherwise, if block is a factory, put new block into position in script canvas. If block is passes the snapping test, snap it with other block.  If already snapped to another block, but it fails snapping test, unsnap.
 * @returns {null}
 */
Block.prototype.ondragend = function(){
    var script_canvas = $('#scripts_container');
    // Check to see if we're in the script canvas at all
    if (!(this.snap_target || script_canvas.intersects(this.get_helper().intersection_shape()))){
        return;
    }
    this.highlight_drop_pointer(false, this);
    if (this.snap_target){
        this.snap_target.highlight_drop_pointer(false, this.snap_target);
    }
    var instance = this;
    if (!this.isInstance){
        instance = this.clone();
    }
    if (!this.isInstance){ // reposition if factory
        script_canvas.append(instance.drag_wrapper);
        instance.drag_wrapper.repositionInFrame(script_canvas);
    }else{
        if(this.drag_parent){
            instance.moveToScriptCanvas();
        }
    }
    if (this.snap_target){
        if (instance.drop_intersects(this.snap_target)){
            this.snap_target.append(instance);
        }else if(this.snap_target.drop_intersects(instance)){
            instance.append(this.snap_target);
        }
    }
    if (!this.isInstance && this.current_helper){
        this.current_helper.hide();
    }
    $.ui.ddmanager.current.cancelHelperRemoval = true;
}



/**
 * @description Returns the drag_wrapper element, wrapped in jQuery.  If block is a factory, create a new drag_helper to drag.
 * @returns {jQuery} drag_wrapper
 */
Block.prototype.get_helper = function(){
    if (this.isInstance){
        return this.drag_wrapper;
    }else{
        if (!this.current_helper){
            this.current_helper = this.drag_wrapper.clone(true);
            this.drop_target = this.current_helper.find('.drop_target');
            this.drop_pointer = this.current_helper.find('.drop_pointer');
        }else{
            this.current_helper.css('display', 'block');
        }
        $(document.body).append(this.current_helper);
        return this.current_helper;
    }
};

/**
 * @description Set up handlers for dragging
 * @returns {Block}
 */
Block.prototype.make_draggable = function(){
    var self = this;
    this.drag_wrapper.draggable({drag: function(){self.ondrag()}, start: function(){self.ondragstart()}, helper: function(){return self.get_helper()}, handle: this.handle, stop: function(){self.ondragend()}, refreshPositions: true});
    return this;
}

/**
 * @description Creates drop pointer and adds to block
 * @returns {Block}
 */
Block.prototype.make_containable = function(){
    this.drop_pointer = $('<div class="drop_pointer"></div>');
    this.block.prepend(this.drop_pointer);
}

Block._last_uniq = 0;

/**
 * @description Get a uniq value for the block id
 * @returns {Number}
 */
Block.prototype.uniq = function(){
    if (! this._uniq){
        Block._last_uniq++;
        this._uniq = Block._last_uniq;
    }
    return this._uniq;
};

/**
 * @description Setup of initialization initialization, remembers original parameters, sets isIntance, registers block in list of all Blocks.
 * @returns {Block}
 */
Block.prototype.block_init = function(params){
    // all blocks inherit this
    this.initial_params = params;
    this.isInstance = params.instance || false;
    this.initial_params.instance = true;
    this.register();
    return this;
};

Block.blocks = [];

/**
 * @description Adds block to list of all Blocks, unless it is a factory block.
 * @returns {Block}
 */
Block.prototype.register = function(){
    if (this.isInstance){
        Block.blocks.push(this);
    }
    return this;
};

/**
 * @description Empty initialization step, intended for specific block types to override
 * @returns {Block}
 */
Block.prototype.dom_init = function(params){
    //customize for each type of block
    return this;
};

/**
 * @description Empty initialization step, intended for specific block types to override
 * @returns {Block}
 */
Block.prototype.init = function(params){
    return this;
};

/**
 * @description General initialization for all block types
 * @returns {Block}
 */
Block.prototype.initialize = function(params){
    // Block-level initialialization, all blocks
    //console.log('name: ' + this.constructor.name);
    this.drag_parent = null;
    this.block_init(params); // block-level, do not over-ride
    this.block_dom_init(params); // DOM initialization to own method
    /// 3. Move DOM properties to jq_propertyname for code clarity
    // Individual initialiation, over-ride for each type of block
    this.init(params); // class-specific initialization, customize for each class
    this.dom_init(params);
    this.make_draggable();
    this.make_droppable();
};

/**
 * @params {Object} params
 * @description General DOM initialization for all block types
 * @returns {Block}
 */
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
    this.drop_pointer = null;
    this.drop_target = null;
    this.make_nestable();
    if (params.x && params.y){
        this.position(params.x, params.y);
    }
    if (params.label){
        this.label(params.label);
    }
    return this;
};

/**
 * @description Debugging method for seeing the drop target while testing.  Has no effect unless DEBUG is true.
 * @returns {null}
 */
Block.prototype.highlight_drop_target = function(flag, other){
    if (!DEBUG) return;
    if (this.drop_target){
        if (flag){
            this.drop_target.css('border', '1px solid blue');
        }else{
            this.drop_target.css('border-width', '0px');
        }
    }else{
        if (flag){
            this.block.css('border', '1px solid yellow');
        }else{
            this.block.css('border-width', '0px');
        }
    }
    if (other){
        other.highlight_drop_pointer(flag);
    }
};

/**
 * @description Debugging method for seeing the drop pointer while testing.  Has no effect unless DEBUG is true.
 * @returns {null}
 */
Block.prototype.highlight_drop_pointer = function(flag, other){
    if (!DEBUG) return;
    if (this.drop_pointer){
        if (flag){
            this.drop_pointer.css('border', '1px solid red'); 
        }else{
            this.drop_pointer.css('border-width', '0px');
        }
    }else{
        if (flag){
            this.block.css('border', '1px solid green');
        }else{
            this.block.css('border-width', '0px');
        }
    }
    if (other){
        other.highlight_drop_target(flag);
    }
}

/**
 * @param {Block} other
 * @description Tests to see if one object intersects (drop_pointer to drop_target) another
 * @returns {Boolean}
 */
Block.prototype.drop_intersects = function(other){
    if (other === this) return false;
    if (!this.drop_pointer) return false;
    if (!other.drop_target) return false;
    if (this.drag_parent == other) return false;
    if (other.drag_parent == this) return false;
    return this.drop_pointer.intersects(other.drop_target);
}

/**
 * @param {Object} params
 * @description DOM initialization, adds and sizes drag_wrapper
 * @returns {Block}
 */
Block.prototype.make_nestable = function(params){
    this.drag_wrapper = $('<div class="drag_wrapper"></div>');
    var width = this.block.css('width');
    var left = this.block.css('left');
    var top = this.block.css('top');
    this.drag_wrapper.css({position: 'absolute', width: width, left: left, top: top});
    this.drag_wrapper.append(this.block);
    return this;
};

/**
 * @description DOM initialization, adds drop_target
 * @returns {Block}
 */
Block.prototype.make_droppable = function(){
    this.drop_target = $('<div class="drop_target"></div>');
    this.block.append(this.drop_target);
    return this;
};

/**
 * @class
 * @name Expression
 * @extends Block
 */
function Expression(){
}
Expression.prototype = new Block();

Expression.expressions = [];

/**
 * @description Adds expression to list of all Expressions, unless it is a factory block.
 * @returns {Expression}
 */
Expression.prototype.register = function(){
    if (this.isInstance){
        Expression.expressions.push(this);
    }
    return this;
};

/**
 * @description Initialization specialized for Expressions, changes block class to expression
 * @returns {Expression}
 */
Expression.prototype.init = function(params){
    this.block.addClass('expression').removeClass('block');
    return this;
}

/**
 * @description DOM initialization specialized for Expressions, adds "right" element, purely for styling
 * @returns {Expression}
 */
Expression.prototype.dom_init = function(params){
    this.block.prepend('<div class="right"></div>');
    return this;
}

/**
 * @description Sets drag_wrapper.  For an Expression, the drag wrapper is the expression's main block element.
 * @returns {Expression}
 */
Expression.prototype.make_nestable = function(params){
    this.drag_wrapper = this.block;
    return this;
};

/**
 * @description Drag handler, tests against other expressions while dragging.
 * @returns {null}
 */
Expression.prototype.ondrag = function(){
    var self = this;
    if (!Expression.expressions.length) return;
    var matched = false
    $.each(Expression.expressions, function(idx, block){
        matched = self.test_snapping(block);
        if (matched){
            self.snap_target = block;
            return false // stop the iteration
        }
    });
    if (!matched){
        self.highlight_drop_target(false, self);
    }
};

/**
 * @class
 * @name Step
 * @extends Block
 */
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

/**
 * @class
 * @name IntExpr
 * @extends Expression
 */
function IntExpr(params){
    this.initialize(params);
}
IntExpr.prototype = new Expression();
IntExpr.prototype.constructor = IntExpr;

IntExpr.prototype.drop_intersects = function(other){
    if (other === this) return false;
//    if (!this.drop_pointer) return false;
    if (!((other instanceof IntExpr) || (other instanceof IntValue))) return false;
//    if (this.drag_parent == other) return false;
//    if (other.drag_parent == this) return false;
    console.log(other.drag_wrapper);
    return this.drag_wrapper.intersects(other.drag_wrapper.find('.int'));
}

/**
 * @class
 * @name IntValue
 * @extends Expression
 */
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

/**
 * @class
 * @name BoolExpr
 * @extends Expression
 */
function BoolExpr(params){
    this.initialize(params);
}
BoolExpr.prototype = new Expression();
BoolExpr.prototype.constructor = BoolExpr;

/**
 * @class
 * @name BoolValue
 * @extends Expression
 */
function BoolValue(params){
    this.initialize(params);
    this.block.css('margin-left', '20px');
    this._checkbox = $('<input type="checkbox" />');
    this.block.prepend(this._checkbox);
    this._checkbox.css({position: 'absolute', top: '3px', left: '-20px'});
}
BoolValue.prototype = new Expression();
BoolValue.prototype.constructor = BoolValue;

/**
 * @class
 * @name Trigger
 * @extends Block
 */
function Trigger(params){
    this.initialize(params);
    this.block.addClass('trigger container');
    this.block.prepend('<div class="right"></div>');
    Trigger.triggers.push(this);
}
Trigger.prototype = new Block();
Trigger.prototype.constructor = Trigger;
Trigger.triggers = [];


/**
 * @class
 * @name Loop
 * @extends Block
 */
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



