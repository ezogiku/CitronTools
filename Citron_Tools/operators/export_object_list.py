import bpy
import csv
import os

class CITRON_OT_ExportObjectList(bpy.types.Operator):
    bl_idname = "citron.export_object_list"
    bl_label = "Export Object List to CSV"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.citron_tool_settings
        base_collections_items = settings.base_collections
        BASE_COLLECTION_NAMES = [item.collection.name for item in base_collections_items if item.collection]

        if not BASE_COLLECTION_NAMES:
            self.report({'ERROR'}, "No base collections specified. Please set them in the N panel.")
            return {'CANCELLED'}

        collection_parents = {}
        def build_collection_parent_map(parent_collection):
            for child in parent_collection.children:
                collection_parents[child] = parent_collection
                build_collection_parent_map(child)
        
        build_collection_parent_map(context.scene.collection)

        def get_relative_collection_path(obj, base_names):
            if not obj.users_collection: return "(Unassigned)"
            relative_paths = []
            for col in obj.users_collection:
                path_parts = []
                found_base = False
                current_col = col
                while True:
                    if current_col.name in base_names:
                        found_base = True
                        break
                    path_parts.insert(0, current_col.name)
                    if current_col not in collection_parents: break
                    current_col = collection_parents[current_col]
                if found_base:
                    relative_paths.append(" / ".join(path_parts))
            return ", ".join(relative_paths) if relative_paths else "(Outside Base)"
        
        blend_filepath = bpy.data.filepath
        directory = os.path.dirname(blend_filepath) if blend_filepath else os.path.expanduser("~/Desktop")
        if not blend_filepath:
            self.report({'WARNING'}, "Blend file is not saved. Saving CSV to Desktop.")

        output_filepath = os.path.join(directory, "objects_list_export.csv")
        header = ["No.", "Object Name", "Content", "Visibility", "Material", "Modifiers", "Polygon Count", "Collection Path", "Notes"]
        
        data_rows = []
        for i, obj in enumerate(context.scene.objects, 1):
            visibility_str = f"View: {'Hidden' if obj.hide_get() else 'Visible'} / Render: {'Hidden' if obj.hide_render else 'Visible'}"
            materials_str = ", ".join([m.material.name for m in obj.material_slots if m.material]) or "None"
            modifiers_str = ", ".join([mod.name for mod in obj.modifiers]) or "None"
            poly_count = len(obj.data.polygons) if obj.type == 'MESH' else "-"
            collection_path_str = get_relative_collection_path(obj, BASE_COLLECTION_NAMES)
            data_rows.append([i, obj.name, obj.type.capitalize(), visibility_str, materials_str, modifiers_str, poly_count, collection_path_str, ""])
            
        try:
            with open(output_filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data_rows)
            self.report({'INFO'}, f"CSV saved to: {output_filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"File write error: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}