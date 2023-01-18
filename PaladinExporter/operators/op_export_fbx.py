import bpy
import os
import json

class Paladin_OT_ExportFbx(bpy.types.Operator):
    bl_idname = "paladin.exportfbx"
    bl_label = "Export FBX"

    @classmethod
    def poll(cls, context):
        export_data = context.scene.exporter
        items = export_data.items_list
        items_values = export_data.items_list.values()

        if getattr(export_data,'path') == "":
            return False
        if len(items) == 0:
            return False
        for value in items_values:
            if value.include_in_export:
                return True
        return False

    @classmethod
    def description(cls, context, event):
        export_data = context.scene.exporter
        items = export_data.items_list
        items_values = export_data.items_list.values()

        if getattr(export_data,'path') == "":
            return "Choose a 'Global Path' first"
        if len(items) == 0:
            return "Add Collections to the export list first"
        for value in items_values:
            if value.include_in_export:
                return "Export all 'Enabled' collections from the export list"
        return "Enable at least one export collection"

    def execute(self, context):
        export_data = context.scene.exporter
        items_values = export_data.items_list.values()
        old_selected = context.selected_objects
        old_active = context.view_layer.objects.active
        old_mode = context.object.mode
        exported_objects = []

        settings_folder = 'presets'
        settings_file = 'fbx_unity_object.json'
        current_path = os.path.dirname(__file__)
        settings_path = os.path.join(os.path.dirname(current_path), settings_folder, settings_file)

        with open(settings_path, 'r') as settings_file:
            self.settings = json.load(settings_file)

        print(self.settings["object_types"])

        bpy.ops.object.mode_set(mode='OBJECT')
        
        for item_value in items_values:
            if item_value.include_in_export == False:
                continue
            collection = bpy.data.collections[item_value.collection_name]
            if collection is None:
                print("collection not found! " + item_value.collection_name)
                continue
            
            parent_objects = []
            
            ## Find all top level objects in collection
            for obj in collection.objects:
                if obj.parent == None and obj.type in ('MESH','EMPTY','ARMATURE'):
                    parent_objects.append(obj)
                
            for obj in parent_objects:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                context.view_layer.objects.active = obj
                bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
                filename = obj.name
                
                #if export_data.bake_animation:
                #    filename += export_data.filename_suffix

                filename += ".fbx"
                
                exported_objects.append(filename)
                old_location = obj.location.copy()

                if not item_value.use_object_origin:
                    obj.location = (0,0,0)

                export_path = item_value.custom_path + filename
                if not item_value.use_custom_path or item_value.custom_path == "":
                    export_path = export_data.path + filename

                bpy.ops.export_scene.fbx(
                    filepath=bpy.path.abspath(export_path),
                    batch_mode=(self.settings["batch_mode"]),
                    check_existing=(self.settings["check_existing"]),
                # Include
                    use_selection=True,
                    use_visible=(self.settings["use_visible"]),
                    use_active_collection=(self.settings["use_active_collection"]),
                    object_types=set(self.settings["object_types"]),
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
            self.report({'ERROR'},"No objects in exported collections!")
        elif length == 1:
            self.report({'INFO'},"1 object was exported")
        else:
            self.report({'INFO'},f"{length} objects were exported")

        # Resetting selected/active objects and mode:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in old_selected:
            obj.select_set(True)
        context.view_layer.objects.active = old_active
        bpy.ops.object.mode_set(mode=old_mode)
                
        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
