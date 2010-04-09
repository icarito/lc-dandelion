/**
 * Blocks Utilities 0.1 (http://livingcode.org/blocks)
 * Copyright (c) 2008-2009 Dethe Elza (http://livingcode.org/)
 * 
 * Licensed under the MIT (MIT-LICENSE.txt)
 *
 */
 
 /**
 * @fileOverview Scratch-specific extensions for jQuery
 * @name layout
 * @author Dethe Elza
 */

var dk_grey = '#666';
var md_grey = '#999';
var lt_grey = '#CCC';
var white = '#FFF';
var MAX_WIDTH = $(window).width();
var MAX_HEIGHT = $(window).height();
var TOP_BUTTON_BAR_HEIGHT = 45;
var COLUMN_HEIGHT = MAX_HEIGHT - TOP_BUTTON_BAR_HEIGHT;
var BLOCKS_COLUMN_WIDTH = 210;
var STAGE_COLUMN_WIDTH = 450;
var PAD = 10;

/**
 * @class
 * @name Layout
 */
$.fn.extend( /** @lends Layout.prototype */ {
    /**
     * @returns Element
     * @description creates a new div, gives it an id, places it absolutely, appends it to current item, and returns the new div (NOT current item)
     */
    place: function(box){
        var div = $('<div id="' + box.name + '"></div>');
        div.css({position: 'absolute', left: box.x, top: box.y, width: box.w, height: box.h, backgroundColor: box.c});
        this.append(div);
        return div;
    },
    /**
     * @returns jQuery
     * @description applies CSS border rounding, border, and overflow, returns this
     */
    round: function(topleft, topright, bottomright, bottomleft, bordercolor){
        this.css('-webkit-border-top-left-radius', topleft);
        this.css('-moz-border-radius-topleft', topleft);
        this.css('border-top-left-radius', topleft);
        this.css('-webkit-border-top-right-radius', topright);
        this.css('-moz-border-radius-topright', topright);
        this.css('border-top-right-radius', topright);
        this.css('-webkit-border-bottom-right-radius', bottomright);
        this.css('-moz-border-radius-bottomright', bottomright);
        this.css('border-bottom-right-radius', bottomright);
        this.css('-webkit-border-bottom-left-radius', bottomleft);
        this.css('-moz-border-radius-bottomleft', bottomleft);
        this.css('-border-bottom-left-radius', bottomleft);
        this.css('border', '3px inset ' + bordercolor);
        this.css('overflow-x', 'auto');
        return this;
    },
    /**
     * @returns jQuery
     * @description uses button_spec to create a button menu interface, returns this
     */
    block_menu_buttons: function(button_spec){
        var parent = this;
        $.each(button_spec, function(idx, spec){
            var button = $('<div id="button_' + this.name + '">' + $.upcap(this.name) + '</div>');
            parent.append(button);
            button.round(10,10,10,10,md_grey);
            button.css({backgroundColor: dk_grey, color: spec.color, width: 75, display: 'block', textAlign: 'center', 'float': 'left', marginLeft: 10, borderStyle: 'outset'});
            button.click(function(){
                application.show_block_palette(spec.name);
                $(application.current_button).trigger('unselect');
                application.current_button = this;
                $(this).css({backgroundColor: spec.color, color: white});
            });
            button.bind('unselect', function(){
                $(this).css({backgroundColor: dk_grey, color: spec.color});
            });
            if (spec['default']){
                button.click();
            }
        });
        return this;
    },
    /**
     * @returns jQuery
     * @description creates a new block palette and hides it (they all occupy the same space), return this
     */
    add_palette: function(name, color, block_spec){
        var palette = $('<div></div>');
        application['_' + name + '_palette'] = palette;
        this.append(palette);
        $.each(block_spec, function(){
            palette.append( new this.type({label: this.label, x: 2, y: this.y, color: color}).drag_wrapper);
        });
        palette.hide();
        return this;
    }
    
});


// Scratch object, rules for initializing and updating scratch layout (should be mostly declarative)
/**
 * @class
 * @name Scratch
 */
function Scratch(){};

/**
 * @description second part of two-part initialization
 * @returns null
 */
Scratch.prototype.initialize = function(){
    $(document.body).css({margin: 0, padding: 0, overflow: 'hidden'});
    $(document.body).round(15,15,15,15,md_grey).css({'border-style': 'outset', 'background-color': lt_grey, 'height': MAX_HEIGHT - 6});
    $('#top_button_bar').css({height: TOP_BUTTON_BAR_HEIGHT + 'px', backgroundColor: lt_grey});
    $('#top_button_bar h1').css({display: 'inline', padding: '5px'});
    this.blocks_column();
    this.scripts_column();
    this.stage_column();
};

Scratch.prototype.blocks_column = function(){
    var box = {x: PAD, y: TOP_BUTTON_BAR_HEIGHT + PAD,
               w: BLOCKS_COLUMN_WIDTH, h: 115,
               name: 'blocks_menu', c: md_grey};
    $('body').place(box).round(15,15,5,5, dk_grey);
    box.y = box.y + box.h + PAD; box.h = COLUMN_HEIGHT - box.y - PAD; box.name = 'blocks_palette'; box.c = dk_grey;
    $('body').place(box).round(5,5,15,15, md_grey);
    this.blocks_palettes();
    this.blocks_buttons();
};

Scratch.prototype.blocks_buttons = function(){
    $('#blocks_menu').block_menu_buttons([
        {color: 'blue', name: 'motion', 'default': true},
        {color: 'orange', name: 'control'},
        {color: 'purple', name: 'looks'},
        {color: 'lightblue', name: 'sensing'},
        {color: 'violet', name: 'sound'},
        {color: 'green', name: 'numbers'},
        {color: 'turquoise', name: 'pen'},
        {color: 'red', name: 'variables'}
    ]);
};

Scratch.prototype.blocks_palettes = function(){
    this.load_images();
    this.motion_palette();
    this.control_palette();
    this.looks_palette();
    this.sensing_palette();
    this.sound_palette();
    this.numbers_palette();
    this.pen_palette();
    this.variables_palette();
};

Scratch.prototype.load_images = function(){
    this.images = {
        flag: $('<img class="block_icon" width="18" height="18" src="images/flag.png" />'),
        stopsign: $('<img class="block_icon" width="18" height="18" src="images/stopsign.png" />'),
        clockwise: $('<img class="block_icon" width="18" height="18" src="images/clockwise.png" />'),
        counterclockwise: $('<img class="block_icon" width="18" height="18" src="images/counterclockwise.png" />')
    };
};


Scratch.prototype.show_block_palette = function(palette_name){
    if(this._current_palette){
        this._current_palette.hide();
    }
    this._current_palette = this['_' + palette_name + '_palette'];
    this._current_palette.show();
};

Scratch.prototype.control_palette = function(){
    return $('#blocks_palette').add_palette('control', 'gold', [
        {type: Trigger, label: 'When [{flag}] clicked', y: 5},
        {type: Trigger, label: 'When [key] pressed', y: 50},
        {type: Trigger, label: 'When [sprite] clicked', y: 95},
        {type: Step, label: 'Wait [1] secs', y: 140},
        {type: Loop, label: 'forever', y: 180},
        {type: Loop, label: 'repeat [10]', y: 290},
        {type: Step, label: 'broadcast [message]', y: 400},
        {type: Step, label: 'broadcast [message] and wait', y: 440},
        {type: Trigger, label: 'When I receive [message]', y: 480},
        {type: Loop, label: 'forever if [bool]', y: 525},
        {type: Loop, label: 'if [bool]', y: 635},
        {type: Loop, label: 'if [bool] else', y: 745},
        {type: Step, label: 'wait until [bool]',x: 2, y: 855},
        {type: Loop, label: 'repeat until [bool]', y: 895},
        {type: Step, label: 'stop script', y: 1005},
        {type: Step, label: 'stop all [{stopsign}]', y: 1045}
    ]);
};

Scratch.prototype.motion_palette = function(){
    return $('#blocks_palette').add_palette('motion', 'blue', [
        {type: Step, label: 'Move [10] steps', y: 5},
        {type: Step, label: 'Turn [{clockwise}] [10] degrees', y: 45},
        {type: Step, label: 'Turn [{counterclockwise}] [10] degrees', y: 85},
        {type: Step, label: 'point in direction [90]', y: 130},
        {type: Step, label: 'point towards [sprite]', y: 170},
        {type: Step, label: 'go to x: [-200] y: [-150]', y: 215},
        {type: Step, label: 'go to [sprite]', y: 255},
        {type: Step, label: 'glide [1] secs to x: [-200] y: [-150]', y: 295},
        {type: Step, label: 'change x by [10]', y: 340},
        {type: Step, label: 'set x to [0]', y: 380},
        {type: Step, label: 'change y by [10]', y: 420},
        {type: Step, label: 'set y to [0]', y: 460},
        {type: Step, label: 'if on edge, bounce', y: 505},
        {type: Step, label: '[check] x position', y: 550},
        {type: Step, label: '[check] y position', y: 590},
        {type: Step, label: '[check] direction', y: 630}
    ]);
};

Scratch.prototype.looks_palette = function(){
    return $('#blocks_palette').add_palette('looks', 'blueviolet', [
        {type: Step, label: 'switch to costume [costume]', y: 5},
        {type: Step, label: 'next costume', y: 45},
        {type: Step, label: 'say ["Hello"] for [2] secs', y: 90},
        {type: Step, label: 'say ["Hello"]', y: 130},
        {type: Step, label: 'think ["Hmmm..."] for [2] secs', y: 170},
        {type: Step, label: 'think ["Hmmm..."]', y: 210},
        {type: Step, label: 'change [effect] effect by [25]', y: 255},
        {type: Step, label: 'set [effect] effect to [2]', y: 295},
        {type: Step, label: 'clear graphic effects', y: 335},
        {type: Step, label: 'change size by [10]', y: 380},
        {type: Step, label: 'set size to [40]', y: 420},
        {type: Step, label: '[check] size', y: 460},
        {type: Step, label: 'show', y: 505},
        {type: Step, label: 'hide', y: 545},
        {type: Step, label: 'go to front', y: 590},
        {type: Step, label: 'go back [1] layers', y: 630}
    ]);
};

Scratch.prototype.sensing_palette = function(){
    return $('#blocks_palette').add_palette('sensing', 'cyan', [
        {type: IntExpr, label: 'mouse x', y: 5},
        {type: IntExpr, label: 'mouse y', y: 45},
        {type: BoolExpr, label: 'mouse down?', y: 85},
        {type: BoolExpr, label: 'key [key] pressed?', y: 130},
        {type: BoolExpr, label: 'touching [sprite]?', y: 175},
        {type: BoolExpr, label: 'touching [color]?', y: 215},
        {type: BoolExpr, label: 'color [color] is over [color]?', y: 255},
        {type: IntExpr, label: 'distance to [sprite]', y: 300},
        {type: Step, label: 'reset timer', y: 345},
        {type: IntValue, label: 'timer', y: 385},
        {type: IntValue, label: 'loudness', y: 430},
        {type: BoolValue, label: 'loud?', y: 470}
        // Not implemented: sensor values
    ]);
};

Scratch.prototype.sound_palette = function(){
    return $('#blocks_palette').add_palette('sound', 'magenta', [
        {type: Step, label: 'play sound [sound]', y: 5},
        {type: Step, label: 'play sound [sound] and wait', y: 45},
        {type: Step, label: 'stop all sounds', y: 85}
        // Not implemented: midi notes and instruments
    ]);
};

Scratch.prototype.numbers_palette = function(){
    return $('#blocks_palette').add_palette('numbers', 'seagreen', [
        {type: IntExpr, label: '[int] + [int]', y: 5},
        {type: IntExpr, label: '[int] - [int]', y: 45},
        {type: IntExpr, label: '[int] * [int]', y: 85},
        {type: IntExpr, label: '[int] / [int]', y: 125},
        {type: IntExpr, label: 'pick random [int] to [int]', y: 170},
        {type: BoolExpr, label: '[int] &lt; [int]', y: 215},
        {type: BoolExpr, label: '[int] = [int]', y: 255},
        {type: BoolExpr, label: '[int] > [int]', y: 295},
        {type: BoolExpr, label: '[bool] and [bool]', y: 340},
        {type: BoolExpr, label: '[bool] or [bool]', y: 380},
        {type: BoolExpr, label: 'not [bool]', y: 420},
        {type: IntExpr, label: '[int] mod [int]', y: 465},
        {type: IntExpr, label: 'abs [int]', y: 505},
        {type: IntExpr, label: 'round [int]', y: 545}
    ]);
};

Scratch.prototype.pen_palette = function(){
    return $('#blocks_palette').add_palette('pen', 'green', [
        {type: Step, label: 'clear', y: 5},
        {type: Step, label: 'pen down', y: 50},
        {type: Step, label: 'pen up', y: 90},
        {type: Step, label: 'set pen color to [color]', y: 135},
        {type: Step, label: 'change pen color by [10]', y: 175},
        {type: Step, label: 'set pen color to [0]', y: 205},
        {type: Step, label: 'change pen shade by [10]', y: 250},
        {type: Step, label: 'set pen shade to [0]', y: 295},
        {type: Step, label: 'change pen size by [1]', y: 340},
        {type: Step, label: 'set pen size to [1]', y: 380},
        {type: Step, label: 'stamp', y: 425}
    ]);
};

Scratch.prototype.variables_palette = function(){
    return $('#blocks_palette').add_palette('variables', 'orangered', [
        {type: Step, label: 'Make a variable', y: 5}, // should be a Button
        {type: Step, label: 'Delete a variable', y: 45}, // should be a Button
        {type: Step, label: 'change x by [1]', y: 90},
        {type: Step, label: 'set x to [0]', y: 130},
        {type: IntValue, label: 'x', y: 170},
        {type: Step, label: 'change y by [1]', y: 215},
        {type: Step, label: 'set y to [0]', y: 255},
        {type: IntValue, label: 'y', y: 295}
    ]);
};


Scratch.prototype.scripts_column = function(){
    var left = BLOCKS_COLUMN_WIDTH + PAD * 2;
    var top = TOP_BUTTON_BAR_HEIGHT + PAD;
    var width = MAX_WIDTH - (BLOCKS_COLUMN_WIDTH + STAGE_COLUMN_WIDTH + PAD * 4);
    var height = 80;
    $('body').place({name: 'scripts_controlpanel', x: left, y: top, w: width, h: height, c: md_grey}).round(15,30,5,5, dk_grey);
    top = top + height + PAD;
    height = COLUMN_HEIGHT - top - PAD;
    $('body').place({name: 'scripts_container', x: left, y: top, w: width, h: height, c: dk_grey}).round(5,5,15,15, md_grey);
};

Scratch.prototype.stage_column = function(){
    var left = MAX_WIDTH - (STAGE_COLUMN_WIDTH + PAD);
    var top = PAD;
    var width = STAGE_COLUMN_WIDTH;
    var height = 50;
    $('body').place({name: 'stage_tools', x: left, y: top, w: width, h: height, c: lt_grey});
    top = top + height + PAD;
    height = 350;
    $('body').place({name: 'stage_canvas', x: left, y: top, w: width, h: height, c: white}).css('border', '3px inset ' + md_grey);
    top = top + height + PAD;
    height = 30;
    $('body').place({name: 'stage_buttons', x: left, y: top, w: width, h: height, c: lt_grey});
    top = top + height + PAD;
    height = COLUMN_HEIGHT - top - PAD;
    $('body').place({name: 'stage_sprites', x: left, y: top, w: width, h: height, c: lt_grey}).round(15,15,15,15,md_grey);
};


$(function(){
    window.application = new Scratch();
    application.initialize();
});