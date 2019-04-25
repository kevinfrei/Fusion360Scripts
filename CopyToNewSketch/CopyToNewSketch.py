#Author-Kevin Frei
#Description-Copy all circles to a new sketch

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        sk = adsk.fusion.Sketch.cast(app.activeEditObject)
        ui.messageBox(sk.name)

        circles = sk.sketchCurves.sketchCircles        
        data = []
        for j in range(circles.count):
            c = circles.item(j)
            p = c.centerSketchPoint.worldGeometry
            data.append((p.x, p.y, p.z, c.radius))
            
        design = app.activeProduct
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = adsk.fusion.Sketch.cast(sketches.add(xyPlane))
        
        for d in data:           
            pt = adsk.core.Point3D.create(d[0], d[1], d[2])
            sketch.sketchCurves.sketchCircles.addByCenterRadius(pt, d[3])
            
#        a = sk.sketchCurves.sketchLines
#        ui.messageBox('{0} lines currently'.format(a.count))
#        for i in range(a.count - 1, -1, -1):
#            line = a.item(i)
#            if line.startSketchPoint.worldGeometry.x < 0:
#                a.item(i).deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
