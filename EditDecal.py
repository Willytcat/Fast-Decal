import bpy


def update_decal_preview(context, image):
    if bpy.data.textures.get("decalPreviewText"):
        bpy.data.textures.remove(bpy.data.textures["decalPreviewText"])
        bpy.data.textures.new(name="decalPreviewText", type="IMAGE")
        texture = bpy.data.textures["decalPreviewText"]
    else:
        bpy.data.textures.new(name="decalPreviewText", type="IMAGE")
        texture = bpy.data.textures["decalPreviewText"]
            
    texture.image = image
    
    return texture


class EditDecal(bpy.types.Operator):
    """Edit selected decal properties"""
    bl_idname = "decal.edit_decal"
    bl_label = "Edit Decal"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        editing = context.scene.FD.editing
        
        if obj.get("decal_type") != None and obj["decal_group"] != None:
            edited = obj["decal_group"]
            
            if editing == False:
                context.scene.FD.editing = True
                update_decal_preview(context, edited.nodes['Image Texture'].image)
                context.region.tag_redraw()
            else:
                context.scene.FD.editing = False
                context.region.tag_redraw()
            
        elif obj.get("decal_type") != None and obj["decal_group"] == None:
            context.scene.FD.editing = False
            context.region.tag_redraw()
            self.report({'WARNING'}, "This cursor does not seem to have an associated node group")
            bpy.data.objects.remove(obj)
        else:
            context.scene.FD.editing = False
            context.region.tag_redraw()
            #update_ui(context)
            self.report({'INFO'}, "This is not a decal cursor")
        
        return {'FINISHED'}
    
    
def register():
    bpy.utils.register_class(EditDecal)


def unregister():
    bpy.utils.unregister_class(EditDecal)


if __name__ == "__main__":
    register()
