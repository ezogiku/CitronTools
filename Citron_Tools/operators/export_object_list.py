import bpy
import csv
import os

class CITRON_OT_ExportObjectList(bpy.types.Operator):
    """シーンのオブジェクト情報をCSVファイルに出力します"""
    bl_idname = "citron.export_object_list"
    bl_label = "オブジェクトリストをCSVに出力"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # --- 設定を取得 ---
        # NパネルのUIで設定されたコレクションリストを取得
        settings = context.scene.citron_tool_settings
        base_collections_items = settings.base_collections
        
        # 名前だけのリストに変換 (項目が空でないかもチェック)
        BASE_COLLECTION_NAMES = [item.collection.name for item in base_collections_items if item.collection]

        if not BASE_COLLECTION_NAMES:
            self.report({'ERROR'}, "基準コレクションが指定されていません。Nパネルで設定してください。")
            return {'CANCELLED'}

        # (ここから下のロジックは前回とほぼ同じ)
        # --- ヘルパー関数 ---
        collection_parents = {}
        def build_collection_parent_map(parent_collection):
            for child in parent_collection.children:
                collection_parents[child] = parent_collection
                build_collection_parent_map(child)
        
        build_collection_parent_map(context.scene.collection)

        def get_relative_collection_path(obj, base_names):
            if not obj.users_collection: return "（未分類）"
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
            return ", ".join(relative_paths) if relative_paths else "（基準外）"
        
        # --- メイン処理 ---
        blend_filepath = bpy.data.filepath
        directory = os.path.dirname(blend_filepath) if blend_filepath else os.path.expanduser("~/Desktop")
        if not blend_filepath:
            self.report({'WARNING'}, "blendファイルが未保存のため、デスクトップにCSVファイルを保存します。")

        output_filename = "objects_list_export.csv"
        output_filepath = os.path.join(directory, output_filename)
        
        header = ["No.", "オブジェクト名", "内容", "表示/非表示", "引用マテリアル", "モディファイア", "ポリゴン数", "コレクション階層", "備考"]
        
        data_rows = []
        for i, obj in enumerate(context.scene.objects, 1):
            obj_name = obj.name
            content_str = obj.type.capitalize().replace('_', ' ')
            if obj.type == 'LIGHT': content_str = f"Light ({obj.data.type})"
            
            visibility_str = f"ビュー: {'非表示' if obj.hide_get() else '表示'} / レンダー: {'非表示' if obj.hide_render else '表示'}"
            materials_str = ", ".join([m.material.name for m in obj.material_slots if m.material]) or "なし"
            modifiers_str = ", ".join([mod.name for mod in obj.modifiers]) or "なし"
            poly_count = len(obj.data.polygons) if obj.type == 'MESH' else "-"
            # UIで設定された基準コレクション名リストを使ってパスを生成
            collection_path_str = get_relative_collection_path(obj, BASE_COLLECTION_NAMES)
            
            data_rows.append([i, obj_name, content_str, visibility_str, materials_str, modifiers_str, poly_count, collection_path_str, ""])
            
        try:
            with open(output_filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data_rows)
            self.report({'INFO'}, f"CSVを保存しました: {output_filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"ファイル書き出しエラー: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}