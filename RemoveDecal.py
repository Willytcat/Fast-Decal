import bpy

class RemoveDecal(bpy.types.Operator):
    """Remove a decal cursor and his node_group"""
    bl_idname = "decal.remove_decal"
    bl_label = "Remove Decal"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        global edited_decal
        
        if obj.get("decal_type") != None and obj["decal_group"] != None:
            decal_group = obj["decal_group"]
            
            # remove all the decal_group_node of this node group in every material
            for idx, mat in enumerate(bpy.data.materials):
                if mat.use_nodes == True:
                    for node in mat.node_tree.nodes:
                        if node.type == 'GROUP' and node.node_tree == decal_group:
                            # find the sockets and the node next to the group
                            from_socket, to_socket, to_node = node.inputs['Shader'].links[0].from_socket, node.outputs['Shader'].links[0].to_socket, node.outputs['Shader'].links[0].to_node
                            to_node.location.x = to_node.location.x - 200
                            
                            # remove links and the node group
                            mat.node_tree.links.remove(node.inputs['Shader'].links[0])
                            mat.node_tree.links.remove(node.outputs['Shader'].links[0])
                            mat.node_tree.nodes.remove(node)
                            
                            mat.node_tree.links.new(from_socket, to_socket)
            
            # remove the cursor and the node_group data       
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.node_groups.remove(decal_group)
            bpy.data.objects.remove(obj)
            
            # update the ui
            context.scene.FD.editing = False
            context.region.tag_redraw()
            
            bpy.context.view_layer.update()
                    
        elif obj.get("decal_group") != None and obj["decal_group"] == None:
            self.report({'WARNING'}, "This cursor does not seem to have an associated node group")
            bpy.data.objects.remove(obj)
        else:
            self.report({'INFO'}, "This is not a decal cursor")
            
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(RemoveDecal)


def unregister():
    bpy.utils.unregister_class(RemoveDecal)

if __name__ == "__main__":
    register()
