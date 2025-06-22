"""
玄机一撮 - 卦图渲染模块
包含生成卦象HTML的函数
"""
from styles.theme import get_hexagram_style

def generate_hexagram_html(hexagram_code, changing_lines=None, mark_changed_lines=False, include_html_wrapper=True):
    """
    生成卦象的HTML表示
    
    参数:
    - hexagram_code: 卦象编码，例如 "111111" 表示乾卦
    - changing_lines: 动爻列表，例如 [1, 3, 5] 表示初爻、三爻、五爻为动爻
    - mark_changed_lines: 是否在变卦中标记动爻位置
    - include_html_wrapper: 是否包含完整的HTML文档结构（用于PDF导出时应设为False）
    
    返回:
    - 卦象的HTML字符串
    """
    if not changing_lines:
        changing_lines = []
    
    # 获取卦象样式
    css = get_hexagram_style()
    
    # 生成卦象HTML
    if include_html_wrapper:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            {css}
        </head>
        <body>
            <div class="hexagram">
        """
    else:
        html = '<div class="hexagram">'
    
    # 生成六爻 - 从上到下渲染爻，使上卦在上方，下卦在下方
    # 周易中，卦象的第1-3爻是下卦，第4-6爻是上卦
    # 爻的顺序是从下往上数：初爻(1)、二爻(2)、三爻(3)、四爻(4)、五爻(5)、上爻(6)
    for i in range(5, -1, -1):  # 从5到0，对应第6爻到第1爻
        line_num = 6 - i  # 正确计算爻号：6对应初爻(1)，5对应二爻(2)，以此类推
        is_changing = line_num in changing_lines
        
        if hexagram_code[i] == "1":  # 阳爻
            if is_changing and (not mark_changed_lines or mark_changed_lines):
                html += f'<div class="line"><div class="yang changing"></div></div>'
            else:
                html += f'<div class="line"><div class="yang"></div></div>'
        else:  # 阴爻
            if is_changing and (not mark_changed_lines or mark_changed_lines):
                html += f'<div class="line"><div class="yin changing"></div><div class="yin changing"></div></div>'
            else:
                html += f'<div class="line"><div class="yin"></div><div class="yin"></div></div>'
    
    if include_html_wrapper:
        html += """
            </div>
        </body>
        </html>
        """
    else:
        html += "</div>"
    
    return html