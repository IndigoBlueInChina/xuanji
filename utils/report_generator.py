"""
玄机一撮 - 报告生成模块
包含生成Markdown和HTML报告的函数
"""
import streamlit as st
from markdown import markdown
from styles.theme import get_report_html_style, get_hexagram_style
from utils.hexagram_renderer import generate_hexagram_html
from hexagram_codes import get_hexagram_name, calculate_changed_hexagram, calculate_inverse_hexagram, calculate_mutual_hexagram
import datetime

def create_markdown(content, filename="解卦报告.md", question="", background="", external_signs="", hexagram="", changing_lines=""):
    """创建Markdown文件"""
    # 获取当前日期和时间
    now = datetime.datetime.now()
    date_str = now.strftime("%Y年%m月%d日 %H:%M")
    
    # 构建问卦信息部分
    inquiry_info = f"""
# 周易解卦报告

## 问卦信息

- **所问何事**：{question}
- **是何因缘**：{background}
- **外应**：{external_signs}
- **得卦**：{hexagram}
- **动爻**：{changing_lines}

## 解卦结果

"""
    
    # 添加生成日期
    footer = f"\n\n---\n\n*报告生成时间：{date_str}*"
    
    # 组合完整内容
    full_content = inquiry_info + content + footer
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_content)
    return filename

def create_pdf(content, filename="解卦报告.pdf", hexagram_code=None, changing_line_numbers=None, 
               question="", background="", external_signs="", hexagram="", changing_lines=""):
    """创建HTML文件，用户可以通过浏览器打印为PDF"""
    try:
        # 创建HTML文件而不是PDF
        html_filename = filename.replace('.pdf', '.html')
        
        # 获取当前日期和时间
        now = datetime.datetime.now()
        date_str = now.strftime("%Y年%m月%d日 %H:%M")
        
        # 构建问卦信息HTML
        inquiry_info_html = f"""
        <div class="inquiry-info">
            <h2>问卦信息</h2>
            <table class="info-table">
                <tr>
                    <th>所问何事</th>
                    <td>{question}</td>
                </tr>
                <tr>
                    <th>是何因缘</th>
                    <td>{background}</td>
                </tr>
                <tr>
                    <th>外应</th>
                    <td>{external_signs}</td>
                </tr>
                <tr>
                    <th>得卦</th>
                    <td>{hexagram}</td>
                </tr>
                <tr>
                    <th>动爻</th>
                    <td>{changing_lines}</td>
                </tr>
            </table>
        </div>
        """
        
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
        
        # 添加表格样式
        additional_style = """
        <style>
            .info-table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 2rem;
            }
            
            .info-table th, .info-table td {
                padding: 0.8rem;
                text-align: left;
                border-bottom: 1px solid #e8d8c0;
            }
            
            .info-table th {
                width: 20%;
                background-color: #f0e6d2;
                color: #6b5344;
                font-weight: bold;
            }
            
            .date-footer {
                text-align: right;
                margin-top: 3rem;
                color: #6b5344;
                font-style: italic;
            }
        </style>
        """
        
        # 组合完整HTML
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>解卦报告</title>
            {report_style}
            {additional_style}
            {hexagram_style if hexagram_code else ""}
        </head>
        <body>
            <div class="report-container">
                <h1>玄机一撮 - {hexagram}</h1>
                {inquiry_info_html}
                {hexagram_html}
                <div class="section">
                    <h2>解卦结果</h2>
                    {html_content}
                </div>
                <div class="date-footer">
                    报告生成时间：{date_str}
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