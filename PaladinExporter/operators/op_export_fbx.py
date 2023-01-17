import bpy

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
                

                if export_data.bake_animation:
                    filename += export_data.filename_suffix

                filename += ".fbx"
                
                exported_objects.append(filename)

                old_location = obj.location.copy()

                if not item_value.use_object_origin:
                    obj.location = (0,0,0)

                types_to_export = {}
                if export_data.include_meshes:
                    types_to_export = {'ARMATURE','MESH','EMPTY'}
                else:
                    types_to_export = {'ARMATURE','EMPTY'}

                export_path = item_value.custom_path + filename
                if not item_value.use_custom_path or item_value.custom_path == "":
                    export_path = export_data.path + filename

                bpy.ops.export_scene.fbx(
                    filepath=bpy.path.abspath(export_path),
                    use_selection=True,

                    axis_forward='Y',
                    axis_up = 'Z',

                    object_types=types_to_export,
                    apply_scale_options='FBX_SCALE_ALL',
                    global_scale=1.00,
                    apply_unit_scale=True,

                    use_mesh_modifiers=True,
                    mesh_smooth_type='FACE',
                    batch_mode='OFF',
                    use_custom_props=False,

                    bake_space_transform=False,

                    ## armature
                    primary_bone_axis='Y',
                    secondary_bone_axis='X',
                    use_armature_deform_only=True,
                    add_leaf_bones=False,

                    ## animation
                    bake_anim=export_data.bake_animation,
                    bake_anim_use_all_bones=True,
                    bake_anim_use_nla_strips=False,
                    bake_anim_use_all_actions=True,
                    bake_anim_force_startend_keying=True,
                    bake_anim_step=export_data.bake_anim_step,
                    bake_anim_simplify_factor=export_data.bake_anim_simplify_factor
                    )
                    
                obj.location = old_location
                
        # Reporting number of exported objects:
        length = len(exported_objects)
        if length == 0:
            self.report({'ERROR'},"No objects in exported collections!"



)
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
