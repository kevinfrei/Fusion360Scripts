#Author-Autodesk Inc. (Then changed by me :)
#Description-Extract BOM information from active design
#Doesn't look at components!

import adsk.core, adsk.fusion, traceback

def pickFile(ui, qty):
    try:
        fd = ui.createFileDialog();
        fd.isMultiSelectEnabled = False
        fd.title = "Specify output file for Bill of Materials ({0} items)".format(qty)
        fd.filter = "Comma Separated Value files (*.csv)"
        fd.filterIndex = 0
        dr = fd.showSave()
        if dr == adsk.core.DialogResults.DialogOK:
            return fd.filename
        else:
            return
    except:
        return

def dimtxt(d,n):
    a = max(d.x, d.y, d.z)
    c = min(d.x, d.y, d.z)
    b = d.x + d.y + d.z - a - c
    return "{3},{0:1.6f},{1:1.6f},{2:1.6f}".format(a/2.54, b/2.54, c/2.54, n)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        title = 'Extract BOM'
        if not design:
            ui.messageBox('No active design', title)
            return

        # Get all occurrences in the root component of the active design
        root = design.rootComponent
        
        # Gather information about each unique component
        bom = dict()
        for body in root.bRepBodies:
            if body.isSolid:
                k = dimtxt(body.boundingBox.minPoint.vectorTo(body.boundingBox.maxPoint), body.material.name)
                if k not in bom:
                    bom[k] = [body.name]
                else:
                    bom[k].append(body.name)
        # Display the BOM
        file = pickFile(ui, len(bom))
        if not file:
            return
        out = open(file, "w")
        out.write("Quantity,Material,Length,Width,Height,Name(s)\n")
        for dim,names in bom.items():
            out.write("{0},{1},{2}\n".format(len(names),dim,",".join(names)))
        out.close()
        ui.messageBox("Data saved to {0}".format(file))
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
