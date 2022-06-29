bl_info = {
    'name': 'Fur Shell Addon',
    'blender': (2, 93, 0),
    'category': 'Object',
    'version': (1, 0, 1),
    'author': 'Marcel Klasa Samuel Corno',
}

import copy
import bpy

ToShellModule = bpy.data.texts["ToShell.py"].as_module()
ToShell = ToShellModule.toShell
ToShellData = ToShellModule.toShellData
data = ToShellModule.data

class toShellOperator(bpy.types.Operator):
    
    bl_idname = 'opr.to_shell_operator'
    bl_label = 'To Shell'
    
    def execute(self, context):
        
        ToShell.createShell(context.scene.height)
            
        return {'FINISHED'}

class CreateMidLayersOperator(bpy.types.Operator):
    
    bl_idname = 'opr.intermediate_layers_operator'
    bl_label = 'intermediate layers'
    
    def execute(self, context):
        
        ToShell.CreateIntermediateLayers()
            
        return {'FINISHED'}

myStringProp = bpy.props.StringProperty(
  name='My String Property', default='hello',
  description='A basic string'
)

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
        zone2.label(text='2. Create intermediate layers')
        zone2.prop(context.scene, 'Layers')
        zone2.operator(CreateMidLayersOperator.bl_idname, text='Create intermediate layers')
        zone2.enabled = len(data.topShells) > 0

PROPS = {
    'height': bpy.props.FloatProperty(name='height', default=0.3, min = 0.05),
    'Layers': bpy.props.IntProperty(name='Layers', default=3, min = 1),
}

CLASSES = [
    Panel,
    ToShell,
    toShellOperator,
    CreateMidLayersOperator,
    ToShellData,
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
    bpy.utils.register_class(Panel)