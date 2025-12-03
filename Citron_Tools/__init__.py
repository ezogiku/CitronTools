bl_info = {
    "name": "Citron Tools",
    "author": "Chat Companion & You",
    "version": (1, 2, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Citron Tools",
    "description": "オブジェクトリストのエクスポートなど、便利なツールを集めたアドオン",
    "warning": "",
    "support": "COMMUNITY",
    # ↓↓↓ ご自身のGitHub情報に書き換えるのを忘れないでください ↓↓↓
    "download_url": "https://github.com/ezogiku/CitronTools/releases/latest/download/Citron_Tools.zip",
    "tracker_url": "https://github.com/ezogiku/CitronTools/issues",
    "doc_url": "https://github.com/ezogiku/CitronTools",
    "category": "3D View",
}

import bpy

# 他のファイルからクラスをインポート
from .operators.export_object_list import CITRON_OT_ExportObjectList
from .ui.collection_list import (
    CITRON_CollectionListItem,
    CITRON_ToolSettings,
    CITRON_UL_CollectionList,
    CITRON_OT_AddCollectionItem,
    CITRON_OT_RemoveCollectionItem
)

# パネルクラスの定義（UIの見た目）
class CITRON_PT_MainPanel(bpy.types.Panel):
    bl_label = "Citron Tools"
    bl_idname = "CITRON_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Citron Tools'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.citron_tool_settings

        # 設定エリア
        box = layout.box()
        box.label(text="Base Collection Settings", icon='OUTLINER_COLLECTION')
        
        row = box.row()
        row.template_list(
            "CITRON_UL_CollectionList", "", 
            settings, "base_collections", 
            settings, "active_collection_index"
        )
        
        col = row.column(align=True)
        col.operator(CITRON_OT_AddCollectionItem.bl_idname, text="", icon='ADD')
        col.operator(CITRON_OT_RemoveCollectionItem.bl_idname, text="", icon='REMOVE')
        
        layout.separator()

        # 実行エリア
        box2 = layout.box()
        box2.label(text="Export", icon='EXPORT')
        box2.operator(CITRON_OT_ExportObjectList.bl_idname)

# 登録するクラスのリスト
classes = (
    CITRON_OT_ExportObjectList,
    CITRON_CollectionListItem,
    CITRON_ToolSettings,
    CITRON_UL_CollectionList,
    CITRON_OT_AddCollectionItem,
    CITRON_OT_RemoveCollectionItem,
    CITRON_PT_MainPanel,  # ここで使う名前と...
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