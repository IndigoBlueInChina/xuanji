"""二十四节气和三候计算模块"""
from datetime import datetime
import math

# 二十四节气名称
SOLAR_TERMS = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
]

# 十二消息卦（按农历月份对应）
TWELVE_MESSAGE_HEXAGRAMS = {
    1: "地雷复卦",    # 农历正月，一阳生
    2: "地泽临卦",    # 农历二月，二阳生
    3: "地天泰卦",    # 农历三月，三阳生
    4: "雷天大壮卦",  # 农历四月，四阳生
    5: "泽天夬卦",    # 农历五月，五阳生
    6: "天风姤卦",    # 农历六月，一阴生
    7: "天山遁卦",    # 农历七月，二阴生
    8: "天地否卦",    # 农历八月，三阴生
    9: "风地观卦",    # 农历九月，四阴生
    10: "山地剥卦",   # 农历十月，五阴生
    11: "地地坤卦",   # 农历十一月，纯阴
    12: "天天乾卦"    # 农历十二月，纯阳
}

# 三候名称（每个节气分为三候，共72候）
THREE_PENTADS = {
    "立春": ["东风解冻", "蛰虫始振", "鱼陟负冰"],
    "雨水": ["獭祭鱼", "候雁北", "草木萌动"],
    "惊蛰": ["桃始华", "仓庚鸣", "鹰化为鸠"],
    "春分": ["玄鸟至", "雷乃发声", "始电"],
    "清明": ["桐始华", "田鼠化为鴽", "虹始见"],
    "谷雨": ["萍始生", "鸣鸠拂其羽", "戴胜降于桑"],
    "立夏": ["蝼蝈鸣", "蚯蚓出", "王瓜生"],
    "小满": ["苦菜秀", "靡草死", "麦秋至"],
    "芒种": ["螳螂生", "鵙始鸣", "反舌无声"],
    "夏至": ["鹿角解", "蜩始鸣", "半夏生"],
    "小暑": ["温风至", "蟋蟀居宇", "鹰始挚"],
    "大暑": ["腐草为萤", "土润溽暑", "大雨时行"],
    "立秋": ["凉风至", "白露生", "寒蝉鸣"],
    "处暑": ["鹰乃祭鸟", "天地始肃", "禾乃登"],
    "白露": ["鸿雁来", "玄鸟归", "群鸟养羞"],
    "秋分": ["雷始收声", "蛰虫坯户", "水始涸"],
    "寒露": ["鸿雁来宾", "雀入大水为蛤", "菊有黄华"],
    "霜降": ["豺乃祭兽", "草木黄落", "蛰虫咸俯"],
    "立冬": ["水始冰", "地始冻", "雉入大水为蜃"],
    "小雪": ["虹藏不见", "天气上升地气下降", "闭塞而成冬"],
    "大雪": ["鹖鴠不鸣", "虎始交", "荔挺出"],
    "冬至": ["蚯蚓结", "麋角解", "水泉动"],
    "小寒": ["雁北乡", "鹊始巢", "雉始鸲"],
    "大寒": ["鸡乳", "征鸟厉疾", "水泽腹坚"]
}

def calculate_solar_longitude(date):
    """计算太阳黄经（简化算法）"""
    # 获取年份的天数
    year = date.year
    # 计算从年初到当前日期的天数
    start_of_year = datetime(year, 1, 1)
    days_from_start = (date - start_of_year).days
    
    # 简化计算：一年365.25天对应360度
    # 春分（3月20日左右）太阳黄经为0度
    # 估算春分日期（3月20日）
    spring_equinox = datetime(year, 3, 20)
    days_from_spring_equinox = (date - spring_equinox).days
    
    # 计算太阳黄经（度）
    longitude = (days_from_spring_equinox * 360.0 / 365.25) % 360
    return longitude

def get_solar_term_and_pentad(date=None):
    """获取指定日期的节气和候信息"""
    if date is None:
        date = datetime.now()
    
    # 计算太阳黄经
    longitude = calculate_solar_longitude(date)
    
    # 每个节气对应15度黄经
    # 春分为0度，立夏为30度，以此类推
    # 调整起始点：立春为315度（或-45度），春分为0度
    adjusted_longitude = (longitude + 45) % 360
    
    # 计算节气索引（0-23）
    term_index = int(adjusted_longitude // 15)
    
    # 获取节气名称
    solar_term = SOLAR_TERMS[term_index]
    
    # 计算在当前节气中的位置（0-14.99度）
    position_in_term = adjusted_longitude % 15
    
    # 每候5度，计算候数（1-3）
    pentad_index = int(position_in_term // 5)
    pentad_number = pentad_index + 1
    
    # 获取候的名称
    pentad_name = THREE_PENTADS[solar_term][pentad_index]
    
    return {
        'solar_term': solar_term,
        'pentad_number': pentad_number,
        'pentad_name': pentad_name,
        'description': f"{solar_term}第{pentad_number}候：{pentad_name}"
    }

def get_message_hexagram(date=None):
    """获取十二消息卦信息"""
    if date is None:
        date = datetime.now()
    
    # 简化计算：根据公历月份估算农历月份
    # 这里使用简化方法，实际应用中可能需要更精确的农历转换
    month = date.month
    
    # 公历与农历的大致对应（简化处理）
    # 考虑到农历比公历晚约1个月
    lunar_month = month - 1 if month > 1 else 12
    
    message_hexagram = TWELVE_MESSAGE_HEXAGRAMS.get(lunar_month, "未知")
    
    return {
        'lunar_month': lunar_month,
        'message_hexagram': message_hexagram
    }

def get_detailed_solar_info(date=None):
    """获取详细的节气信息"""
    if date is None:
        date = datetime.now()
    
    info = get_solar_term_and_pentad(date)
    message_info = get_message_hexagram(date)
    
    # 计算在整年中的候数（1-72）
    term_index = SOLAR_TERMS.index(info['solar_term'])
    annual_pentad = term_index * 3 + info['pentad_number']
    
    return {
        **info,
        **message_info,
        'annual_pentad': annual_pentad,
        'full_description': f"{info['solar_term']}第{info['pentad_number']}候（全年第{annual_pentad}候）：{info['pentad_name']}，十二消息卦：{message_info['message_hexagram']}"
    }