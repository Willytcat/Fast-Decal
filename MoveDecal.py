import bpy
import mathutils
from mathutils import Vector, Matrix
from bpy_extras import view3d_utils


def adapt_matrix(selobj):

    # Rotating / panning / zooming 3D view is handled here.
    # Creates a matrix.
    if selobj.rotation_mode == "AXIS_ANGLE":
        # object rotation_quaternionmode axisangle
        ang, x, y, z =  selobj.rotation_axis_angle
        matrix = Matrix().Rotation(-ang, 4, Vector((x, y, z)))
    elif selobj.rotation_mode == "QUATERNION":
        # object rotation_quaternionmode euler
        w, x, y, z = selobj.rotation_quaternion
        x = -x
        y = -y
        z = -z
        quat = Quaternion([w, x, y, z])
        matrix = quat.to_matrix()
        matrix.resize_4x4()
    else:
        # object rotation_quaternionmode euler
        ax, ay, az = selobj.rotation_euler
        mat_rotX = Matrix().Rotation(-ax, 4, 'X')
        mat_rotY = Matrix().Rotation(-ay, 4, 'Y')
        mat_rotZ = Matrix().Rotation(-az, 4, 'Z')
        if selobj.rotation_mode == "XYZ":
            matrix = mat_rotX @ mat_rotY @ mat_rotZ
        elif selobj.rotation_mode == "XZY":
            matrix = mat_rotX @ mat_rotZ @ mat_rotY
        elif selobj.rotation_mode == "YXZ":
            matrix = mat_rotY @ mat_rotX @ mat_rotZ
        elif selobj.rotation_mode == "YZX":
            matrix = mat_rotY @ mat_rotZ @ mat_rotX
        elif selobj.rotation_mode == "ZXY":
            matrix = mat_rotZ @ mat_rotX @ mat_rotY
        elif selobj.rotation_mode == "ZYX":
            matrix = mat_rotZ @ mat_rotY @ mat_rotX
    # handle object scaling
    sx, sy, sz = selobj.scale
    mat_scX = Matrix().Scale(sx, 4, Vector([1, 0, 0]))
    mat_scY = Matrix().Scale(sy, 4, Vector([0, 1, 0]))
    mat_scZ = Matrix().Scale(sz, 4, Vector([0, 0, 1]))
    matrix = mat_scX @ mat_scY @ mat_scZ @ matrix

    return matrix


def cursor_pos(context, event):
        
    viewport_region = context.region
    viewport_region_data = context.space_data.region_3d
    viewport_matrix = viewport_region_data.view_matrix.inverted()
        
    # Shooting a ray from the camera, through the mouse cursor towards the grid with a length of 100000
    # If the camera is more than 100000 units away from the grid it won't detect a point
    ray_start = viewport_matrix.to_translation()
    ray_depth = viewport_matrix @ Vector((0,0,-100000))
        
    # Get the 3D vector position of the mouse
    ray_end = view3d_utils.region_2d_to_location_3d(viewport_region,viewport_region_data, (event.mouse_region_x, event.mouse_region_y), ray_depth)
        
    # A triangle on the grid plane. We use these 3 points to define a plane on the grid
    point_1 = Vector((0,0,1))
    point_2 = Vector((0,1,0))
    point_3 = Vector((1,0,0))
        
    # Create a 3D position on the grid under the mouse cursor using the triangle as a grid plane
    # and the ray cast from the camera
    position_on_grid = mathutils.geometry.intersect_ray_tri(point_1,point_2,point_3,ray_end,ray_start,False)
    
    if position_on_grid == None:
        return Vector((0, 0, 0))
    
    return position_on_grid


def cursor_ray_cast(context, event):
        
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y
        
    direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    # Same as the view3d_utils.region_2d_to_origin_3d
    origin = context.space_data.region_3d.view_matrix.inverted().translation#view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    
    
    depsgraph = context.evaluated_depsgraph_get()
    depsgraph.update()
    
    result, location, normal, index, ray_object, matrix = scene.ray_cast(depsgraph, origin, direction)
    
    if result == True:
        depsgraph.update()
        evaluated_ray_object = ray_object.evaluated_get(depsgraph)#adapt(ray_object)#
        
        globalcoordinate = Vector((0, 0, 0))
        localcoordinateforobject = location @ adapt_matrix(evaluated_ray_object).inverted()
        
        normal_rotation_euler = Vector((0, 0, 1)).rotation_difference(evaluated_ray_object.data.polygons[index].normal).to_euler() #* adapt(evaluated_ray_object).inverted().to_euler()
        #normal_rotation_euler2 = normal_rotation_euler1.to_quaternion().rotation_difference(adapt(ray_object).to_euler()).to_euler()# difference again
        localcoordinateforobject
        
        return result, localcoordinateforobject, normal_rotation_euler, index, evaluated_ray_object, matrix, depsgraph
    else:
        return result, location, normal, index, ray_object, matrix, depsgraph
    


class MoveDecal(bpy.types.Operator):
    """Move a decal cursor and automatically snap it to other surfaces"""
    bl_idname = "decal.move_decal"
    bl_label = "Move Decal"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def modal(self, context, event):
        global editing
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            # allow navigation
            return {'PASS_THROUGH'}
        elif event.type == 'MOUSEMOVE':
            result, location, normal, index, ray_object, matrix, depsgraph = cursor_ray_cast(context, event)
            self.cursor_parent = ray_object
            
            if result == True and self.snapping == True:
                self.cursor.location = location
                self.cursor.rotation_euler = normal
                #self.cursor.rotation_euler.y = -1.5708
            else:
                pos = cursor_pos(context, event)
                self.cursor.location = pos
                #self.cursor.rotation_euler.y = -1.5708
            return {'RUNNING_MODAL'}
        elif event.type == 'LEFTMOUSE':
            self.cursor.hide_viewport = False
            editing = False
            bpy.ops.decal.edit_decal()
            return {'FINISHED'}
        elif event.type in {'LEFT_CTRL', 'RIGHT_CTRL'}:
            snapping_inverse = not self.snapping
            self.snapping = snapping_inverse
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            #bpy.ops.decal.remove_decal()
            self.cursor.location = self.init_pos
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.cursor = context.active_object
        self.init_pos = self.cursor.location
        
        self.snapping = True
        
        if self.cursor.get("decal_group") == None:
            self.report({'INFO'}, "Only a decal cursor can be moved !")
            return {'CANCELLED'}
        
        self.cursor.location = cursor_pos(context, event)
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(MoveDecal)


def unregister():
    bpy.utils.unregister_class(MoveDecal)


if __name__ == "__main__":
    register()
