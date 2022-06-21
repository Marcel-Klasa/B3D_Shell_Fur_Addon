bl_info = {
    # required
    'name': 'Fur Shell Addon',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 1),
    'author': 'Marcel Klasa',
}

import bpy, copy

height = 0.3

class toShell():
    def createShell():
        act_obj = bpy.context.active_object
        new_obj = bpy.data.objects.new('Top_Shell', act_obj.data.copy())
        bpy.context.collection.objects.link(new_obj)

        for v in new_obj.data.vertices:
            v.co += v.normal * height

class toShellOperator(bpy.types.Operator):
    
    bl_idname = 'opr.to_shell_operator'
    bl_label = 'To Shell'
    
    def execute(self, context):
        
        toShell.createShell()
            
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
        self.layout.operator(toShellOperator.bl_idname, text='Create Shell')

CLASSES = [
    Panel,
    toShell,
    toShellOperator,
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
    bpy.utils.register_class(Panel)