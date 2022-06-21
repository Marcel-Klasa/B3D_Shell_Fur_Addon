bl_info = {
    # required
    'name': 'Fur Shell Addon',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 1),
    'author': 'Marcel Klasa Samuel Corno',
}

import bpy, copy

height = 0.3

class toShellData():
    def __init__(self):
        self.act_obj = None
        self.nodes = []
        self.topShell = None
        self.layers = []


data = toShellData()

class toShell():

    ### BUTTON TOP SHELL
    
    def createShell():
        act_obj = bpy.context.active_object
        
        if act_obj is None:
            return
        
        topShell = bpy.data.objects.new('Top_Shell', act_obj.data.copy())
        bpy.context.collection.objects.link(topShell)

        data.act_obj = act_obj

        data.topShell = topShell

        for v1, v2 in zip(act_obj.data.vertices, topShell.data.vertices):
            v2.co += v2.normal * height
            data.nodes.append((v1, v2))
            
    ### BUTTON MID LAYER
            
    def CreateIntermediateLayers():
        
        midLayer = bpy.data.objects.new('MidLayer', data.act_obj.data.copy())
        bpy.context.collection.objects.link(midLayer)
        
        for lerp, v in zip(data.nodes, midLayer.data.vertices):
            v.co = (lerp[0].co + lerp[1].co) / 2
        

class toShellOperator(bpy.types.Operator):
    
    bl_idname = 'opr.to_shell_operator'
    bl_label = 'To Shell'
    
    def execute(self, context):
        
        toShell.createShell()
            
        return {'FINISHED'}

class CreateMidLayersOperator(bpy.types.Operator):
    
    bl_idname = 'opr.to_shell_operator_test'
    bl_label = 'To Shell test'
    
    def execute(self, context):
        
        toShell.CreateIntermediateLayers()
            
        return {'FINISHED'}

class Panel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_example_panel'
    bl_label = 'Shell'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shell Fur'
    
    def draw(self, context):
        self.layout.label(text='1. Make a shell')
        col = self.layout.column()
        col.enabled = False#bpy.context.active_object is not None
        col.prop(self.layout.operator(toShellOperator.bl_idname, text='Create Shell'), "custom_property")
        self.layout.label(text='2. Create intermediate layers')
        self.layout.operator(CreateMidLayersOperator.bl_idname, text='Create intermediate layers')

CLASSES = [
    Panel,
    toShell,
    toShellOperator,
    CreateMidLayersOperator,
    toShellData,
]

def register():
    print('registered') # just for debug
    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    print('unregistered') # just for debug
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

if __name__ == '__main__':
    bpy.utils.register_class(toShellOperator)
    bpy.utils.register_class(CreateMidLayersOperator)
    bpy.utils.register_class(Panel)