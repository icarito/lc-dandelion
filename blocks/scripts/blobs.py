'''
In progress, still trying to figure out best approach for generating 2D metaballs

Notes from Flash implementation:

http://www.quasimondo.com/archives/000562.php#000562

It works like this: at the base are some circle movieclips that meander
around the center and change their sizes - pretty standard particle motion
kind of stuff. In the next step I blur this screen with a big radius. Then
I use the new threshold filter to turn all pixels that a darker as a certain
grey-level to black and all the brighter ones to transparent. This results
already in the classical "blob" outline. Then I add a very fine black glow
in order to remove the staircase look of the borders. As a final touch I use
the bevel filter to give it the 3d look. That's it.
'''

output_template = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%%" height="100%%" version="1.1"
xmlns="http://www.w3.org/2000/svg">
<defs>
  <filter id="MyFilter" filterUnits="userSpaceOnUse" x="0" y="0" width="200" height="120">
    <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
    <!--feOffset in="blur" dx="4" dy="4" result="offsetBlur"/-->
    <feSpecularLighting in="blur" surfaceScale="5" specularConstant=".75" 
                        specularExponent="20" lighting-color="#bbbbbb"  
                        result="specOut">
      <fePointLight x="-5000" y="-10000" z="20000"/>
    </feSpecularLighting>
    <feComposite in="specOut" in2="SourceAlpha" operator="in" result="specOut"/>
    <feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" 
                 k1="0" k2="1" k3="1" k4="0" result="litPaint"/>
    <!--feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="litPaint"/>
    </feMerge-->
  </filter>
</defs>
%s
</svg>'''

RATIO = 1.61803399 # golden ratio

class Blob(object):

    def __init__(self, **kws):
        self.color = 'blue'
        self.width = 150
        self.height = int(round(self.width / RATIO))
        self.metaballs = 5
        self.template = template = '<circl filter="url(#MyFilter)" fill="%(color)s" cx="%(cx)s" cy="%(cy)s" r="%(radius)s" />'
        self.__dict__.update(kws) # allow keyword arguments to over-ride defaults
