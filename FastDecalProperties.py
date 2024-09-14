import bpy

BSDFInputs = [
    ("0", "Base Color", ""),
    ("1", "Metallic", ""),
    ('2', "Roughness", ""),
    ('3', "IOR", ""),
    ('4', "Alpha", ""),
    ('5', "Normal", ""),
    ('6', "Weight", ""),
    ('7', "Subsurface Weight", ""),
    ('8', "Subsurface Radius", ""),
    ('9', "Subsurface Scale", ""),
    ('10', "Subsurface IOR", ""),
    ('11', "Subsurface Anisotropy", ""),
    ('12', "Specular IOR Level", ""),
    ('13', "Specular Tint", ""),
    ('14', "Anisotropic Rotation", ""),
    ('15', "Tangent", ""),
    ('16', "Transmission Weight", ""),
    ('17', "Coat Weight", ""),
    ('18', "Coat Roughness", ""),
    ('19', "Coat IOR", ""),
    ('20', "Coat Tint", ""),
    ('21', "Coat Normal", ""),
    ('22', "Sheen Weight", ""),
    ('23', "Sheen Roughness", ""),
    ('24', "Sheen Tint", ""),
    ('25', "Emission Color", ""),
    ('26', "Emission Strength", ""),
]

class FastDecalProperties(bpy.types.PropertyGroup):
    editing: bpy.props.BoolProperty()
    cursor_hided: bpy.props.BoolProperty()
    principal_input_type: bpy.props.EnumProperty(name="Input Type", items=BSDFInputs)
    principal_input: bpy.props.StringProperty(name="", subtype='FILE_PATH')

class DecalFilePaths(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(name="Input Type", items=BSDFInputs)
    file_path: bpy.props.StringProperty(name="Input Filepath", subtype='FILE_PATH')

# ajouter le principal input et le retirer de la pointer property

options = [
    ('OPT1', "Option 1", "Première option"),
    ('OPT2', "Option 2", "Deuxième option"),
    ('OPT3', "Option 3", "Troisième option"),
]

bpy.utils.register_class(FastDecalProperties)
bpy.utils.register_class(DecalFilePaths)

bpy.types.Scene.FD = bpy.props.PointerProperty(type=FastDecalProperties)
bpy.types.Scene.FD_inputs = bpy.props.CollectionProperty(type=DecalFilePaths)

