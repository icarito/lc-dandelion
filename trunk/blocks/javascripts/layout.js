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
        return this;
    },
    block_menu_button: function(color, choice){
        this.round(5,5,5,5,md_grey);
        this.css({backgroundColor: dk_grey, color: color, width: 75, display: 'block', float: 'left', marginLeft: 10, borderStyle: 'outset'});
        this.click(function(){
            //scratch.show_block_factory(choice);
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
    $('#blocks_factories').place({x: left, y: top, w: width, h: height, c: dk_grey}).round(5,5,15,15, md_grey);
    this.blocks_buttons();
}

Scratch.prototype.blocks_buttons = function(){
    $('#button_motion').block_menu_button('blue', 'motion_factory');
    $('#button_looks').block_menu_button('purple', 'looks_factory');
    $('#button_sound').block_menu_button('violet', 'sound_factory');
    $('#button_pen').block_menu_button('turquoise', 'pen_factory');
    $('#button_control').block_menu_button('orange', 'control_factory').click();
    $('#button_sensing').block_menu_button('blue', 'sensing_factory');
    $('#button_numbers').block_menu_button('green', 'numbers_factory');
    $('#button_variables').block_menu_button('red', 'variables_factory');
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