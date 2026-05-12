import bpy
from bpy.props import EnumProperty, IntProperty
from ..utilities.general import generate_random_uuid, is_collection_valid

# Blender's builtin name for collections root
DEFAULT_SCENE_COLLECTION = 'Scene Collection'
UUID_PROPERTY = 'UUID'

class Paladin_OT_ExportSetAdd(bpy.types.Operator):
    bl_idname = "paladin.export_set_add"
    bl_label = "Add Set"
    bl_description = "Adds an 'Export Set'"
    bl_options = {'UNDO'}

    def execute(self, context):
        new_set = context.scene.exporter.sets.add()
        # Blender may populate the new slot with stale data from undo history
        # or leftover file data — always start with a clean items list.
        count = len(new_set.items)
        while new_set.items:
            new_set.items.remove(0)
        if count:
            print(f"[Game Exporter] ExportSetAdd: cleared {count} pre-existing item(s) from new set slot")
        return{'FINISHED'}

class Paladin_OT_ExportSetRemove(bpy.types.Operator):
    bl_idname = "paladin.export_set_remove"
    bl_label = "Remove Set"
    bl_description = "Delete this 'Export Set'"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.exporter.sets

    index:IntProperty(name="set_index", default = 0)

    def execute(self, context):
        context.scene.exporter.sets.remove(self.index)
        return{'FINISHED'}

class Paladin_OT_ExportSetItemAdd(bpy.types.Operator):
    bl_idname = "paladin.export_set_items_add"
    bl_label = "Add"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.collection.name == DEFAULT_SCENE_COLLECTION:
            return False
        return True
            
    @classmethod
    def description(cls, context, event):
        collection_name = context.collection.name
        if collection_name == DEFAULT_SCENE_COLLECTION:
            return "You cannot add 'Scene Collection'"
        return f"Adds Collection '{collection_name}' to this export set"

    set_index:IntProperty(name="Set Index", default = 0)

    def execute(self, context):
        collection = context.collection
        collection_name = context.collection.name
        export_set = context.scene.exporter.sets[self.set_index]

        # Create a unique id for the collection object if it doesn't have one
        if UUID_PROPERTY not in collection:
            collection[UUID_PROPERTY] = generate_random_uuid()

        collection_uuid = collection[UUID_PROPERTY]

        # Duplicated collections inherit the original's UUID custom property.
        # If another collection shares this UUID, generate a new one for this collection.
        for other in bpy.data.collections:
            if other != collection and other.get(UUID_PROPERTY) == collection_uuid:
                collection[UUID_PROPERTY] = generate_random_uuid()
                collection_uuid = collection[UUID_PROPERTY]
                break

        # linking is done using the unique id property of the collection object
        for item in export_set.items:
            if item.uuid == collection_uuid:
                self.report({'WARNING'}, f"Collection '{collection_name}' already in set {self.set_index + 1}.")
                return {'CANCELLED'}
                
        item = export_set.items.add()
        item.name = collection_name
        item.uuid = collection_uuid
        export_set.items_index = len(export_set.items) - 1

        # If the export set preset is Substance Painter Object, enable use_collection by default
        enum_items = export_set.bl_rna.properties["preset"].enum_items
        preset_name = enum_items[export_set.preset].name
        if preset_name == "Substance Painter Object":
            item.use_collection = True

        return {'FINISHED'}

class Paladin_OT_ExportSetItemRemove(bpy.types.Operator):
    bl_idname = "paladin.export_set_item_remove"
    bl_label = "Remove set item"
    bl_options = {'UNDO'}
    bl_description = "Removes selected Item from this set"

    set_index:IntProperty(name="Set Index", default = 0)

    def execute(self, context):
        export_set = context.scene.exporter.sets[self.set_index]
        items = export_set.items

        items.remove(export_set.items_index)
        # Selects item above index when it is removed:
        export_set.items_index = min(max(0, export_set.items_index - 1), len(items) - 1)
        return{'FINISHED'}

class Paladin_OT_ExportSetItemMove(bpy.types.Operator):
    bl_idname = "paladin.export_set_item_move"
    bl_label = "Move"
    bl_options = {'UNDO'}

    @classmethod
    def description(cls, context, event):        
        return "Move Export Set Collection up or down"
    
    set_index:IntProperty(name="Set Index", default = 0)
    direction: EnumProperty(items=[('UP', 'Up',""),('DOWN', 'Down',"")])

    def execute(self, context):
        export_set = context.scene.exporter.sets[self.set_index]
        items = export_set.items
        index = export_set.items_index

        if self.direction == "UP":
            next_index = max(index - 1, 0)
        elif self.direction == "DOWN":
            next_index = min(index + 1, len(items) - 1)
            
        items.move(index, next_index)
        export_set.items_index = next_index
        return{'FINISHED'}

class Paladin_OT_ExportSetCleanupMissing(bpy.types.Operator):
    bl_idname = "paladin.export_set_cleanup_missing"
    bl_label = "Remove Missing Collections"
    bl_options = {'UNDO'}
    bl_description = "Removes all items referencing deleted or missing collections from this set"

    set_index: IntProperty(name="Set Index", default=0)

    def execute(self, context):
        export_set = context.scene.exporter.sets[self.set_index]
        items = export_set.items
        to_remove = [i for i in range(len(items)) if not is_collection_valid(items[i].uuid)]
        for i in reversed(to_remove):
            items.remove(i)
        removed = len(to_remove)
        export_set.items_index = min(max(0, export_set.items_index), len(items) - 1)
        if removed:
            self.report({'INFO'}, f"Removed {removed} missing item(s) from Set {self.set_index + 1}.")
        else:
            self.report({'INFO'}, "No missing items found.")
        return {'FINISHED'}


class Paladin_OT_DiagnoseExporterData(bpy.types.Operator):
    bl_idname = "paladin.diagnose_exporter_data"
    bl_label = "Diagnose Exporter Data"
    bl_description = "Prints the full exporter property state to the system console"

    def execute(self, context):
        sets = context.scene.exporter.sets
        print(f"\n[Game Exporter] === DIAGNOSE: {len(sets)} set(s) in scene '{context.scene.name}' ===")
        for si, export_set in enumerate(sets):
            print(f"  Set {si}: {len(export_set.items)} item(s), preset={export_set.preset}")
            for ii, item in enumerate(export_set.items):
                valid = is_collection_valid(item.uuid)
                print(f"    Item {ii}: uuid={repr(item.uuid)}, name={repr(item.name)}, valid={valid}")
        print(f"[Game Exporter] Collections with UUID property:")
        for col in bpy.data.collections:
            if 'UUID' in col:
                print(f"  '{col.name}' → UUID={repr(col['UUID'])}")
        print("[Game Exporter] === END DIAGNOSE ===\n")
        self.report({'INFO'}, f"Diagnose output written to system console.")
        return {'FINISHED'}


class Paladin_OT_RepairAllSets(bpy.types.Operator):
    bl_idname = "paladin.repair_all_sets"
    bl_label = "Repair All Export Sets"
    bl_options = {'UNDO'}
    bl_description = "Removes all items referencing missing collections from every export set in this scene"

    def execute(self, context):
        # Fix UUID conflicts: duplicated collections inherit the original's UUID.
        # Walk all collections; any that share a UUID with an earlier one get a fresh UUID.
        seen_uuids = {}
        reassigned = 0
        for col in bpy.data.collections:
            uuid = col.get(UUID_PROPERTY)
            if uuid is None:
                continue
            if uuid in seen_uuids:
                col[UUID_PROPERTY] = generate_random_uuid()
                reassigned += 1
            else:
                seen_uuids[uuid] = col.name

        # Remove items that reference missing or now-unresolvable collections
        total_removed = 0
        for export_set in context.scene.exporter.sets:
            items = export_set.items
            to_remove = [i for i in range(len(items)) if not is_collection_valid(items[i].uuid)]
            for i in reversed(to_remove):
                items.remove(i)
            total_removed += len(to_remove)
            export_set.items_index = min(max(0, export_set.items_index), len(items) - 1)

        parts = []
        if reassigned:
            parts.append(f"reassigned {reassigned} duplicate UUID(s)")
        if total_removed:
            parts.append(f"removed {total_removed} missing item(s)")
        self.report({'INFO'}, ("Repaired: " + ", ".join(parts)) if parts else "Nothing to repair.")
        return {'FINISHED'}


classes = (
    Paladin_OT_ExportSetAdd,
    Paladin_OT_ExportSetRemove,
    Paladin_OT_ExportSetItemAdd,
    Paladin_OT_ExportSetItemRemove,
    Paladin_OT_ExportSetItemMove,
    Paladin_OT_ExportSetCleanupMissing,
    Paladin_OT_RepairAllSets,
    Paladin_OT_DiagnoseExporterData,
    )
    
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
