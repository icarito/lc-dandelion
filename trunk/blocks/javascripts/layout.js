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

$.fn.extend({
    place: function(box){
        this.css({position: 'absolute', left: box.x + 'px', top: box.y + 'px', width: box.w + 'px', height: box.h + 'px', backgroundColor: box.c});
        return this;
    },
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
    block_menu_button: function(color, choice){
        this.round(10,10,10,10,md_grey);
        this.css({backgroundColor: dk_grey, color: color, width: 75, display: 'block', float: 'left', marginLeft: 10, borderStyle: 'outset'});
        this.click(function(){
            scratch.show_block_palette(choice);
            $(scratch.current_button).trigger('unselect');
            scratch.current_button = this;
            $(this).css({backgroundColor: color, color: white});
        });
        this.bind('unselect', function(){
            $(this).css({backgroundColor: dk_grey, color: color});
        });
        return this;
    }
});

function Scratch(){};

Scratch.prototype.initialize = function(){
    $(document.body).css({margin: 0, padding: 0});
    $(document.body).round(15,15,15,15,md_grey).css({'border-style': 'outset', 'background-color': lt_grey, 'height': MAX_HEIGHT - 6});
    $('#top_button_bar').css({height: TOP_BUTTON_BAR_HEIGHT + 'px', backgroundColor: lt_grey});
    $('#top_button_bar h1').css({display: 'inline', padding: '5px'});
    this.blocks_column();
    this.scripts_column();
    this.stage_column();
}

Scratch.prototype.blocks_column = function(){
    var left = PAD;
    var top = TOP_BUTTON_BAR_HEIGHT + PAD;
    var width = BLOCKS_COLUMN_WIDTH;
    var height = 115;
    $('#blocks_menu').place({x: left, y: top, w: width, h: height, c: md_grey}).round(15,15,5,5, dk_grey);
    top = top + height + PAD;
    height = COLUMN_HEIGHT - top - PAD;
    $('#blocks_palette').place({x: left, y: top, w: width, h: height, c: dk_grey}).round(5,5,15,15, md_grey);
    this.blocks_palettes();
    this.blocks_buttons();
}

Scratch.prototype.blocks_buttons = function(){
    $('#button_motion').block_menu_button('blue', 'motion');
    $('#button_looks').block_menu_button('purple', 'looks');
    $('#button_sound').block_menu_button('violet', 'sound');
    $('#button_pen').block_menu_button('turquoise', 'pen');
    $('#button_control').block_menu_button('orange', 'control').click();
    $('#button_sensing').block_menu_button('blue', 'sensing');
    $('#button_numbers').block_menu_button('green', 'numbers');
    $('#button_variables').block_menu_button('red', 'variables');
}

Scratch.prototype.blocks_palettes = function(){
    //this.motion_palette();
    // this.looks_palette();
    // this.sound_palette();
    // this.pen_palette();
    this.control_palette();
    // this.sensing_palette();
    // this.numbers_palette();
    // this.variables_palette();
}

Scratch.prototype.show_block_palette = function(palette_name){
    if(this._current_palette){
        this._current_palette.hide();
    }
    this._current_palette = this['_' + palette_name + '_palette'];
    this._current_palette.show();
}

Scratch.prototype.control_palette = function(){
    var cp = $('<div></div>');
    this._control_palette = cp;
    $('#blocks_palette').append(cp);
    cp.append(new Trigger({label: 'When [flag] clicked', x: 2, y: 5, color: 'gold'}).drag_wrapper);
    cp.append(new Trigger({label: 'When [key] pressed', x: 2, y: 50, color: 'gold'}).drag_wrapper);
    cp.append(new Trigger({label: 'When [Sprite1] clicked', x: 2, y: 95, color: 'gold'}).drag_wrapper);
    cp.append(new Step({label: 'Wait [1] secs', x: 2, y: 140, color: 'gold'}).drag_wrapper);
    cp.append(new Loop({label: 'forever', x: 2, y: 180, color: 'gold'}).drag_wrapper);
    cp.append(new Loop({label: 'repeat [10]', x: 2, y: 290, color: 'gold'}).drag_wrapper);
    cp.append(new Step({label: 'broadcast [message]', x: 2, y: 400, color: 'gold'}).drag_wrapper);
    cp.append(new Step({label: 'broadcast [message] and wait', x: 2, y: 440, color: 'gold'}).drag_wrapper);
    cp.append(new Trigger({label: 'When I receive [message]', x: 2, y: 480, color: 'gold'}).drag_wrapper);
    cp.append(new Loop({label: 'forever if [condition]', x: 2, y: 525, color: 'gold'}).drag_wrapper);
    cp.append(new Loop({label: 'if [condition]', x: 2, y: 635, color: 'gold'}).drag_wrapper);
    cp.append(new Loop({label: 'if [condition] else', x: 2, y: 745, color: 'gold'}).drag_wrapper);
    cp.append(new Step({label: 'wait until [condition]',x: 2, y: 855, color: 'gold'}).drag_wrapper);
    cp.append(new Loop({label: 'repeat until [condition]', x: 2, y: 895, color: 'gold'}).drag_wrapper);
    cp.append(new Step({label: 'stop script', x: 2, y: 1005, color: 'gold'}).drag_wrapper);
    cp.append(new Step({label: 'stop all [sign]', x: 2, y: 1045, color: 'gold'}).drag_wrapper);
    cp.css('display', 'none');
    return this;
}

Scratch.prototype.motion_palette = function(){
    var mp = $('<div></div>').hide();
    this._motion_palette = mp;
    $('#blocks_palette').append(mp);
    mp.append(new Step({label: 'Move [10] steps', x: 2, y: 5, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'Turn [Clockwise] [10] degrees', x: 2, y: 45, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'Turn [Counter] [10] degrees', x: 2, y: 85, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'point in direction [90]', x: 2, y: 130, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'point towards [sprite]', x: 2, y: 170, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'go to x: [-200] y: [-150]', x: 2, y: 215, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'go to [sprite]', x: 2, y: 255, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'glide [1] secs to x: [-200] y: [-150]', x: 2, y: 295, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'change x by [10]', x: 2, y: 340, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'set x to [0]', x: 2, y: 380, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'change y by [10]', x: 2, y: 420, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'set y to [0]', x: 2, y: 420, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: 'if on edge, bounce', x: 2, y: 465, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: '[check] x position', x: 2, y: 510, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: '[check] y position', x: 2, y: 550, color: 'blue'}).drag_wrapper);
    mp.append(new Step({label: '[check] direction', x: 2, y: 590, color: 'blue'}).drag_wrapper);
    return this;
}

Scratch.prototype.scripts_column = function(){
    var left = BLOCKS_COLUMN_WIDTH + PAD * 2;
    var top = TOP_BUTTON_BAR_HEIGHT + PAD;
    var width = MAX_WIDTH - (BLOCKS_COLUMN_WIDTH + STAGE_COLUMN_WIDTH + PAD * 4);
    var height = 80;
    $('#scripts_controlpanel').place({x: left, y: top, w: width, h: height, c: md_grey}).round(15,30,5,5, dk_grey);
    top = top + height + PAD;
    height = COLUMN_HEIGHT - top - PAD;
    $('#scripts_container').place({x: left, y: top, w: width, h: height, c: dk_grey}).round(5,5,15,15, md_grey);
}

Scratch.prototype.stage_column = function(){
    var left = MAX_WIDTH - STAGE_COLUMN_WIDTH - PAD;
    var top = TOP_BUTTON_BAR_HEIGHT + PAD;
    var width = STAGE_COLUMN_WIDTH;
    var height = 50;
    $('#stage_tools').place({x: left, y: top, w: width, h: height, c: lt_grey});
    top = top + height + PAD;
    height = 350;
    $('#stage_canvas').place({x: left, y: top, w: width, h: height, c: white}).css('border', '3px inset ' + md_grey);
    top = top + height + PAD;
    height = 30;
    $('#stage_buttons').place({x: left, y: top, w: width, h: height, c: lt_grey});
    top = top + height + PAD;
    height = COLUMN_HEIGHT - top - PAD;
    $('#stage_sprites').place({x: left, y: top, w: width, h: height, c: lt_grey}).round(15,15,15,15,md_grey);
}


$(function(){
    window.scratch = new Scratch();
    scratch.initialize();
});