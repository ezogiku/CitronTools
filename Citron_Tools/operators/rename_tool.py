import bpy
import re

# --- 日英翻訳辞書 (JP -> EN) ---
TRANSLATION_DICT = TRANSLATION_DICT = {

    # =========================
    # 髪・頭部
    # =========================
    "前髪": "Bangs",
    "横髪": "SideHair",
    "後ろ髪": "BackHair",
    "後髪": "BackHair",
    "あほ毛": "Ahoge",
    "髪の毛": "Hair",
    "髪": "Hair",
    "頭皮": "Scalp",
    "頭": "Head",

    # =========================
    # 顔・肌・体
    # =========================
    "顔": "Face",
    "肌": "Skin",
    "体": "Body",

    # =========================
    # 頭部・顔（詳細）
    # =========================
    "後頭部": "Occipital",
    "こめかみ": "Temple",
    "おでこ": "Forehead",
    "額": "Forehead",
    "頬骨": "Cheekbone",
    "頬": "Cheek",
    "鼻先": "NoseTip",
    "鼻筋": "NoseBridge",
    "鼻": "Nose",
    "耳たぶ": "Earlobe",
    "耳": "Ear",
    "あご先": "ChinTip",
    "あご": "Chin",
    "下あご": "Jaw",
    "ほうれい線": "Nasolabial",
    
        # =========================
    # 首・胴体（上半身）
    # =========================
    "首元": "NeckBase",
    "首": "Neck",
    "鎖骨": "Clavicle",
    "肩甲骨": "Scapula",
    "肩": "Shoulder",
    "胸骨": "Sternum",
    "胸部": "Chest",
    "胸": "Chest",
    "乳房": "Breast",
    "みぞおち": "SolarPlexus",
    "肋骨": "Rib",
    "腹部": "Abdomen",
    "お腹": "Abdomen",
    "へそ": "Navel",
    "背骨": "Spine",
    "背中": "Back",
    "腰": "Waist",

    # =========================
    # 骨盤・下半身
    # =========================
    "骨盤": "Pelvis",
    "股関節": "HipJoint",
    "尻": "Buttocks",
    "尻肉": "Glute",
    "太もも": "Thigh",
    "もも": "Thigh",
    "ひざ裏": "KneeBack",
    "ひざ": "Knee",
    "すね": "Shin",
    "ふくらはぎ": "Calf",
    "足首": "Ankle",
    "かかと": "Heel",
    "足の甲": "FootInstep",
    "足裏": "Sole",
    "足指": "Toes",
    "足": "Foot",
    
    
    # =========================
    # 腕・手
    # =========================
    "肩関節": "ShoulderJoint",
    "上腕": "UpperArm",
    "二の腕": "UpperArm",
    "肘": "Elbow",
    "前腕": "Forearm",
    "手首": "Wrist",
    "手のひら": "Palm",
    "手": "Hand",
    "親指": "Thumb",
    "人差し指": "Index",
    "中指": "Middle",
    "薬指": "Ring",
    "小指": "Little",

    # =========================
    # 性別差分・R18系で分離しがちな部位
    # =========================
    "バストトップ": "BustTop",
    "乳首": "Nipple",
    "下腹部": "LowerAbdomen",
    "恥骨": "PubicBone",
    "股間": "Groin",

    # =========================
    # 皮膚・変形用の補助オブジェクト
    # =========================
    "筋肉": "Muscle",
    "脂肪": "Fat",
    "血管": "Vein",
    "皮下": "Subcutaneous",

    # =========================
    # 目まわり（装飾含む）
    # =========================
    "ハイライト": "Highlight",
    "ハイライト": "Eyehighlight",
    "白目": "WhiteOfEyes",
    "白目": "WhiteEye",
    "瞳": "Pupil",
    "目": "Eye",
    "涙": "Tears",
    "ぐるぐる": "Guruguru",        # デフォルメ表現
    "ハート": "Heart",             # ハート目
    "キラキラ": "Sparkling",       # スパークル目

    # =========================
    # 眉・まつげ
    # =========================
    "まつげ": "Eyelash",
    "まゆ": "Eyebrow",
    "まゆ": "Eyebrows",


    # =========================
    # 口内
    # =========================
    "口内": "MouthCavity",
    "口": "Mouth",
    "舌": "Tongue",
    "歯": "Teeth",

    # =========================
    # 服
    # =========================
    "ワンピース": "Dress",
    "上着": "Jacket",
    "シャツ": "Shirt",
    "スカート": "Skirt",
    "パニエ": "Panniers",
    "ズボン": "Pants",
    "服": "Clothes",

    # =========================
    # 靴・足まわり
    # =========================
    "サンダル": "Sandals",
    "ローファー": "Loafers",
    "靴下": "Socks",
    "靴": "Shoes",

    # =========================
    # 襟・ボタン
    # =========================
    "襟": "Collar",
    "ボタン": "Button",

    # =========================
    # 装飾・アクセサリー
    # =========================
    "チョーカー": "Choker",
    "シュシュ": "Scrunchie",
    "カフス": "Cuffs",
    "眼鏡": "Glasses",
    "ベルト": "Belt",
    "チェーン": "Chain",
    "ビーズ": "Beads",
    "飾り": "Accessory",
    
        # =========================
    # 上半身衣装（トップス）
    # =========================
    "オーバーサイズシャツ": "OversizedShirt",
    "ロングスリーブシャツ": "LongSleeveShirt",
    "ノースリーブシャツ": "SleevelessShirt",
    "タートルネックシャツ": "Turtleneck",
    "ハイネックシャツ": "HighNeck",
    "ボタンダウンシャツ": "ButtonDownShirt",
    "ブラウス": "Blouse",
    "カーディガン": "Cardigan",
    "セーター": "Sweater",
    "ニット": "Knit",
    "トレーナー": "Sweatshirt",
    "パーカー": "Hoodie",
    "ベスト": "Vest",
    "タンクトップ": "TankTop",
    "キャミソール": "Camisole",
    "Tシャツ": "TShirt",

    # =========================
    # アウター
    # =========================
    "ロングコート": "LongCoat",
    "トレンチコート": "TrenchCoat",
    "ダッフルコート": "DuffleCoat",
    "ダウンジャケット": "DownJacket",
    "ライダースジャケット": "RidersJacket",
    "ブルゾン": "Blouson",
    "ジャンパー": "Jumper",
    "ジャケット": "Jacket",
    "コート": "Coat",

    # =========================
    # 下半身衣装
    # =========================
    "ショートパンツ": "ShortPants",
    "ホットパンツ": "HotPants",
    "スキニーパンツ": "SkinnyPants",
    "ワイドパンツ": "WidePants",
    "ガウチョパンツ": "GauchoPants",
    "レギンス": "Leggings",
    "タイツ": "Tights",
    "デニムパンツ": "DenimPants",
    "パンツ": "Pants",

    # =========================
    # スカート
    # =========================
    "フレアスカート": "FlareSkirt",
    "プリーツスカート": "PleatedSkirt",
    "タイトスカート": "TightSkirt",
    "ミニスカート": "MiniSkirt",
    "ロングスカート": "LongSkirt",
    "スカート": "Skirt",

    # =========================
    # ワンピース・ドレス
    # =========================
    "ロングドレス": "LongDress",
    "ミニドレス": "MiniDress",
    "パーティードレス": "PartyDress",
    "サマードレス": "SummerDress",
    "ワンピース": "Dress",

    # =========================
    # 下着・インナー（分離されやすい）
    # =========================
    "スポーツブラ": "SportsBra",
    "ブラジャー": "Bra",
    "ブリーフ": "Briefs",
    "ショーツ": "Shorts",
    "パンツ下着": "UnderwearBottom",
    "インナーシャツ": "InnerShirt",
    "キャミ下着": "InnerCamisole",
    "下着": "Underwear",

    # =========================
    # 靴・履き物（拡張）
    # =========================
    "ニーハイブーツ": "KneeHighBoots",
    "ショートブーツ": "ShortBoots",
    "ハイヒール": "HighHeels",
    "パンプス": "Pumps",
    "スニーカー": "Sneakers",
    "ブーツ": "Boots",
    "サンダル": "Sandals",
    "ローファー": "Loafers",
    "靴": "Shoes",

    # =========================
    # 靴下・脚装飾
    # =========================
    "ニーハイソックス": "KneeHighSocks",
    "オーバーニーソックス": "OverKneeSocks",
    "網タイツ": "FishnetTights",
    "レッグウォーマー": "LegWarmer",
    "ストッキング": "Stockings",
    "靴下": "Socks",

    # =========================
    # 服の構造パーツ（重要）
    # =========================
    "エポレット": "Epaulet",
    "ウエストベルト": "WaistBelt",
    "ファスナー": "Zipper",
    "チャック": "Zipper",
    "前立て": "Placket",
    "ハトメ": "Eyelet",
    "裏地": "Lining",
    "表地": "OuterFabric",
    "肩パッド": "ShoulderPad",
    "ポケット": "Pocket",
    "フード": "Hood",
    "袖口": "Cuff",
    "袖": "Sleeve",
    "裾": "Hem",
    "襟": "Collar",
    "ボタン": "Button",
    "ベルト": "Belt",

    # =========================
    # 布・素材系（マテリアル分離用）
    # =========================
    "合成皮革": "SyntheticLeather",
    "本革": "GenuineLeather",
    "デニム生地": "DenimFabric",
    "メッシュ生地": "MeshFabric",
    "レース生地": "LaceFabric",
    "サテン生地": "SatinFabric",
    "シフォン生地": "ChiffonFabric",
    "コットン生地": "CottonFabric",
    "ウール生地": "WoolFabric",

    # =========================
    # 装飾パーツ（揺れ物・物理用）
    # =========================
    "フリル装飾": "FrillDeco",
    "リボン装飾": "RibbonDeco",
    "刺繍装飾": "EmbroideryDeco",
    "ワッペン": "Patch",
    "フリル": "Frill",
    "リボン": "Ribbon",
    "レース": "Lace",

    # =========================
    # 描画補助
    # =========================
    "輪郭": "Outline",
    "ライン": "Line",
    "影": "Shadow",

    # =========================
    # 方向・左右（長い表記 → 短い表記）
    # =========================
    "（左）": " L",
    "（右）": " R",
    "左": " L",
    "右": " R",
    "前": "Front",
    "後ろ": "Back",
    "後": "Back",
    "上": "Up",
    "下": "Down",
}


EN_TO_JA_DICT = {v.strip(): k for k, v in TRANSLATION_DICT.items() if not k.startswith(('.', '_', '（'))}
EN_TO_JA_DICT['L'] = '左'
EN_TO_JA_DICT['R'] = '右'

def contains_japanese(text):
    return bool(re.search(r'[\u3040-\u9faf]', text))

def translate_jp_to_en(name):
    new_name = name
    for jp, en in TRANSLATION_DICT.items():
        new_name = new_name.replace(jp, en)
    intermediate_name = re.sub(r'[_\-\.]+', ' ', new_name)
    return intermediate_name.title().replace(' ', '')

def translate_en_to_jp(name):
    words = re.findall(r'[A-Z][a-z]*|[A-Z]+(?=[A-Z]|$)|[0-9]+', name)
    translated_words = [EN_TO_JA_DICT.get(word, word) for word in words]
    return ''.join(translated_words)

class CITRON_OT_RenameUtility(bpy.types.Operator):
    bl_idname = "citron.rename_utility"
    bl_label = "名前を変換"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.citron_rename_settings
        total_renamed = 0
        target_objects = context.selected_objects if settings.scope == 'SELECTED' else context.scene.objects
        translator, checker = (translate_jp_to_en, contains_japanese) if settings.direction == 'JA_TO_EN' else (translate_en_to_jp, lambda name: not contains_japanese(name))
        processed = set()
        
        if settings.rename_objects:
            for obj in target_objects:
                if obj.name not in processed and checker(obj.name):
                    obj.name = translator(obj.name); processed.add(obj.name); total_renamed += 1
        if settings.rename_bones:
            for arm_obj in [obj for obj in target_objects if obj.type == 'ARMATURE']:
                for pbone in arm_obj.pose.bones:
                    if pbone.name not in processed and checker(pbone.name):
                        pbone.name = translator(pbone.name); processed.add(pbone.name); total_renamed += 1
        if settings.rename_materials:
            for obj in target_objects:
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.name not in processed and checker(mat_slot.material.name):
                        mat_slot.material.name = translator(mat_slot.material.name); processed.add(mat_slot.material.name); total_renamed += 1
        if settings.rename_shapekeys:
            for mesh_obj in [obj for obj in target_objects if obj.type == 'MESH' and obj.data.shape_keys]:
                for sk in mesh_obj.data.shape_keys.key_blocks:
                    if sk.name not in processed and checker(sk.name):
                        sk.name = translator(sk.name); processed.add(sk.name); total_renamed += 1
        
        self.report({'INFO'}, f"合計 {total_renamed} 個の名前を変更しました。")
        return {'FINISHED'}

class CITRON_RenameSettings(bpy.types.PropertyGroup):
    direction: bpy.props.EnumProperty(name="変換方向", items=[('JA_TO_EN', "日本語 → 英語", ""), ('EN_TO_JA', "英語 → 日本語", "")], default='JA_TO_EN')
    scope: bpy.props.EnumProperty(name="対象範囲", items=[('ALL', "シーン全体", ""), ('SELECTED', "選択中のみ", "")], default='ALL')
    rename_objects: bpy.props.BoolProperty(name="オブジェクト / エンプティ", default=True)
    rename_bones: bpy.props.BoolProperty(name="ボーン", default=True)
    rename_materials: bpy.props.BoolProperty(name="マテリアル", default=False)
    rename_shapekeys: bpy.props.BoolProperty(name="シェイプキー", default=False)
