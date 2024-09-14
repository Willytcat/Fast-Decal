bl_info = {
    "name": "Fast Decal",
    "author": "William Templemore-Finlayson",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View 3d > Side Panel",
    "description": "Select an image, and object(s), click on the big button, snap, place, rescale, etc., Enjoy",
    "warning": "Still in dev",
}



if "bpy" in locals():
    import importlib
    importlib.reload(CursorHideToggle)
    importlib.reload(EditDecal)
    importlib.reload(FastDecalProperties)
    importlib.reload(InputManager)
    importlib.reload(MoveDecal)
    importlib.reload(NewDecal)
    importlib.reload(RemoveDecal)
    importlib.reload(UIPanel)
else:
    from . import CursorHideToggle
    from . import EditDecal
    from . import FastDecalProperties
    from . import InputManager
    from . import MoveDecal
    from . import NewDecal
    from . import RemoveDecal
    from . import UIPanel

def register():
    CursorHideToggle.register()
    EditDecal.register()
    #FastDecalProperties.register()
    InputManager.register()
    NewDecal.register()
    RemoveDecal.register()
    UIPanel.register()
    MoveDecal.register()

def unregister():
    CursorHideToggle.unregister()
    EditDecal.unregister()
    #FastDecalProperties.unregister()
    InputManager.unregister()
    MoveDecal.unregister()
    NewDecal.unregister()
    RemoveDecal.unregister()
    UIPanel.unregister()

if __name__ == "__main__":
    register()


