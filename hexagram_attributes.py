"""
玄机一撮 - 卦象属性模块
包含八卦和六十四卦的象征意义、能量属性等信息
"""

# 八卦基本属性
# 格式：{卦名: {属性名: 属性值}}
BAGUA_ATTRIBUTES = {
    "乾": {
        "symbol": "☰",
        "natural_symbol": "天",
        "core_energy": "刚健、创造、领导力、纯粹的阳性能量、动力、天行健",
        "natural_meaning": "天、宇宙、穹苍、太阳、冰、金属（坚硬）、圆形物体",
        "energy_traits": "最纯粹、最强大的阳性（主动、扩张、创造）能量。代表无限的创造力、永恒的运动、强大的意志力、领导才能、权威、尊贵、刚强、进取、圆满、成功。能量向上、向外发散。",
        "human_meaning": "君主、父亲、首领、英雄、君子、刚健之人、开创者、决策者",
        "body_parts": "头、大脑、骨骼、肺部（主气）",
        "direction": "西北方（秋冬之交）",
        "element": "金",
        "key_traits": "主动、不息、自强不息、统领全局。能量如天一般高远、刚健、运行不止。"
    },
    "坤": {
        "symbol": "☷",
        "natural_symbol": "地",
        "core_energy": "柔顺、承载、包容、滋养、纯粹阴性能量、稳定、厚德载物",
        "natural_meaning": "大地、田野、平原、土壤、母亲、承载万物的容器、方形物体、布匹、牛",
        "energy_traits": "最纯粹、最深厚的阴性（被动、接纳、孕育）能量。代表无限的包容力、承载力、滋养力、顺从、柔韧、稳定、忍耐、奉献、积累、财富（大地生养万物）。能量向下、向内收敛。",
        "human_meaning": "母亲、皇后、臣民、百姓、包容者、养育者、实干家、后勤支持者",
        "body_parts": "腹部、脾胃（主运化吸收）、肌肉",
        "direction": "西南方（夏末秋初）",
        "element": "土",
        "key_traits": "主静、包容、顺承、化育万物。能量如大地一般厚重、安稳、默默承载滋养一切。"
    },
    "震": {
        "symbol": "☳",
        "natural_symbol": "雷",
        "core_energy": "震动、激发、行动、新生、奋起、变动",
        "natural_meaning": "雷、震动、地震、惊蛰、龙、足部运动、竹子（节节向上）、草木破土新生",
        "energy_traits": "代表能量的突然爆发、启动、唤醒、激发、行动力、进取心、破除旧事物、带来新气象（如春雷唤醒万物）。具有不安定、躁动、令人警醒的特性。能量从下（一阳爻）向上（两阴爻）突破。",
        "human_meaning": "长子、行动者、开拓者、改革者、军人、运动员、发出号令者。也代表恐惧、惊慌（如雷震）",
        "body_parts": "足、肝脏（主疏泄、条达）、神经系统（受惊）",
        "direction": "东方（春季）",
        "element": "木",
        "key_traits": "主动、启动、激发、变动、带来生机与活力（也可能带来动荡）。"
    },
    "巽": {
        "symbol": "☴",
        "natural_symbol": "风",
        "core_energy": "进入、渗透、顺从、传播、流通、谦逊、无孔不入",
        "natural_meaning": "风、气流、木（可弯曲）、绳索、长条形物、管道、信息传播、鸡（司晨）",
        "energy_traits": "代表能量的流动、渗透、扩散、沟通、调和、顺从、谦逊、适应性强。如风一般无孔不入，能进入最细微的地方。具有柔中带刚的特性（两阳爻在上有力量，一阴爻在下能顺入）。",
        "human_meaning": "长女、商人、教师、传播者（记者、信使）、技术人员、修行者、谦逊之人",
        "body_parts": "股（大腿）、胆（主决断）、呼吸系统（风入）",
        "direction": "东南方（春夏之交）",
        "element": "木",
        "key_traits": "主入、流通、传播、调和、柔顺而有力。"
    },
    "坎": {
        "symbol": "☵",
        "natural_symbol": "水",
        "core_energy": "险陷、流动、下沉、智慧、内藏刚健、深不可测",
        "natural_meaning": "水、雨、云、雾、江河、沟渠、深渊、月亮、车轮、弓轮、猪（喜水）",
        "energy_traits": "代表向下流动、内聚、险阻、陷落、危险、挑战、阴暗、寒冷。但中间一阳爻象征内藏的刚健、智慧、生命力（如水滴石穿）。具有外柔（上下阴爻）内刚（中间阳爻）的特性。能量向下、向内聚集。",
        "human_meaning": "中男、谋士、智者、冒险家、陷入困境者、盗贼（坎为盗）、劳碌者",
        "body_parts": "耳朵、肾脏（主水、藏精）、泌尿生殖系统、血液（体液）",
        "direction": "北方（冬季）",
        "element": "水",
        "key_traits": "主险、主藏、主智、外虚内实。能量如深渊之水，表面平静暗藏激流。"
    },
    "离": {
        "symbol": "☲",
        "natural_symbol": "火",
        "core_energy": "光明、美丽、依附、热情、上升、文明、外显",
        "natural_meaning": "火、太阳、闪电、光明、温暖、雉鸟（羽毛艳丽）、龟（甲壳花纹）、甲胄、网络（连接）",
        "energy_traits": "代表向上燃烧、发光发热、照耀、美丽、文明、热情、依附（火需附着于物）、清晰、洞察力（光明）。具有外刚（上下阳爻）内柔（中间阴爻，需依附）的特性。能量向上、向外发散。",
        "human_meaning": "中女、文人、艺术家、美人、军人（甲胄）、依附者（如臣依附君）、有洞察力者",
        "body_parts": "眼睛、心脏（主神明）、小肠、血液（循环）",
        "direction": "南方（夏季）",
        "element": "火",
        "key_traits": "主明、主丽、主附。能量如火焰般明亮、温暖、升腾，照亮一切。"
    },
    "艮": {
        "symbol": "☶",
        "natural_symbol": "山",
        "core_energy": "静止、稳定、阻碍、止息、敦厚、积累、界限",
        "natural_meaning": "山、丘陵、土石、堤坝、门阙、狗（守门）、果实（成熟落地而止）",
        "energy_traits": "代表能量的停止、静止、稳定、稳固、阻挡、积累、沉淀、厚重、保守、界限。如山一般巍然不动，提供依靠也形成阻碍。能量在上（一阳爻）而止于下（两阴爻）。",
        "human_meaning": "少男、守成者、守护者（门卫、保安）、修行者（静坐）、隐士、固执者",
        "body_parts": "手、背部、鼻（突出如山）、脾胃（主肌肉，艮为山，土石堆积）",
        "direction": "东北方（冬春之交）",
        "element": "土",
        "key_traits": "主止、主静、主成、主稳重。能量如山岳般沉稳、不动，是止息和积累之所。"
    },
    "兑": {
        "symbol": "☱",
        "natural_symbol": "泽",
        "core_energy": "喜悦、言说、沟通、愉悦、润泽、缺口、毁折",
        "natural_meaning": "泽（湖泊、沼泽）、水聚集处、缺口（如山口、河口）、雨露、羊（温顺喜悦）、口舌、巫祝",
        "energy_traits": "代表喜悦、快乐、言谈、沟通、交流、滋润、感召力、魅力。也象征缺口、破损（兑上缺）和因喜悦而可能导致的松懈（毁折）。能量外显（两阳爻在下）而口开（上阴爻为开口）。",
        "human_meaning": "少女、演说家、歌者、律师、公关人员、喜悦之人、朋友相聚、娱乐业者。也代表口舌是非",
        "body_parts": "口、舌、牙齿、咽喉、肺（主发声）、内分泌（润泽）",
        "direction": "西方（秋季）",
        "element": "金",
        "key_traits": "主悦、主说、主润。能量如湖泊般平静喜悦，滋养万物，也如开口般善于表达。"
    }
}

# 六十四卦符号映射
# 格式：{卦名: 卦符号}
HEXAGRAM_SYMBOLS = {
    "乾为天卦": "☰☰",
    "坤为地卦": "☷☷",
    "水雷屯卦": "☵☳",
    "山水蒙卦": "☶☵",
    "水天需卦": "☵☰",
    "天水讼卦": "☰☵",
    "地水师卦": "☷☵",
    "水地比卦": "☵☷",
    "风天小畜卦": "☴☰",
    "天泽履卦": "☰☱",
    "地天泰卦": "☷☰",
    "天地否卦": "☰☷",
    "天火同人卦": "☰☲",
    "火天大有卦": "☲☰",
    "地山谦卦": "☷☶",
    "雷地豫卦": "☳☷",
    "泽雷随卦": "☱☳",
    "山风蛊卦": "☶☴",
    "地泽临卦": "☷☱",
    "风地观卦": "☴☷",
    "火雷噬嗑卦": "☲☳",
    "山火贲卦": "☶☲",
    "山地剥卦": "☶☷",
    "地雷复卦": "☷☳",
    "天雷无妄卦": "☰☳",
    "山天大畜卦": "☶☰",
    "山雷颐卦": "☶☳",
    "泽风大过卦": "☱☴",
    "坎为水卦": "☵☵",
    "离为火卦": "☲☲",
    "泽山咸卦": "☱☶",
    "雷风恒卦": "☳☴",
    "天山遁卦": "☰☶",
    "雷天大壮卦": "☳☰",
    "火地晋卦": "☲☷",
    "地火明夷卦": "☷☲",
    "风火家人卦": "☴☲",
    "火泽睽卦": "☲☱",
    "水山蹇卦": "☵☶",
    "雷水解卦": "☳☵",
    "山泽损卦": "☶☱",
    "风雷益卦": "☴☳",
    "泽天夬卦": "☱☰",
    "天风姤卦": "☰☴",
    "泽地萃卦": "☱☷",
    "地风升卦": "☷☴",
    "泽水困卦": "☱☵",
    "水风井卦": "☵☴",
    "泽火革卦": "☱☲",
    "火风鼎卦": "☲☴",
    "震为雷卦": "☳☳",
    "艮为山卦": "☶☶",
    "风山渐卦": "☴☶",
    "雷泽归妹卦": "☳☱",
    "雷火丰卦": "☳☲",
    "火山旅卦": "☲☶",
    "巽为风卦": "☴☴",
    "兑为泽卦": "☱☱",
    "风水涣卦": "☴☵",
    "水泽节卦": "☵☱",
    "风泽中孚卦": "☴☱",
    "雷山小过卦": "☳☶",
    "水火既济卦": "☵☲",
    "火水未济卦": "☲☵"
}

# 根据卦名获取卦象符号
def get_hexagram_symbol(hexagram_name):
    """根据卦名获取卦象符号"""
    return HEXAGRAM_SYMBOLS.get(hexagram_name, "")

# 根据卦名获取卦象能量属性描述
def get_hexagram_attributes(hexagram_name):
    """根据卦名获取卦象的能量属性描述
    
    Args:
        hexagram_name: 卦名，如"乾为天卦"
    
    Returns:
        包含卦象能量属性的字典
    """
    # 提取上下卦
    if "为" in hexagram_name and len(hexagram_name) <= 5:
        # 单卦，如"乾为天卦"、"坤为地卦"
        gua_name = hexagram_name[0]
        if gua_name in BAGUA_ATTRIBUTES:
            return BAGUA_ATTRIBUTES[gua_name]
    else:
        # 复合卦，如"水雷屯卦"、"天水讼卦"
        # 去除"卦"字
        name_without_suffix = hexagram_name.replace("卦", "")
        
        # 处理不同的命名模式
        if "为" in name_without_suffix:
            # 处理如"乾为天"的格式
            gua_name = name_without_suffix.split("为")[0]
            if gua_name in BAGUA_ATTRIBUTES:
                return BAGUA_ATTRIBUTES[gua_name]
        else:
            # 处理如"水雷屯"的格式，提取前两个字符作为上下卦
            if len(name_without_suffix) >= 2:
                upper_gua = name_without_suffix[0]
                lower_gua = name_without_suffix[1]
                
                # 查找上下卦的属性
                upper_attr = BAGUA_ATTRIBUTES.get(upper_gua, {})
                lower_attr = BAGUA_ATTRIBUTES.get(lower_gua, {})
                
                if upper_attr and lower_attr:
                    # 合并上下卦的属性
                    return {
                        "upper_gua": upper_gua,
                        "lower_gua": lower_gua,
                        "upper_symbol": upper_attr.get("symbol", ""),
                        "lower_symbol": lower_attr.get("symbol", ""),
                        "upper_element": upper_attr.get("element", ""),
                        "lower_element": lower_attr.get("element", ""),
                        "upper_energy": upper_attr.get("core_energy", ""),
                        "lower_energy": lower_attr.get("core_energy", ""),
                        "combined_meaning": f"{upper_gua}({upper_attr.get('natural_symbol', '')})在上，{lower_gua}({lower_attr.get('natural_symbol', '')})在下，"
                                        f"代表{upper_attr.get('core_energy', '')}与{lower_attr.get('core_energy', '')}的能量组合。"
                    }
    
    # 如果无法解析，返回空字典
    return {}

# 根据卦名获取卦象符号和名称的组合
def get_hexagram_display(hexagram_name):
    """获取用于显示的卦象符号和名称组合
    
    Args:
        hexagram_name: 卦名，如"乾为天卦"
    
    Returns:
        组合后的字符串，如"☰☰ 乾为天卦"
    """
    symbol = get_hexagram_symbol(hexagram_name)
    if symbol:
        return f"{symbol} {hexagram_name}"
    return hexagram_name

# 获取所有卦象的显示名称列表
def get_all_hexagram_displays():
    """获取所有卦象的显示名称列表，用于选择框
    
    Returns:
        包含所有卦象显示名称的列表，如["☰☰ 乾为天卦", "☷☷ 坤为地卦", ...]
    """
    # 导入HEXAGRAM_CODES以保持顺序一致
    from hexagram_codes import HEXAGRAM_CODES
    
    # 按照原始顺序生成显示名称
    return [get_hexagram_display(name) for name in HEXAGRAM_CODES.keys()]

# 从显示名称中提取卦名
def get_hexagram_name_from_display(display_name):
    """从显示名称中提取卦名
    
    Args:
        display_name: 显示名称，如"☰☰ 乾为天卦"
    
    Returns:
        卦名，如"乾为天卦"
    """
    # 去除前面的符号部分
    parts = display_name.split(" ", 1)
    if len(parts) > 1:
        return parts[1]
    return display_name 