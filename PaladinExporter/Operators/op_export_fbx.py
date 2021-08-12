import bpy

class Paladin_OT_ExportFbx(bpy.types.Operator):
    bl_idname = "paladin.exportfbx"
    bl_label = "Export FBX"

    @classmethod
    def poll(cls, context):
        if bpy.context.object.mode != "OBJECT":
            return False
        
        return True

    def execute(self, context):
        exportItems = context.scene.ExportItemsList.values()

        for exportItem in exportItems:

            if exportItem.include_in_export == False:
                continue

            collection = bpy.data.collections[exportItem.collection_name]
            
            if collection is None:
                print("collection not found! " + exportItem.collection_name)
                continue
            
            parent_objects = []

            ## Find all top level objects in collection
            for ob in collection.objects:
                if ob.parent == None and ob.type in ('MESH','EMPTY','ARMATURE'):
                    parent_objects.append(ob)
                
            for ob in parent_objects:
                bpy.ops.object.select_all(action='DESELECT')
                ob.select_set(True)
                context.view_layer.objects.active = ob
                bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
                filename = ob.name

                if context.scene.ExportData.bake_animation:
                    filename += context.scene.ExportData.filename_suffix

                filename += ".fbx"

                old_location = ob.location.copy()

                if exportItem.reset_origin:
                    ob.location = (0,0,0)

                types_to_export = {}
                if context.scene.ExportData.include_meshes:
                    types_to_export = {'ARMATURE','MESH','EMPTY'}
                else:
                    types_to_export = {'ARMATURE','EMPTY'}

                bpy.ops.export_scene.fbx(
                    filepath=bpy.path.abspath(context.scene.ExportData.path + filename),
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
                    bake_anim=context.scene.ExportData.bake_animation,
                    bake_anim_use_all_bones=True,
                    bake_anim_use_nla_strips=True,
                    bake_anim_use_all_actions=True,
                    bake_anim_force_startend_keying=True,
                    bake_anim_step=context.scene.ExportData.bake_anim_step,
                    bake_anim_simplify_factor=context.scene.ExportData.bake_anim_simplify_factor
                    )
                
                ob.location = old_location
                
        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
