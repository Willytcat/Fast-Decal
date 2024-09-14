import bpy
import mathutils
from mathutils import Vector, Matrix


def adapt_ratio(cursor, image):
    init_cursor_scale = cursor.scale
    cursor.scale = Vector(((image.size[1] / 1000), (image.size[0] / 1000), init_cursor_scale[2]))
    
def find_free_bump(bump_node, nodes):
    for i, node in enumerate(nodes):
        if node.type == 'BUMP' and bump_node != node and node.inputs[3].is_linked == False:
            return node
    return nodes['Principled BSDF']

def create_decal_node_group(self, context, cursor):
        
        #for mat in bpy.data.materials:
            #for node in mat.node_tree.nodes: #Unselect the others nodes in all the mat
                #node.select = False
            
        image = bpy.data.images.load(bpy.context.scene.FD.principal_input, check_existing=True)
        
        # create a group
        decal_node_group = bpy.data.node_groups.new(image.name, 'ShaderNodeTree')
        
        # create group inputs
        group_inputs = decal_node_group.nodes.new('NodeGroupInput')
        group_inputs.location = (800,0)
        
        # create group outputs
        group_outputs = decal_node_group.nodes.new('NodeGroupOutput')
        group_outputs.location = (1400,0)
        
        #adding the sockects 'Shader' input and output
        decal_node_group.interface.new_socket('Shader', in_out='INPUT', socket_type='NodeSocketShader')
        decal_node_group.interface.new_socket('Shader', in_out='OUTPUT', socket_type='NodeSocketShader')
        
        bpy.context.view_layer.update()
        
        nodes = decal_node_group.nodes
        links = decal_node_group.links    
        
        
        #create Mix Shader node
        mix_shader = nodes.new("ShaderNodeMixShader")
        mix_shader.location.x = +1100
        mix_shader.location.y = +100
        
        #create Texture Coordinate node
        text_coor = nodes.new("ShaderNodeTexCoord")
        text_coor.location.x = -450
        text_coor.location.y = -50
        text_coor.object = cursor
        
        #create Mapping node
        mapping = nodes.new("ShaderNodeMapping")
        mapping.location.x = -250
        mapping.location.y = -100
        mapping.inputs[1].default_value = Vector((0.5, 0.5, 0.5))
        mapping.inputs[3].default_value = Vector((0.5, 0.5, 0.5))
        mapping.inputs[2].default_value[2] = -1.5708

        
        #create Separate XYZ node
        separate_xyz = nodes.new("ShaderNodeSeparateXYZ")
        separate_xyz.location.x = -250
        separate_xyz.location.y = 100
        
        #create Less Than node
        greater_than = nodes.new("ShaderNodeMath")
        greater_than.operation = 'GREATER_THAN'
        greater_than.inputs[1].default_value = -1
        greater_than.location.x = -75
        greater_than.location.y = +200
        
        #create Greater Than node
        less_than = nodes.new("ShaderNodeMath")
        less_than.operation = 'LESS_THAN'
        less_than.inputs[1].default_value = 1
        less_than.location.x = -75
        less_than.location.y = +50
        
        #create Mix node
        mix = nodes.new("ShaderNodeMix")
        mix.data_type = 'RGBA'
        mix.location.x = +775
        mix.location.y = -200
        mix.hide = True
        
        #create Multiply node
        multiply_1 = nodes.new("ShaderNodeMix")
        multiply_1.data_type = 'RGBA'
        multiply_1.blend_type = 'MULTIPLY'
        multiply_1.location.x = +150
        multiply_1.location.y = +200
        multiply_1.inputs[0].default_value = 1.000

        #create Multiply node
        multiply_2 = nodes.new("ShaderNodeMix")
        multiply_2.data_type = 'RGBA'
        multiply_2.blend_type = 'MULTIPLY'
        multiply_2.location.x = +350
        multiply_2.location.y = -150
        multiply_2.inputs[0].default_value = 1.000
        
        #create Principled BSDF node
        principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf.location.x = +500
        principled_bsdf.location.y = +175
        
        
        text_img = nodes.new("ShaderNodeTexImage")
        text_img.location.y = -200
        text_img.extension = 'CLIP'
        text_img.image = image
        adapt_ratio(cursor, image)
        
        l = links
        principal_input = bpy.context.scene.FD.principal_input
        
        if not principal_input.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tga')):
            principal_input = ""
            bpy.ops.decal.remove_decal()
            return {'CANCELLED'}
        
        #set the principal input
        if int(bpy.context.scene.FD.principal_input_type) == 5:
            bump_node = nodes.new("ShaderNodeBump")
            bump_node.location.x = 100
            bump_node.location.y = -200
            
            l.new(text_img.outputs[0], bump_node.inputs['Height'], verify_limits=True)
            l.new(text_img.outputs[1], multiply_2.inputs['B'], verify_limits=True)
            l.new(bump_node.outputs[0], find_free_bump(bump_node, nodes).inputs["Normal"], verify_limits=True)
            l.new(mapping.outputs[0], text_img.inputs[0])
            
        else:
            l.new(text_img.outputs[0], principled_bsdf.inputs[int(bpy.context.scene.FD.principal_input_type)], verify_limits=True)
            l.new(text_img.outputs[1], multiply_2.inputs['B'], verify_limits=True)
            l.new(mapping.outputs[0], text_img.inputs[0])
        
        
        if len(bpy.context.scene.FD_inputs) > 0:
            node_loc = -200
            for i, input in enumerate(bpy.context.scene.FD_inputs):
                node_loc -= 200
                # check if its an image
                if input.file_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tga')) == False:
                    self.report({'WARNING'}, "Only image type file (.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tga) can be imported !")
                    input.file_path = ""
                    continue
                
                image = bpy.data.images.load(input.file_path, check_existing=True)
                text_img = nodes.new("ShaderNodeTexImage")
                text_img.location.y = node_loc
                text_img.extension = 'CLIP'
                text_img.image = image
                
                if int(input.type) == 5:
                    bump_node = nodes.new("ShaderNodeBump")
                    bump_node.location.x = 100
                    bump_node.location.y = node_loc
            
                    l.new(text_img.outputs[0], bump_node.inputs['Height'], verify_limits=True)
                    l.new(bump_node.outputs[0], find_free_bump(bump_node, nodes).inputs["Normal"], verify_limits=True)
                    l.new(mapping.outputs[0], text_img.inputs[0])
            
                else:
                    l.new(text_img.outputs[0], principled_bsdf.inputs[int(input.type)], verify_limits=True)
                    l.new(mapping.outputs[0], text_img.inputs[0])
            
        
        #create Invert node
        invert = nodes.new("ShaderNodeInvert")
        invert.location.x = +575
        invert.location.y = -150
        
        #create Value node
        value_node = nodes.new("ShaderNodeValue")
        value_node.location.x = +775
        value_node.location.y = -230
        value_node.outputs[0].default_value = 0.5
        
        #create the links between the nodes above
        
        l.new(text_coor.outputs[3], separate_xyz.inputs[0])
        l.new(text_coor.outputs[3], mapping.inputs[0])
        
        l.new(separate_xyz.outputs[2], greater_than.inputs[0])
        l.new(separate_xyz.outputs[2], less_than.inputs[0])
        
        l.new(greater_than.outputs[0], multiply_1.inputs['A'])
        l.new(less_than.outputs[0], multiply_1.inputs['B'])
        
        l.new(multiply_1.outputs['Result'], multiply_2.inputs['A'])
        
        l.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
        
        l.new(multiply_2.outputs['Result'], invert.inputs['Color'])
        
        l.new(invert.outputs[0], mix.inputs[0])
        l.new(invert.outputs[0], mix.inputs['B'])
        
        l.new(value_node.outputs[0], mix.inputs['A'])
        
        l.new(mix.outputs['Result'], mix_shader.inputs[0])
        
        l.new(group_inputs.outputs[0], mix_shader.inputs[2])
        l.new(mix_shader.outputs[0], group_outputs.inputs[0])
        
        
        return decal_node_group

def mat_setup(self, context, cursor, image_fpath):
    
    decal_node_group = create_decal_node_group(self, context, cursor)
    if decal_node_group == {'CANCELLED'}:
        self.report({'WARNING'}, "Only image type file (.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tga) can be imported !")
        return decal_node_group
    
    decal_node_group["decal_type"] = "Decal_Group"
    cursor["decal_type"] = "Decal_Cursor"
    
    cursor["decal_group"] = decal_node_group
    decal_node_group["decal_cursor"] = cursor
        
    bpy.context.view_layer.update()
        
    for obj_index, obj in enumerate(context.selected_objects):
        if obj.type == 'MESH' and len(obj.material_slots) > 0:
            print(obj.name)
            for mat_index, slot in enumerate(obj.material_slots):
                print(slot.name)
                material = slot.material
                
                material.use_nodes = True
                obj.active_material_index = mat_index
                    
                node_tree = material.node_tree
                node_group = node_tree.nodes.new('ShaderNodeGroup')
                node_group.node_tree = decal_node_group
                
                # get the mat output of the node_tree
                material_output = node_tree.get_output_node('ALL')
                    
                #check if a link is relied to the mat output and link the decal group node to it
                for link_index, link in enumerate(node_tree.links):
                   # check for a link between the mat output and a shader
                    if link.to_socket == material_output.inputs[0] or link.to_socket == material_output.inputs["Surface"]:
                        #find the node relied to the mat output
                        socket_before_mat_output = node_tree.links[link_index].from_socket
                            
                        #move the mat output and decal node group
                        node_group.location = material_output.location
                        material_output.location.x = material_output.location.x + 200
                            
                        #remove the link
                        node_tree.links.remove(node_tree.links[link_index])
                            
                        # and link the node group
                        node_tree.links.new(socket_before_mat_output, node_group.inputs['Shader'])
                        node_tree.links.new(node_group.outputs['Shader'], material_output.inputs['Surface'])
                            
                        break
            return decal_node_group
                        
        elif obj.type == 'MESH' and len(obj.material_slots) <= 0:
            return None
        


class NewDecal(bpy.types.Operator):
    """Select object(s) and click here to apply a decal"""
    bl_idname = "decal.new_decal"
    bl_label = "New Decal"
    
    #first_mouse_x: IntProperty()
    #first_value: FloatProperty()
    def new_cursor(self, context):
        #bpy.ops.object.empty_add(type='CUBE')
        cursor = bpy.data.objects.new(name="Decal", object_data=None)
        scene_collection = context.layer_collection.collection
        scene_collection.objects.link(cursor)
        cursor.empty_display_type = 'CUBE'
        cursor.scale = Vector((1, 1, 0.1))
    
        return cursor
    

    def execute(self, context):
        print("New Decal")
        
        self.cursor = self.new_cursor(context)
        self.decal_node = mat_setup(self, context, self.cursor, context.scene.FD.principal_input)
        self.cursor_parent = None
        
        # check if mat_setup return None wich provide an error
        if self.decal_node == None:
            if len(context.selected_objects) <= 0:
                msg = "You need to select object(s) for the addon to work"
            else:
                msg = "All selected objects must have a material!"
            bpy.ops.object.select_all(action='DESELECT')
            self.cursor.select_set(True)
            bpy.context.view_layer.objects.active = self.cursor
            self.report({'WARNING'}, msg)
            bpy.ops.decal.remove_decal()
            return {'CANCELLED'}
        
        bpy.ops.object.select_all(action='DESELECT')
        self.cursor.select_set(True)
        bpy.context.view_layer.objects.active = self.cursor
        
        bpy.ops.decal.move_decal('INVOKE_DEFAULT')
        
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(NewDecal)
    
    
    
def unregister():
    bpy.utils.unregister_class(NewDecal)


if __name__ == "__main__":
    register()
