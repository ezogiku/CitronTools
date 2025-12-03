import bpy

class CITRON_CollectionListItem(bpy.types.PropertyGroup):
    collection: bpy.props.PointerProperty(name="Collection", type=bpy.types.Collection)

class CITRON_UL_CollectionList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "collection", text="")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class CITRON_OT_AddCollectionItem(bpy.types.Operator):
    bl_idname = "citron.add_collection_item"
    bl_label = "Add Base Collection"
    def execute(self, context):
        context.scene.citron_tool_settings.base_collections.add()
        return {'FINISHED'}

class CITRON_OT_RemoveCollectionItem(bpy.types.Operator):
    bl_idname = "citron.remove_collection_item"
    bl_label = "Remove Base Collection"
    def execute(self, context):
        settings = context.scene.citron_tool_settings
        index = settings.active_collection_index
        settings.base_collections.remove(index)
        if index > 0:
            settings.active_collection_index = index - 1
        return {'FINISHED'}

class CITRON_ToolSettings(bpy.types.PropertyGroup):
    base_collections: bpy.props.CollectionProperty(type=CITRON_CollectionListItem)
    active_collection_index: bpy.props.IntProperty(name="Index")