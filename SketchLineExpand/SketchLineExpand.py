#Author-Kevin Frei
#Description-Attempt to replace overlaid lines with individual lines.

import adsk.core, adsk.fusion, adsk.cam, traceback, collections

def getX(p):
    return p.x

def getY(p):
    return p.y

def getZ(p):
    return p.z

def delta(get, p1, p2):
    return get(p2) - get(p1)

def run(context):
    ui = None
    # The number of digits of accuracy for the slope values
    # accuracy = 5
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        sk = adsk.fusion.Sketch.cast(app.activeEditObject)

        lines = sk.sketchCurves.sketchLines

        # First, find out which plane the sketch lives in
        # Get our rise & run functions, assuming one plane is flat
        # TODO: This doesn't work for non-flat planes :/
        deltaX = False
        deltaY = False
        deltaZ = False
        for i in range(lines.count):
            l = lines.item(i)
            s = l.startSketchPoint.worldGeometry
            e = l.endSketchPoint.worldGeometry
            # TODO: This should be normalized somehow, but that's an optimization
            x = delta(getX, s, e)
            y = delta(getY, s, e)
            z = delta(getZ, s, e)
            if x != 0:
                deltaX = True
                if deltaY or deltaZ:
                    break
            if y != 0:
                deltaY = True
                if deltaX or deltaZ:
                    break
            if z != 0:
                deltaZ = True
                if deltaX or deltaY:
                    break

        getA = getY if deltaX == 0 else getX
        getB = getZ if deltaY == 0 else getY

        colinear = {}
        # For each potential, walk through the line segments and see if they
        # can be merged/removed/etc...
        for i in range(lines.count):
            # For each common slope, find unique actual lines
            line = lines.item(i)
            # Basically find A, B, and C for Ax + By = C
            s = line.startSketchPoint.worldGeometry
            e = line.endSketchPoint.worldGeometry
            run = delta(getA, s, e)
            rise = delta(getB, s, e)
            A = rise
            B = -run
            C = rise * s.x + run * s.y
            func = '{0:.5f},{1:.5f},{2:.5f}'.format(A, B, C)
            if func not in colinear:
                colinear[func] = [i]
            else:
                colinear[func].append(i)
        val = 0
        for i in colinear:
            lineList = colinear[i]
            if len(lineList) == 1:
                continue
            # We have more than one colinear line
            # Are they actually intersecting?
            for j in lineList:
                pass
#TODO: Continue here

        ui.messageBox('{} positions'.format(val))




#        for i in toRemove:
#            a.item(i).deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
