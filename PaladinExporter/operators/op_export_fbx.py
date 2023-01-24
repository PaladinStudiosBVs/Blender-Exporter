import bpy
import os
import json
from ..utilities.general import preset_path_get, is_collection_valid, has_export_sets, has_sets_include, included_sets_has_item

class Paladin_OT_ExportFbx(bpy.types.Operator):
    bl_idname = "paladin.exportfbx"
    bl_label = "Export FBX"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if not bpy.data.is_saved:
            return False
        if not has_export_sets():
            return False
        if not has_sets_include():
            return False
        if not included_sets_has_item():
            return False   
        return True
    
    @classmethod
    def description(cls, context, event):
        if not bpy.data.is_saved:
            return "Save the file before Exporting"
        if not has_export_sets():
            return "Create at least one Export Set"
        if not has_sets_include():
            return "Enable at least one Export Set"
        if not included_sets_has_item():
            return "Add items to the enabled Export Set(s)"
        return "Export items from the export sets"

    def execute(self, context):
        export_data = context.scene.exporter
        export_sets = export_data.sets
        preset_path = preset_path_get()
        old_selected = context.selected_objects
        
        if len(old_selected) > 0:
            old_active = context.view_layer.objects.active
            old_mode = context.object.mode

        exported_objects = []
        
        for export_set in export_sets:
            if export_set.set_include == False:
                continue
            with open(os.path.join(preset_path, export_set.set_preset), 'r') as preset_setting:
                self.settings = json.load(preset_setting)

            for item in export_set.items:
                if item.item_include == False:
                    continue
                
                if not is_collection_valid(item.item_name):
                    print(f"Collection not found: '{item.item_name}'")
                    continue
                collection = bpy.data.collections[item.item_name]
                
                parent_objects = []
                for obj in collection.objects:
                    if obj.parent == None and obj.type in ('MESH','EMPTY','ARMATURE') and obj.visible_get() == True:
                        parent_objects.append(obj)
                
                if len(parent_objects) == 0:
                    continue
                
                old_mode = context.object.mode
                bpy.ops.object.mode_set(mode='OBJECT')

                for obj in parent_objects:
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    context.view_layer.objects.active = obj
                    bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
                    old_location = obj.location.copy()
                    if not item.item_use_origin:
                        obj.location = (0,0,0)
                    
                    # Defining file name and export location:
                    filename = f"{export_set.set_prefix}{obj.name}{export_set.set_suffix}.fbx"
                    exported_objects.append(filename)
                    
                    export_path = os.path.join(os.path.dirname(bpy.data.filepath), filename)
                    if item.item_use_path and not item.item_path == "":
                        export_path = os.path.join(item.item_path, filename)
                    elif not export_set.set_path == "":
                        export_path = os.path.join(export_set.set_path, filename)
                    
                    bpy.ops.export_scene.fbx(
                        filepath=bpy.path.abspath(export_path),
                    # Hard Coded
                        batch_mode= "OFF",
                        check_existing= False,
                        use_selection=True,
                        use_active_collection=False,
                    # Include
                        use_visible=(self.settings["use_visible"]),
                        object_types= set(self.settings["object_types"]),
                        use_custom_props=(self.settings["use_custom_props"]),
                    # Transform
                        global_scale=(self.settings["global_scale"]),
                        apply_scale_options=(self.settings["apply_scale_options"]),
                        axis_forward=(self.settings["axis_forward"]),
                        axis_up =(self.settings["axis_up"]),
                        apply_unit_scale=(self.settings["apply_unit_scale"]),
                        use_space_transform=(self.settings["use_space_transform"]),
                        bake_space_transform=(self.settings["bake_space_transform"]),
                    # Geometry
                        mesh_smooth_type=(self.settings["mesh_smooth_type"]),
                        use_subsurf=(self.settings["use_subsurf"]),
                        use_mesh_modifiers=(self.settings["use_mesh_modifiers"]),
                        use_mesh_edges=(self.settings["use_mesh_edges"]),
                        use_triangles=(self.settings["use_triangles"]),
                        use_tspace=(self.settings["use_tspace"]),
                        colors_type=(self.settings["colors_type"]),
                    # Armature
                        primary_bone_axis=(self.settings["primary_bone_axis"]),
                        secondary_bone_axis=(self.settings["secondary_bone_axis"]),
                        armature_nodetype=(self.settings["armature_nodetype"]),
                        use_armature_deform_only=(self.settings["use_armature_deform_only"]),
                        add_leaf_bones=(self.settings["add_leaf_bones"]),
                    # Animation
                        bake_anim=(self.settings["bake_anim"]),
                        bake_anim_use_all_bones=(self.settings["bake_anim_use_all_bones"]),
                        bake_anim_use_nla_strips=(self.settings["bake_anim_use_nla_strips"]),
                        bake_anim_use_all_actions=(self.settings["bake_anim_use_all_actions"]),
                        bake_anim_force_startend_keying=(self.settings["bake_anim_force_startend_keying"]),
                        bake_anim_step=(self.settings["bake_anim_step"]),
                        bake_anim_simplify_factor=(self.settings["bake_anim_simplify_factor"])
                        )

                    obj.location = old_location
        
        # Reporting number of exported objects:
        length = len(exported_objects)
        if length == 0:
            self.report({'ERROR'},"No objects were exported")
        elif length == 1:
            self.report({'INFO'},"One object was exported")
        else:
            self.report({'INFO'},f"{length} objects were exported")

        # Resetting selected/active objects and mode:
        bpy.ops.object.select_all(action='DESELECT')
        
        if len(old_selected) > 0:
            for obj in old_selected:
                obj.select_set(True)
            context.view_layer.objects.active = old_active
            bpy.ops.object.mode_set(mode=old_mode)

        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
