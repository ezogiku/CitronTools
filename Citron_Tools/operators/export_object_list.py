import bpy
import csv
import os

class CITRON_OT_ExportObjectList(bpy.types.Operator):
    """シーンのオブジェクト情報をCSVファイルに出力します"""
    bl_idname = "citron.export_object_list"
    # UIのボタンラベルを日本語に変更
    bl_label = "オブジェクトリストをCSVに出力"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.citron_tool_settings
        base_collections_items = settings.base_collections
        BASE_COLLECTION_NAMES = [item.collection.name for item in base_collections_items if item.collection]

        if not BASE_COLLECTION_NAMES:
            # エラーメッセージを日本語に変更
            self.report({'ERROR'}, "基準コレクションが指定されていません。Nパネルで設定してください。")
            return {'CANCELLED'}

        collection_parents = {}
        def build_collection_parent_map(parent_collection):
            for child in parent_collection.children:
                collection_parents[child] = parent_collection
                build_collection_parent_map(child)
        
        build_collection_parent_map(context.scene.collection)

        def get_relative_collection_path(obj, base_names):
            # コレクション階層の文字列を日本語に変更
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
        
        blend_filepath = bpy.data.filepath
        directory = os.path.dirname(blend_filepath) if blend_filepath else os.path.expanduser("~/Desktop")
        if not blend_filepath:
            # 警告メッセージを日本語に変更
            self.report({'WARNING'}, ".blendファイルが未保存です。デスクトップにCSVファイルを保存します。")

        output_filepath = os.path.join(directory, "objects_list_export.csv")
        # ★ご指定のヘッダーに差し替え
        header = ["No.", "オブジェクト名", "内容", "表示/非表示", "引用マテリアル", "モディファイア", "ポリゴン数", "コレクション階層", "備考"]
        
        data_rows = []
        for i, obj in enumerate(context.scene.objects, 1):
            # 表示/非表示の文字列を日本語に変更
            view_vis = "非表示" if obj.hide_get() else "表示"
            render_vis = "非表示" if obj.hide_render else "表示"
            visibility_str = f"ビュー: {view_vis} / レンダー: {render_vis}"
            
            # マテリアル/モディファイアがない場合の文字列を日本語に変更
            materials_str = ", ".join([m.material.name for m in obj.material_slots if m.material]) or "なし"
            modifiers_str = ", ".join([mod.name for mod in obj.modifiers]) or "なし"
            
            poly_count = len(obj.data.polygons) if obj.type == 'MESH' else "-"
            collection_path_str = get_relative_collection_path(obj, BASE_COLLECTION_NAMES)
            
            # ヘッダーの順に合わせてデータを格納
            data_rows.append([i, obj.name, obj.type.capitalize(), visibility_str, materials_str, modifiers_str, poly_count, collection_path_str, ""])
            
        try:
            with open(output_filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data_rows)
            # 完了メッセージを日本語に変更
            self.report({'INFO'}, f"CSVを保存しました: {output_filepath}")
        except Exception as e:
            # エラーメッセージを日本語に変更
            self.report({'ERROR'}, f"ファイル書き込みエラー: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}