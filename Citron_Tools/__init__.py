bl_info = {
    "name": "Citron Tools",
    "author": "Chat Companion & You",
    "version": (1, 2, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Citron Tools",
    "description": "オブジェクトリストのエクスポートなど、便利なツールを集めたアドオン",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy

# --- 他のファイルからクラスをインポート ---
from .operators.export_object_list import CITRON_OT_ExportObjectList
from .ui.collection_list import (
    CITRON_CollectionListItem,
    CITRON_ToolSettings,
    CITRON_UL_CollectionList,
    CITRON_OT_AddCollectionItem,
    CITRON_OT_RemoveCollectionItem
)

# ------------------------------------------------------------------------
# パネルクラスの定義 (UIの見た目)
# ------------------------------------------------------------------------
class CITRON_PT_MainPanel(bpy.types.Panel):
    bl_label = "Citron Tools"
    bl_idname = "CITRON_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Citron Tools'

    def draw(self, context):
        layout = self.layout
        # シーンに保存されているアドオン設定を取得
        settings = context.scene.citron_tool_settings

        # --- 設定エリア ---
        box = layout.box()
        box.label(text="基準コレクション設定", icon='OUTLINER_COLLECTION')
        
        # UIリストを描画
        row = box.row()
        row.template_list(
            "CITRON_UL_CollectionList", "", 
            settings, "base_collections", 
            settings, "active_collection_index"
        )
        
        # +/- ボタンを描画するコラム
        col = row.column(align=True)
        col.operator(CITRON_OT_AddCollectionItem.bl_idname, text="", icon='ADD')
        col.operator(CITRON_OT_RemoveCollectionItem.bl_idname, text="", icon='REMOVE')
        
        layout.separator()

        # --- 実行エリア ---
        box2 = layout.box()
        box2.label(text="エクスポート", icon='EXPORT')
        box2.operator(CITRON_OT_ExportObjectList.bl_idname)

# ------------------------------------------------------------------------
# 登録/解除処理
# ------------------------------------------------------------------------
classes = (
    CITRON_OT_ExportObjectList,
    CITRON_CollectionListItem,
    CITRON_ToolSettings,
    CITRON_UL_CollectionList,
    CITRON_OT_AddCollectionItem,
    CITRON_OT_RemoveCollectionItem,
    CITRON_PT_MainPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # シーンプロパティにアドオンの設定を追加
    bpy.types.Scene.citron_tool_settings = bpy.props.PointerProperty(type=CITRON_ToolSettings)

def unregister():
    # シーンプロパティからアドオンの設定を削除
    del bpy.types.Scene.citron_tool_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()