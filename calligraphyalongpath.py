#!/usr/bin/env python




#=====================================================================
# import dependencies
#---------------------------------------------------------------------
import inkex
import bezmisc
import cubicsuperpath
import simpletransform
import simplestyle
import copy






#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# CalligraphyAlongPath Class
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class CalligraphyAlongPath(inkex.Effect):




  #===================================================================
  # class constructor
  #-------------------------------------------------------------------
  def __init__(self):

    # initiate
    inkex.Effect.__init__(self)

    # ellipsis pattern's width
    self.OptionParser.add_option("-e", "--pwidth", action="store",\
      type="float", dest="pwidth", default=4.0, help="Pattern Width")

    # ellipsis pattern's height
    self.OptionParser.add_option("-b", "--pheight", action="store",\
      type="float", dest="pheight", default=0.4, help="Pattern Height")

    # ellipsis pattern's angle
    self.OptionParser.add_option("-a", "--pangle", action="store",\
      type="int", dest="pangle", default=30, help="Pattern Angle")




  #===================================================================
  # main effect function
  #-------------------------------------------------------------------
  def effect(self):

    # we need exactly one path to work on
    if len(self.options.ids) != 1:
      inkex.errormsg(_("This extension requires one selected path."))
      return

    # get option values from GUI
    opts = self.options
    width = opts.pwidth if opts.pwidth else 0.4
    height = opts.pheight if opts.pheight else 4.0
    angle = opts.pangle if opts.pangle else 30

    # pattern instance
    self.ptrn = self.create_pattern((width, height), (50,50), angle, self.current_layer)

    # path element
    el = inkex.Effect.getElementById(self, self.options.ids[0])

    # parse element into cubic Bezier
    parsed = cubicsuperpath.parsePath(el.get('d'))[0]

    # duplicate the pattern and place on the path uniformly
    i = 0
    while i < (len(parsed) - 1): # we don't run this on the last item

        # nodes "s": starting node, "n": next node
        s = parsed[i]
        n = parsed[i + 1]

        # prepare arguments for Bezier function
        points = ((n[1][0], n[1][1]), (n[0][0], n[0][1]), (s[2][0], s[2][1]), (s[1][0], s[1][1]))

        # multiply patterns using the points
        self.duplicate(points)
        i += 1

    # delete the pattern
    self.ptrn.getparent().remove(self.ptrn)
  # /def effect




  #===================================================================
  # creates a pattern/brush to be used for calligraphic styles
  #-------------------------------------------------------------------
  def create_pattern(self, rxy, cxy, angle, parent):

    # radius vars
    (rx, ry) = rxy 

    # center vars
    (cx, cy) = cxy

    # pattern style
    style = {
      'stroke': '#000000',
      'stroke-width': '0',
      'fill': '#000000',
      'fill-opacity': '1.0'
    }

    # pattern element attributes
    attribs = {
      'style': simplestyle.formatStyle(style),
      'rx': str(rx),
      'ry': str(ry),
      'cx': str(cx),
      'cy': str(cy)
    }

    # create an xml element for the pattern
    el = inkex.etree.SubElement(parent, inkex.addNS('ellipse','svg'), attribs )

    # rotate the pattern to mimic calligraphy pen
    transformation = 'rotate(' + str(angle) + ',' + str(cx) + ',' + str(cy) + ')'
    transform = simpletransform.parseTransform(transformation)
    simpletransform.applyTransformToNode(transform, el)

    return el 
  # /def create_pattern




  #===================================================================
  # copy the pattern and position on the given coordinate
  #-------------------------------------------------------------------
  def copy_pattern(self, x, y):
    p = copy.deepcopy(self.ptrn)
    cx = float(self.ptrn.get('cx'))
    cy = float(self.ptrn.get('cy'))
    transformation = 'translate(' + str(x - cx) + ', ' + str(y - cy) + ')'
    transform = simpletransform.parseTransform(transformation)
    simpletransform.applyTransformToNode(transform, p)
    self.current_layer.append(p)
  # /def copy_pattern




  #===================================================================
  # duplicate the pattern
  #-------------------------------------------------------------------
  def duplicate(self, points):
    i = 0
    while i < 1:
      x, y = bezmisc.bezierpointatt(points, i)
      self.copy_pattern(x, y)
      i += 0.001
  # /def duplicate


# /Class CalligraphyAlongPath






#=====================================================================
# instantiate
#---------------------------------------------------------------------
if __name__ == '__main__':
  e = CalligraphyAlongPath()
  e.affect()
