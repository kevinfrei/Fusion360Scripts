#Author-Kevin Frei
#Description-Remove Duplicate Circles & Lines from the active sketch

import adsk.core, adsk.fusion, adsk.cam, traceback, collections

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        sk = adsk.fusion.Sketch.cast(app.activeEditObject)
        #ui.messageBox(sk.name)
        # De-dupe the circles first:
        a = sk.sketchCurves.sketchCircles
        ui.messageBox('{0} circles currently'.format(a.count))
        seen = set()
        toRemove = []
        for i in range(a.count):
            c = sk.sketchCurves.sketchCircles.item(i)
            cr = c.radius
            cc = c.centerSketchPoint.worldGeometry
            data = '{0},{1},{2},{3}'.format(cr, cc.x, cc.y, cc.z)
            if data not in seen:
                seen.add(data)
            else:
                toRemove.append(i)
        if len(toRemove) > 0:
            toRemove.reverse()
            ui.messageBox('Removing {0} circles'.format(len(toRemove)))
            for i in toRemove:
                a.item(i).deleteMe()

        a = sk.sketchCurves.sketchLines
        ui.messageBox('{0} lines currently'.format(a.count))
        seen = set()
        toRemove = []
        for i in range(a.count):
            l = sk.sketchCurves.sketchLines.item(i)
            s = l.startSketchPoint.worldGeometry
            e = l.endSketchPoint.worldGeometry
            data = '{0},{1},{2},{3},{4},{5}'.format(s.x, s.y, s.z, e.x, e.y, e.z)
            if data not in seen:
                seen.add(data)
            else:
                toRemove.append(i)
        if len(toRemove) > 0:
            toRemove.reverse()
            ui.messageBox('Removing {0} lines'.format(len(toRemove)))
            for i in toRemove:
                a.item(i).deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
