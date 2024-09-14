import bpy

bl_info = {
    "name": "Fast Decal",
    "author": "William Templemore-Finlayson",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View 3d > Side Panel",
    "description": "Select an image, and object(s), click on the big button, snap, place, rescale, etc., Enjoy",
    "warning": "Still in dev",
}


def update_decal_preview(img):
    obj = bpy.context.active_object
    if obj != None and obj.get("decal_group") != None:
        decal = obj.get("decal_group")
        
        texture = bpy.data.textures["decalPreviewText"] 
        texture.image = decal.nodes["Image Texture"].image
    
    return None


class DecalAddonUIPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_decal_addonUI_panel"
    
    bl_space_type = "VIEW_3D" 
    bl_region_type = "UI"

    bl_category = "Decal"  # found in the Sidebar
    bl_label = "Decal Addon"  # found at the top of the Panel
    
    updater = True
    
    def draw (self, context):
        
        cursor_hided = context.scene.FD.cursor_hided
        editing = context.scene.FD.editing
        obj = context.active_object
        
        row = self.layout.row()
        row.scale_y = 2
        row.operator("decal.new_decal", text="New Decal !", icon='TEXTURE_DATA')
            
        self.layout.row().separator(factor=0.5)
        
        row = self.layout.row()
        row.prop(context.scene.FD, "principal_input_type", text="Input")
        
        row = self.layout.row()
        row.scale_y = 1.5
        row.prop(context.scene.FD, "principal_input")
        
        row = self.layout.row()
        row.alignment = 'RIGHT'
        row.scale_x = 1
        row.scale_y = 1
        row.operator("decal.input_add", text="", icon="ADD"), row.operator("decal.input_remove", text="", icon="REMOVE")
        
        if len(context.scene.FD_inputs) > 0:
            for i, input in enumerate(context.scene.FD_inputs):
                row = self.layout.row()
                row.prop(input, "type", text="Input")
                row = self.layout.row()
                row.scale_y = 1.5
                row.prop(input, "file_path", text="")
                self.layout.row().separator()
        
        self.layout.row().separator(factor=1)
        
        row = self.layout.row()
        
        if cursor_hided == True:
            hided_icon = 'HIDE_ON'
            #print("hide on")
        else:
            hided_icon = 'HIDE_OFF'
            #print("hide off")
            
        row.operator("decal.cursor_hide_toggle", text="", icon=hided_icon), row.operator("decal.edit_decal", text="", icon='PROPERTIES'), row.operator("decal.move_decal", text="", icon='EMPTY_ARROWS'), row.operator("decal.remove_decal", text="", icon='TRASH')
        row.scale_x = 2
        row.scale_y = 2
        
        if obj != None and obj.get("decal_group") != None and editing == True:
            
            decal = obj["decal_group"]
            row = self.layout.row()
            row.separator()
            
            col = self.layout.box().column()
            col.prop(decal.nodes["Image Texture"], "image", text="Image")
            
            #update_decal_preview()#bpy.data.textures["decalPreviewText"].image = decal.nodes["Image Texture"].image
            #col.template_preview(bpy.data.textures["decalPreviewText"])
            #col.prop(decal.nodes["Image Texture"], "image", text="Image")
            
            col.separator()
            #col.operator("decal.update_decal", text="Update Decal")
            col.prop(decal.nodes["Value"].outputs[0], "default_value", text="Opacity")
            col.prop(decal.nodes["Mapping"].inputs[1], "default_value", text="Location")
            col.prop(decal.nodes["Mapping"].inputs[2], "default_value", text="Rotation")
            col.prop(decal.nodes["Mapping"].inputs[3], "default_value", text="Scale")
            

def register():
    bpy.utils.register_class(DecalAddonUIPanel)


def unregister():
    bpy.utils.unregister_class(DecalAddonUIPanel)


if __name__ == "__main__":
    register()
