# ファイル名: Citron_Tools/__init__.py

bl_info = {
    "name": "Citron Tools",
    "author": "Chat Companion & You",
    "version": (1, 3, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Citron Tools",
    "description": "便利なツール集",
    "warning": "",
    "support": "COMMUNITY",
    # ↓↓↓ ご自身のGitHub情報に書き換えるのを忘れないでください ↓↓↓
    "download_url": "https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases/latest/download/Citron_Tools.zip",
    "tracker_url": "https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues",
    "doc_url": "https://github.com/YOUR_USERNAME/YOUR_REPO_NAME",
    "category": "3D View",
}

import bpy

# --- 各ファイルからクラスをインポート ---
from .operators.export_object_list import CITRON_OT_ExportObjectList
from .operators.rename_tool import CITRON_OT_RenameUtility, CITRON_RenameSettings
from .operators.bone_hierarchy_exporter import (
    CITRON_OT_InstallDependencies,
    CITRON_OT_ExportBoneHierarchyPNG,
    CITRON_OT_ExportBoneHierarchyCSV
)
from .ui.collection_list import (
    CITRON_CollectionListItem,
    CITRON_ToolSettings,
    CITRON_UL_CollectionList,
    CITRON_OT_AddCollectionItem,
    CITRON_OT_RemoveCollectionItem
)

# --- UIパネルの定義 ---
class CITRON_PT_MainPanel(bpy.types.Panel):
    bl_label = "Citron Tools"
    bl_idname = "CITRON_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Citron Tools'

    def draw(self, context):
        layout = self.layout
        csv_settings = context.scene.citron_tool_settings
        rename_settings = context.scene.citron_rename_settings
        
        box = layout.box()
        box.label(text="CSVエクスポート設定", icon='OUTLINER_COLLECTION')
        row = box.row()
        row.template_list("CITRON_UL_CollectionList", "", csv_settings, "base_collections", csv_settings, "active_collection_index")
        col = row.column(align=True)
        col.operator(CITRON_OT_AddCollectionItem.bl_idname, text="", icon='ADD')
        col.operator(CITRON_OT_RemoveCollectionItem.bl_idname, text="", icon='REMOVE')
        box.operator(CITRON_OT_ExportObjectList.bl_idname)
        
        layout.separator()
        box3 = layout.box()
        box3.label(text="名前変更ツール", icon='FONT_DATA')
        col = box3.column(align=True)
        col.label(text="変換方向:"); col.prop(rename_settings, "direction", expand=True)
        col.label(text="対象範囲:"); col.prop(rename_settings, "scope", expand=True)
        col.label(text="変更するデータタイプ:")
        grid = col.grid_flow(row_major=True, columns=2, align=True)
        grid.prop(rename_settings, "rename_objects"); grid.prop(rename_settings, "rename_bones")
        grid.prop(rename_settings, "rename_materials"); grid.prop(rename_settings, "rename_shapekeys")
        box3.separator()
        box3.operator(CITRON_OT_RenameUtility.bl_idname)
        
        layout.separator()
        box4 = layout.box()
        box4.label(text="ボーン階層ツール", icon='BONE_DATA')
        col = box4.column(align=True)
        col.label(text="初回のみ実行が必要です:", icon='INFO')
        col.operator(CITRON_OT_InstallDependencies.bl_idname)
        box4.separator()
        col2 = box4.column(align=True)
        col2.label(text="エクスポート形式:")
        row = col2.row(align=True)
        row.operator(CITRON_OT_ExportBoneHierarchyPNG.bl_idname, icon='IMAGE_DATA')
        row.operator(CITRON_OT_ExportBoneHierarchyCSV.bl_idname, icon='TEXT')

# --- 登録/解除処理 ---
classes = (
    CITRON_OT_ExportObjectList,
    CITRON_OT_RenameUtility,
    CITRON_RenameSettings,
    CITRON_OT_InstallDependencies,
    CITRON_OT_ExportBoneHierarchyPNG,
    CITRON_OT_ExportBoneHierarchyCSV,
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
    bpy.types.Scene.citron_tool_settings = bpy.props.PointerProperty(type=CITRON_ToolSettings)
    bpy.types.Scene.citron_rename_settings = bpy.props.PointerProperty(type=CITRON_RenameSettings)

def unregister():
    del bpy.types.Scene.citron_tool_settings
    del bpy.types.Scene.citron_rename_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()