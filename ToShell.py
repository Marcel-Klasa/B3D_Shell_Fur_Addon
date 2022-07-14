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
        data.topShells.clear()
        
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
            
    def CreateIntermediateLayers(layersCount):
        for obj, shell in data.topShells.items():
            for i in range(1, layersCount + 1):
                obj.update_from_editmode()
                shell.update_from_editmode()
                layer = bpy.data.objects.new(f"Layer{i}", obj.data.copy())
                bpy.context.collection.objects.link(layer)
                
                layer.location = obj.location.copy()
                layer.rotation_euler = obj.rotation_euler.copy()
                shell.location = obj.location.copy()
                shell.rotation_euler = obj.rotation_euler.copy()
                
                for v1, v2 in zip(obj.data.vertices, layer.data.vertices):
                    v2.co = v1.co + (data.nodes[v1].co - v1.co) * i / (layersCount + 1)