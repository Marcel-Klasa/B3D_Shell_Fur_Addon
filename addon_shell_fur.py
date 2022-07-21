bl_info = {
    'name': 'Fur Shell Addon',
    'blender': (3, 2, 0),
    'category': 'Object',
    'version': (1, 0, 2),
    'author': 'Marcel Klasa & Samuel Corno',
}

import copy
import bpy
from bpy.utils import resource_path
from pathlib import Path

class toShellData():
    def __init__(self):
        self.topShells = {}
        self.nodes = {}
        self.layers = []
        self.obj = None

data = toShellData()

class toShell():

    ### BUTTON TOP SHELLd
    
    def createShell(height):
        act_objs = bpy.context.selected_objects
        data.topShells.clear()
        data.layers.clear()
        
        for obj in  act_objs:
            obj.update_from_editmode()
            topShell = bpy.data.objects.new('Top_Shell', obj.data.copy())
            bpy.context.collection.objects.link(topShell)
            
            topShell.location = obj.location.copy()
            topShell.rotation_euler = obj.rotation_euler.copy()
            
            data.topShells[obj] = topShell
            data.obj = obj
            
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
                    
                data.layers.append(layer)
                
        for layer in data.layers:
            bpy.ops.object.select_all(action='DESELECT')
            layer.select_set(state = True)
            data.obj.select_set(state = True)
            bpy.ops.object.join()    


class Render():

    ### BUTTON RENDER
    ### - Join Layers
    ### - Add Materials
    ### - Render to texture

    
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




class toShellOperator(bpy.types.Operator):
    
    bl_idname = 'opr.to_shell_operator'
    bl_label = 'To Shell'
    
    def execute(self, context):
        
        toShell.createShell(context.scene.height)
            
        return {'FINISHED'}

class CreateMidLayersOperator(bpy.types.Operator):
    
    bl_idname = 'opr.intermediate_layers_operator'
    bl_label = 'intermediate layers'
    
    def execute(self, context):
        
        toShell.CreateIntermediateLayers(context.scene.Layers)
            
        return {'FINISHED'}

class RenderLayersOperator(bpy.types.Operator):
    
    bl_idname = 'opr.render_layers_operator'
    bl_label = 'render layers'
    
    def execute(self, context):
        
        Render.applyMaterials(data.layers,data.topShells)
            
        return {'FINISHED'}


class Panel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_example_panel'
    bl_label = 'Shell'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shell Fur'
    
    def draw(self, context):
        zone1 = self.layout.column()
        zone1.label(text='1. Make a shell')
        zone1.prop(context.scene, 'height')
        zone1.operator(toShellOperator.bl_idname, text='Create Shell')
        zone1.enabled = len(bpy.context.selected_objects) > 0
        
        zone2 = self.layout.column()
        zone2.label(text='2. Modify Shell shape')
        zone2.label(text='3. Create intermediate layers')
        zone2.prop(context.scene, 'Layers')
        zone2.operator(CreateMidLayersOperator.bl_idname, text='Create intermediate layers')
        zone2.enabled = len(data.topShells) > 0
        
        zone3 = self.layout.column()
        zone3.label(text='4. Unwrap UVs')
        zone3.label(text='5. Select Path for saving')
        zone3.prop(context.scene, 'filepath')
        zone3.label(text='6. Select texture size')
        zone3.prop(context.scene, 'imageSizeX')
        zone3.prop(context.scene, 'imageSizeY')
        zone3.label(text='7. Render and wait')
        zone3.operator(RenderLayersOperator.bl_idname, text='Render')
        zone3.enabled = len(data.topShells) > 0
        
        #IMAGE_MT_editor_menus.draw_collapsible(context, layout)
        
        

PROPS = {
    'height': bpy.props.FloatProperty(name='height', default=0.3, min = 0.05),
    'Layers': bpy.props.IntProperty(name='Layers', default=3, min = 1),
    'filepath': bpy.props.StringProperty(name='Path', default = bpy.path.abspath('//')),
    'imageSizeX': bpy.props.IntProperty(name='Size X', default = 4096, min = 1),
    'imageSizeY': bpy.props.IntProperty(name='Size Y', default = 4096, min = 1),
}


######## Register everything ########

CLASSES = [
    Panel,
    toShell,
    toShellOperator,
    CreateMidLayersOperator,
    RenderLayersOperator,
    toShellData,
]

def register():
    for name, prop in PROPS.items():
        setattr(bpy.types.Scene, name, prop)
        
    for c in CLASSES:
        bpy.utils.register_class(c)

def unregister():
    for name, prop in PROPS.items():
        delattr(bpy.types.Scene, name, prop)
    
    for c in CLASSES:
        bpy.utils.unregister_class(c)

if __name__ == '__main__':
    for name, prop in PROPS.items():
        setattr(bpy.types.Scene, name, prop)
    
    bpy.utils.register_class(toShellOperator)
    bpy.utils.register_class(CreateMidLayersOperator)
    bpy.utils.register_class(RenderLayersOperator)
    bpy.utils.register_class(Panel)