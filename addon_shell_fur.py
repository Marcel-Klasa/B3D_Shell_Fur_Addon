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
        self.topShells = {}
        self.nodes = {}
        self.layers = []


data = toShellData()

class toShell():

    ### BUTTON TOP SHELL
    
    def createShell():
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
        self.layout.enabled = len(bpy.context.selected_objects) > 0
        self.layout.operator(toShellOperator.bl_idname, text='Create Shell')
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