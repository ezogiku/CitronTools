import bpy

# UIリストの各行のデータを保持するためのプロパティグループ
class CITRON_CollectionListItem(bpy.types.PropertyGroup):
    # 各行がBlenderの「コレクション」データへのポインタを持つ
    collection: bpy.props.PointerProperty(
        name="Collection",
        type=bpy.types.Collection
    )

# UIリスト自体のレイアウトを定義するクラス
class CITRON_UL_CollectionList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # UIリストの各行の見た目を定義
        # data = シーン設定, item = CITRON_CollectionListItem のインスタンス
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # コレクション選択欄を表示
            layout.prop(item, "collection", text="")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

# リストに新しい項目を追加するオペレーター
class CITRON_OT_AddCollectionItem(bpy.types.Operator):
    bl_idname = "citron.add_collection_item"
    bl_label = "Add Base Collection"

    def execute(self, context):
        context.scene.citron_tool_settings.base_collections.add()
        return {'FINISHED'}

# リストから選択中の項目を削除するオペレーター
class CITRON_OT_RemoveCollectionItem(bpy.types.Operator):
    bl_idname = "citron.remove_collection_item"
    bl_label = "Remove Base Collection"

    def execute(self, context):
        settings = context.scene.citron_tool_settings
        index = settings.active_collection_index
        settings.base_collections.remove(index)
        # 削除後にインデックスが範囲外にならないように調整
        if index > 0:
            settings.active_collection_index = index - 1
        return {'FINISHED'}

# アドオン全体の設定を保持するためのプロパティグループ
class CITRON_ToolSettings(bpy.types.PropertyGroup):
    # 上で定義したCollectionListItemのリスト（コレクションプロパティ）
    base_collections: bpy.props.CollectionProperty(type=CITRON_CollectionListItem)
    # UIリストで現在選択されている行のインデックス
    active_collection_index: bpy.props.IntProperty(name="Index")