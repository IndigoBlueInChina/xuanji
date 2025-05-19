"""
玄机一撮 - 报告生成模块
包含生成Markdown和HTML报告的函数
"""
import streamlit as st
from markdown import markdown
from styles.theme import get_report_html_style, get_hexagram_style
from utils.hexagram_renderer import generate_hexagram_html
from hexagram_codes import get_hexagram_name, calculate_changed_hexagram, calculate_inverse_hexagram, calculate_mutual_hexagram

def create_markdown(content, filename="解卦报告.md"):
    """创建Markdown文件"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def create_pdf(content, filename="解卦报告.pdf", hexagram_code=None, changing_line_numbers=None):
    """创建HTML文件，用户可以通过浏览器打印为PDF"""
    try:
        # 创建HTML文件而不是PDF
        html_filename = filename.replace('.pdf', '.html')
        
        # 将Markdown内容转换为HTML
        html_content = markdown(content)
        
        # 生成卦图HTML
        hexagram_html = ""
        if hexagram_code:
            # 获取卦象样式
            hexagram_style = get_hexagram_style()
            
            # 本卦
            original_hexagram_html = generate_hexagram_html(hexagram_code, changing_line_numbers)
            
            # 交互卦
            mutual_code = calculate_mutual_hexagram(hexagram_code)
            mutual_hexagram = get_hexagram_name(mutual_code)
            mutual_hexagram_html = generate_hexagram_html(mutual_code)
            
            # 变卦（如果有动爻）
            changed_hexagram_html = ""
            if changing_line_numbers:
                changed_code = calculate_changed_hexagram(hexagram_code, changing_line_numbers)
                changed_hexagram = get_hexagram_name(changed_code)
                changed_hexagram_html = f"""
                <div class="hexagram-item">
                    <div class="hexagram-title">变卦：{changed_hexagram}</div>
                    {generate_hexagram_html(changed_code, changing_line_numbers, mark_changed_lines=True)}
                </div>
                """
            
            # 综卦
            inverse_code = calculate_inverse_hexagram(hexagram_code)
            inverse_hexagram = get_hexagram_name(inverse_code)
            inverse_hexagram_html = generate_hexagram_html(inverse_code)
            
            # 组合卦图HTML
            hexagram_html = f"""
            <div class="hexagram-display">
                <div class="hexagram-item">
                    <div class="hexagram-title">本卦</div>
                    {original_hexagram_html}
                </div>
                
                <div class="hexagram-item">
                    <div class="hexagram-title">交互卦：{mutual_hexagram}</div>
                    {mutual_hexagram_html}
                </div>
                
                {changed_hexagram_html}
                
                <div class="hexagram-item">
                    <div class="hexagram-title">综卦：{inverse_hexagram}</div>
                    {inverse_hexagram_html}
                </div>
            </div>
            """
        
        # 获取报告样式
        report_style = get_report_html_style()
        
        # 组合完整HTML
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>解卦报告</title>
            {report_style}
            {hexagram_style if hexagram_code else ""}
        </head>
        <body>
            <div class="report-container">
                <h1>周易解卦报告</h1>
                {hexagram_html}
                <div class="section">
                    {html_content}
                </div>
                <div class="footer">
                    玄机一撮 | 基于邵康节一撮金的周易解卦系统
                </div>
            </div>
        </body>
        </html>
        """
        
        # 写入HTML文件
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        return html_filename
    except Exception as e:
        st.error(f"HTML生成失败: {str(e)}")