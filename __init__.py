bl_info = {
    "name": "Reload UI",
    "author": "Samuel Bernou",
    "version": (0, 2, 0),
    "blender": (2, 81, 0),
    "location": "Ctrl + Alt + Shift + N",
    "description": "Reload file with your own UI",
    "warning": "",
    "wiki_url": "https://github.com/Pullusb/reloadUI",
    "tracker_url": "https://github.com/Pullusb/reloadUI/issues",
    "category": "System"}

import bpy
from bpy.utils import register_class, unregister_class

def timeline_view_all(all_view=True):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'DOPESHEET_EDITOR': #TIMELINE
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'window': window, 'screen': window.screen, 'area': area, 'region': region}
                        bpy.ops.action.view_all(override) # bpy.ops.time.view_all(override)
                        if not all_view:
                            break

def go_camera_view(all_view=True):
    for window in bpy.context.window_manager.windows:
         for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                if not all_view:
                    break


class RUI_OT_Reload_with_startup_UI_OP(bpy.types.Operator):
    bl_idname = "utils.reload_with_startup_ui"
    bl_label = "Revert with startup UI"
    bl_description = "reload the file with own startup file UI"
    bl_options = {"REGISTER"}

    def execute(self, context):
        #move weirdly current frame so save and re-apply
        f = bpy.context.scene.frame_current
        my_file = bpy.data.filepath#get the filepath of the blend
        bpy.ops.wm.read_homefile()#start new file (load startup file)
        bpy.ops.wm.open_mainfile(filepath=my_file, load_ui=False)#reload file with load UI off
        bpy.context.scene.frame_set(f)
        
        # PROBLEM : keeps reverting and opening recent-file without loading UI...
        #Solution : refresh load_UI pref
        bpy.context.preferences.filepaths.use_load_ui = bpy.context.preferences.filepaths.use_load_ui
        
        ## set timeline to see anim regions
        timeline_view_all()

        # Go in camera if active
        #bpy.context.scene.update()
        if bpy.context.scene.camera:
            #activate cam view
            go_camera_view()
        return {"FINISHED"}


## to add in a panel :
#layout.operator('utils.reload_with_startup_ui', icon=FILE_REFRESH)#MOD_WIREFRAME#RENDERLAYERS#no button for now


###---keymap---------------

addon_keymaps = []
def register_keymaps():
    addon = bpy.context.window_manager.keyconfigs.addon
    #km = addon.keymaps.new(name = "3D View", space_type = "VIEW_3D")#viewD only
    km = addon.keymaps.new(name = "Window",space_type='EMPTY', region_type='WINDOW')#all view
    kmi = km.keymap_items.new("utils.reload_with_startup_ui", type = "N", value = "PRESS", shift = True, alt =True, ctrl = True)
    addon_keymaps.append((km, kmi))

def unregister_keymaps():
    # wm = bpy.context.window_manager
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


###---register--------------

#classes = (RUI_OT_Reload_with_startup_UI_OP)

def register():
    if not bpy.app.background:
        register_class(RUI_OT_Reload_with_startup_UI_OP)
        # for cls in classes:
        #     register_class(cls)
        register_keymaps()

def unregister():
    if not bpy.app.background:
        unregister_keymaps()
        unregister_class(RUI_OT_Reload_with_startup_UI_OP)
        # for cls in reversed(classes):
        #     unregister_class(cls)
        

if __name__ == "__main__":
    register()
