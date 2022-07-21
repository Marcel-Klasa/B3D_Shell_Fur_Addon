import bpy, copy
from bpy.utils import resource_path
from pathlib import Path

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
                layer = bpy.data.objects.new("Layers", obj.data.copy())
                bpy.context.collection.objects.link(layer)
                
                layer.location = obj.location.copy()
                layer.rotation_euler = obj.rotation_euler.copy()
                shell.location = obj.location.copy()
                shell.rotation_euler = obj.rotation_euler.copy()
                
                for v1, v2 in zip(obj.data.vertices, layer.data.vertices):
                    v2.co = v1.co + (data.nodes[v1].co - v1.co) * i / (layersCount + 1)


class Render():

    ### BUTTON RENDER
    ### - Join Layers
    ### - Add Materials
    ### - Render to texture
    
#    def Join_Layers(): ##help
#        for I in range(1, len(data.layers)):
#            bpy.ops.object.select_all(action='DESELECT')
#            data.layers[I].select_set(state = True)
#            data.layers[0].select_set(state = True)
#            bpy.ops.object.join()

    
    def applyMaterials(layers, top_layers):
        
        USER = Path(resource_path('USER'))
        ADDON = "B3D_Shell_Fur_Addon-main"
        ASSETSBLEND = "Shell Fur Addon V13.blend"
        srcPath = USER / "scripts/addons" / ADDON / "assets" / ASSETSBLEND
        blendpath = str(srcPath)
        
        with bpy.data.libraries.load(blendpath, link=False) as (data_src, data_dst):
            data_dst.materials = ["Layers_mat"]
            data_dst.materials = ["Top_Shell_Mat"]
        layer_mat = data_dst.materials[0]
        topshell_mat = data_dst.materials[0]
        
        for layer in layers:
            if layer.data.materials:
                layer.data.materials[0] = mat
            else:
                layer.data.materials.append(mat)
        
        for top_layer in top_layers:
            if layers.data.materials:
                layers.data.materials[0] = mat
            else:
                layers.data.materials.append(mat)
        
        #bpy.context.object.visible_shadow = False

    