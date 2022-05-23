bl_info = {
    # required
    'name': 'Fur Shell Addon',
    'blender': (2, 80, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 0),
    'author': 'Marcel Klasa',
}

import bpy, copy

height = 0.3

class toShell():

    bl_idname = 'opr.to_shell'
    bl_label = 'To Shell'

    def createShell():
        act_obj = bpy.context.active_object
        new_obj = bpy.data.objects.new('Top_Shell', act_obj.data.copy())
        bpy.context.collection.objects.link(new_obj)

        for v in new_obj.data.vertices:
            v.co += v.normal * height

class toShellOperator(bpy.types.Operator):
    
    bl_idname = 'opr.to_shell_operator'
    bl_label = 'To Shell opr'
    
    def execute(self, context):
        
        toShell.createShell()
            
        return {'FINISHED'}

class Panel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_example_panel'
    bl_label = 'Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        self.layout.label(text='Hello there')
        col = self.layout.column()
        self.layout.operator(toShellOperator.bl_idname, text='Shellize')

CLASSES = (
    Panel,
    toShellOperator,
)

def register():
    #print('registered') # just for debug
    from bpy.utils import register_class
    for clss in CLASSES:
        bpy.utils.register_class(clss)

def unregister():
    #print('unregistered') # just for debug
    from bpy.utils import unregister_class
    for clss in reversed(CLASSES):
        bpy.utils.unregister_class(clss)

#if __name__ == '__main__':
#    bpy.utils.register_class(toShellOperator)
#    bpy.utils.register_class(Panel)