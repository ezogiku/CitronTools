# ファイル名: Citron_Tools/operators/bone_hierarchy_exporter.py

import bpy
import sys
import subprocess
import importlib
import csv
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

# --- 依存ライブラリの管理 ---
REQUIRED_MODULES = ["pydot", "matplotlib"]

class CITRON_OT_InstallDependencies(Operator):
    """画像出力に必要なライブラリ(pydot, matplotlib)をインストールします"""
    bl_idname = "citron.install_dependencies"
    bl_label = "依存ライブラリをインストール"

    def execute(self, context):
        try:
            py_exec = sys.executable
            subprocess.run([py_exec, "-m", "ensurepip"], check=True)
            subprocess.run([py_exec, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            for module_name in REQUIRED_MODULES:
                if importlib.util.find_spec(module_name) is None:
                    self.report({'INFO'}, f"{module_name}をインストールしています...")
                    subprocess.run([py_exec, "-m", "pip", "install", module_name], check=True)
                    self.report({'INFO'}, f"{module_name}のインストールが完了しました。")
                else:
                    self.report({'INFO'}, f"{module_name}は既にインストールされています。")
            self.report({'INFO'}, "全てのライブラリの準備が完了しました。")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"インストールに失敗しました: {e}")
            return {'CANCELLED'}

# --- 共通ロジックとヘルパー関数 ---
def get_bone_hierarchy_and_depth(armature_data):
    parents = {bone.name: bone.parent.name if bone.parent else None for bone in armature_data.bones}
    depths = {}
    def get_depth(bone_name):
        if bone_name in depths: return depths[bone_name]
        parent = parents.get(bone_name)
        if not parent:
            depths[bone_name] = 0
            return 0
        else:
            depth = get_depth(parent) + 1
            depths[bone_name] = depth
            return depth
    for bone in armature_data.bones: get_depth(bone.name)
    return parents, depths

# --- PNG出力オペレーター ---
class CITRON_OT_ExportBoneHierarchyPNG(Operator, ExportHelper):
    """選択中のアーマチュアのボーン階層を色付きのPNG画像で出力します"""
    bl_idname = "citron.export_bone_hierarchy_png"
    bl_label = "ボーン階層を画像(PNG)で出力"
    filename_ext = ".png"
    filter_glob: bpy.props.StringProperty(default="*.png", options={"HIDDEN"})

    def execute(self, context):
        try:
            import pydot
            import matplotlib.colors as mcolors
            import colorsys
        except ImportError:
            self.report({'ERROR'}, "依存ライブラリが不足しています。先にインストールを実行してください。")
            return {'CANCELLED'}
        obj = context.active_object
        if not obj or obj.type != "ARMATURE":
            self.report({"ERROR"}, "アクティブなアーマチュアを選択してください。")
            return {"CANCELLED"}
        arm = obj.data
        parents, depths = get_bone_hierarchy_and_depth(arm)
        max_depth = max(depths.values()) if depths else 1
        def get_color_palette(base_color, depth, max_depth):
            base_rgb = mcolors.to_rgb(base_color)
            h, l, s = colorsys.rgb_to_hls(*base_rgb)
            new_l = min(1.0, 0.3 + 0.55 * (depth / max_depth))
            r, g, b = colorsys.hls_to_rgb(h, new_l, s)
            return '#%02x%02x%02x' % (int(255 * r), int(255 * g), int(255 * b))
        graph = pydot.Dot(graph_type="digraph", rankdir="LR")
        nodes = {}
        for name, depth in depths.items():
            if name.endswith((".L", "_L")): color = get_color_palette("#3399ff", depth, max_depth)
            elif name.endswith((".R", "_R")): color = get_color_palette("#ffd700", depth, max_depth)
            else: color = get_color_palette("#00cc66", depth, max_depth)
            node = pydot.Node(name, label=name, style="filled", fillcolor=color, shape="box", fontcolor="black")
            nodes[name] = node; graph.add_node(node)
        for name, parent in parents.items():
            if parent: graph.add_edge(pydot.Edge(parent, name))
        try:
            graph.write_png(self.filepath)
            self.report({"INFO"}, f"PNGを出力しました： {self.filepath}")
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"画像出力に失敗しました。GraphvizがPCにインストールされていない可能性があります。エラー: {e}")
            return {"CANCELLED"}

# --- CSV出力オペレーター ---
class CITRON_OT_ExportBoneHierarchyCSV(Operator, ExportHelper):
    """選択中のアーマチュアのボーン階層をCSV形式で出力します"""
    bl_idname = "citron.export_bone_hierarchy_csv"
    bl_label = "ボーン階層をCSVで出力"
    filename_ext = ".csv"
    filter_glob: bpy.props.StringProperty(default="*.csv", options={"HIDDEN"})

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "ARMATURE":
            self.report({"ERROR"}, "アクティブなアーマチュアを選択してください。")
            return {"CANCELLED"}
        arm = obj.data
        parents, depths = get_bone_hierarchy_and_depth(arm)
        children_map = {name: [] for name in parents}; root_bones = []
        for bone_name, parent_name in parents.items():
            if parent_name: children_map[parent_name].append(bone_name)
            else: root_bones.append(bone_name)
        try:
            with open(self.filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                def write_bone_recursively(bone_name, depth):
                    row = [''] * depth + [bone_name]; writer.writerow(row)
                    children = sorted(children_map.get(bone_name, []))
                    for child_name in children: write_bone_recursively(child_name, depth + 1)
                for root_bone in sorted(root_bones): write_bone_recursively(root_bone, 0)
            self.report({"INFO"}, f"CSVを出力しました： {self.filepath}")
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"CSV出力に失敗しました: {e}")
            return {"CANCELLED"}