import bpy

class NewDecalInput(bpy.types.Operator):
    """Add an filepath input"""
    bl_idname = "decal.input_add"
    bl_label = "Add Input"
    
    def execute(self, context):
        context.scene.FD_inputs.add()
        return {'FINISHED'}
    

class RemoveDecalInput(bpy.types.Operator):
    """Remove the last filepath input"""
    bl_idname = "decal.input_remove"
    bl_label = "Remove Input"
    
    def execute(self, context):
        idx = len(context.scene.FD_inputs)
        if idx > 0:
            context.scene.FD_inputs.remove(idx-1)
        return {'FINISHED'}
    


def register():
    bpy.utils.register_class(NewDecalInput)
    bpy.utils.register_class(RemoveDecalInput)


def unregister():
    bpy.utils.unregister_class(NewDecalInput)
    bpy.utils.unregister_class(RemoveDecalInput)


if __name__ == "__main__":
    register()
