#Author-Kevin Frei
#Description-Expands lines within a contained region

import adsk.core, adsk.fusion, adsk.cam, traceback, collections

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        sk = adsk.fusion.Sketch.cast(app.activeEditObject)

        circles = sk.sketchCurves.sketchCircles        
        for j in range(circles.count - 1, -1, -1):
            circles.item(j).deleteMe()
            
            
#        a = sk.sketchCurves.sketchLines
#        ui.messageBox('{0} lines currently'.format(a.count))
#        for i in range(a.count - 1, -1, -1):
#            line = a.item(i)
#            if line.startSketchPoint.worldGeometry.x < 0:
#                a.item(i).deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
