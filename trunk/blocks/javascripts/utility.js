function print(str){
    if (console && console.log){
        console.log(str);
    }
}

// Additions to the global object


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
    }
});

// Additions to the result set object

$.fn.extend({
    // set or return position
    positionRelative: function(pos){
        if (pos){
            this.css({position: 'absolute', left: pos.left + 'px', top: pos.top + 'px'});
            return this;
        }else{
            return this.offset();
        }
    },
    repositionInFrame: function(frame){
        var pos = frame.offset();
        this.each(function(){
            this.style.left = (parseInt(this.style.left) - pos.left) + 'px';
            this.style.top = (parseInt(this.style.top) - pos.top) + 'px';
        });
        return this;
    },
    // positioning helper, returns {left, top, right, bottom}
    box: function(){
        var pos = this.offset();
        if (!pos){
            print('warning: trying to get offset failed (is object not visible?)');
            print(this);
            pos = {left: 0, top: 0};
        }
//        console.log(this.info() + '.box() called.  offset == ' + pos);
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
        if (other.length < 1){
            return false;
        }
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
    // debug helper
    info: function(){
        var self = this.get(0);
        if (!self){
            console.log('trying to get info on an empty list?');
            return 'nil object';
        }
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
    }
});