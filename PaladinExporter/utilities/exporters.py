import bpy

def export_fbx(self, export_path):
    bpy.ops.export_scene.fbx(filepath=bpy.path.abspath(export_path),
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
            # Breaks exporter in blender before 3.5, needs condition:
            #colors_type=(self.settings["colors_type"]),
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
