import bpy

class CursorHideToggle(bpy.types.Operator):
    """Toggle to hide the cursor in the scene"""
    bl_idname = "decal.cursor_hide_toggle"
    bl_label = "Cursor Hide Toggle"
    
    def execute(self, context):
        inversion = not context.scene.FD.cursor_hided
        context.scene.FD.cursor_hided = inversion
        
        for index, obj in enumerate(bpy.data.objects):
            if obj.get("decal_type") != None:
                obj.hide_viewport = context.scene.FD.cursor_hided
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(CursorHideToggle)


def unregister():
    bpy.utils.unregister_class(CursorHideToggle)


if __name__ == "__main__":
    register()
