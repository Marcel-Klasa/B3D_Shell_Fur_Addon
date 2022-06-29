import bpy, copy

class toShellData():
    def __init__(self):
        self.topShells = {}
        self.nodes = {}
        self.layers = []

data = toShellData()

class toShell():

    ### BUTTON TOP SHELL
    
    def createShell(height):
        act_objs = bpy.context.selected_objects
        
        for obj in  act_objs:
            obj.update_from_editmode()
            topShell = bpy.data.objects.new('Top_Shell', obj.data.copy())
            bpy.context.collection.objects.link(topShell)
            
            topShell.location = obj.location.copy()
            topShell.rotation_euler = obj.rotation_euler.copy()
            
            data.topShells[obj] = topShell

            for v1, v2 in zip(obj.data.vertices, topShell.data.vertices):
                v2.co += v2.normal * height
                data.nodes[v1] = v2
            
    ### BUTTON MID LAYER
            
    def CreateIntermediateLayers():
        
        for obj, shell in data.topShells.items():
            obj.update_from_editmode()
            shell.update_from_editmode()
            midLayer = bpy.data.objects.new('MidLayer', obj.data.copy())
            bpy.context.collection.objects.link(midLayer)
            
            midLayer.location = obj.location.copy()
            midLayer.rotation_euler = obj.rotation_euler.copy()
            shell.location = obj.location.copy()
            shell.rotation_euler = obj.rotation_euler.copy()
                        
            for v1, v2 in zip(obj.data.vertices, midLayer.data.vertices):
                print(data.nodes[v1])
                v2.co = (v1.co + data.nodes[v1].co) / 2