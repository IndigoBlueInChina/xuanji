import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from fpdf import FPDF
import tempfile
from hexagram_codes import HEXAGRAM_CODES, get_hexagram_code, get_hexagram_name, calculate_changed_hexagram, calculate_inverse_hexagram, calculate_mutual_hexagram, get_yicuojin_sentence

# 设置页面配置（必须是第一个Streamlit命令）
st.set_page_config(page_title="玄机一撮", page_icon="🎴", layout="wide")

# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端 (使用兼容模式)
client = OpenAI(
    api_key=os.getenv("LLM_SERVICE_API_KEY"),
    base_url=os.getenv("LLM_SERVICE_BASE_URL")
)

# 配置LLM模型名称
LLM_MODEL = os.getenv("LLM_SERVICE_MODEL", "qwen-plus")

# 六十四卦列表
HEXAGRAMS = list(HEXAGRAM_CODES.keys())

# 生成卦图的HTML代码
def generate_hexagram_html(hexagram_code, changing_lines=None):
    """生成卦图的HTML代码
    
    Args:
        hexagram_code: 卦象编码，如"111010"
        changing_lines: 动爻列表，从1开始，如[1, 3, 5]
    
    Returns:
        卦图的HTML代码
    """
    if not hexagram_code:
        return ""
    
    if changing_lines is None:
        changing_lines = []
    
    html = """
    <style>
    .hexagram {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 20px 0;
    }
    .line {
        width: 100px;
        height: 10px;
        margin: 5px 0;
        display: flex;
    }
    .yang {
        background-color: black;
        width: 100%;
    }
    .yin {
        display: flex;
        width: 100%;
    }
    .yin-left, .yin-right {
        background-color: black;
        width: 45%;
    }
    .yin-middle {
        width: 10%;
    }
    .changing {
        background-color: red;
    }
    </style>
    <div class="hexagram">
    """
    
    for i in range(6):
        line_num = 6 - i  # 从下往上数，初爻为1
        is_changing = line_num in changing_lines
        line_type = hexagram_code[i]
        
        if line_type == "1":  # 阳爻
            if is_changing:
                html += f'<div class="line"><div class="yang changing"></div></div>'
            else:
                html += f'<div class="line"><div class="yang"></div></div>'
        else:  # 阴爻
            if is_changing:
                html += f'<div class="line"><div class="yin"><div class="yin-left changing"></div><div class="yin-middle"></div><div class="yin-right changing"></div></div></div>'
            else:
                html += f'<div class="line"><div class="yin"><div class="yin-left"></div><div class="yin-middle"></div><div class="yin-right"></div></div></div>'
    
    html += "</div>"
    return html

def get_interpretation(question, background, external_signs, hexagram, changing_lines):
    """调用OpenAI API获取卦象解读"""
    prompt_parts = [f"作为一位精通邵康节一撮金的周易专家，请解读以下情况：\n\n问题：{question}"]
    
    if background.strip():
        prompt_parts.append(f"背景：{background}")
    
    if external_signs.strip():
        prompt_parts.append(f"外应：{external_signs}")
    
    prompt_parts.append(f"所得卦象：{hexagram}")
    prompt_parts.append(f"动爻：{changing_lines}")
    
    # 获取原卦的编码
    original_code = get_hexagram_code(hexagram)
    
    # 添加计算得到的交互卦、变卦、综卦的名称
    if changing_lines and original_code:
        # 将动爻文本转换为数字列表
        changing_line_numbers = []
        for line in changing_lines.split("、"):
            if line == "初爻":
                changing_line_numbers.append(1)
            elif line == "二爻":
                changing_line_numbers.append(2)
            elif line == "三爻":
                changing_line_numbers.append(3)
            elif line == "四爻":
                changing_line_numbers.append(4)
            elif line == "五爻":
                changing_line_numbers.append(5)
            elif line == "上爻":
                changing_line_numbers.append(6)
        
        # 计算变卦、综卦和交互卦
        changed_code = calculate_changed_hexagram(original_code, changing_line_numbers)
        inverse_code = calculate_inverse_hexagram(original_code)
        mutual_code = calculate_mutual_hexagram(original_code)
        
        # 获取卦象名称
        changed_hexagram = get_hexagram_name(changed_code)
        inverse_hexagram = get_hexagram_name(inverse_code)
        mutual_hexagram = get_hexagram_name(mutual_code)

        # 获取一撮金原文
        yicuojin_sentence = get_yicuojin_sentence(hexagram, changing_line_numbers)
        
        # 添加到提示中
        if yicuojin_sentence:
            prompt_parts.append(f"一撮金原文：{yicuojin_sentence}")
        if mutual_hexagram:
            prompt_parts.append(f"交互卦：{mutual_hexagram}")
        if changed_hexagram:
            prompt_parts.append(f"变卦：{changed_hexagram}")
        if inverse_hexagram:
            prompt_parts.append(f"综卦：{inverse_hexagram}")
    
    prompt_parts.append("""
请从以下几个方面进行详细解读，解读过程中，需要给出所依据的系辞、卦辞、爻辞、彖辞、象辞、一撮金原文 ：
1. 对问题的具体建议，包括如何应对当前问题、未来发展趋势等
2. 交互卦、变卦、综卦的启示
3. 时间指示（如果有则需说明，没有直接略过），包括可能的时间范围、影响程度等

""")
    
    prompt = "\n".join(prompt_parts)
    print(prompt)

    try:
        # 创建一个占位符用于显示流式输出
        result_placeholder = st.empty()
        full_response = ""
        
        # 使用流式输出模式调用API
        stream = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            stream=True  # 启用流式输出
        )
        
        # 逐步接收并显示响应
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                # 更新显示的内容
                result_placeholder.markdown(full_response)
        
        # 返回完整响应
        return full_response
    except Exception as e:
        return f"解读生成出错：{str(e)}"

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
        from markdown import markdown
        html_content = markdown(content)
        
        # 生成卦图HTML
        hexagram_html = ""
        if hexagram_code:
            # 获取卦象名称
            hexagram_name = get_hexagram_name(hexagram_code)
            
            # 生成本卦图
            hexagram_html += f"""
            <div class="hexagram-section">
                <h3>本卦：{hexagram_name}</h3>
                {generate_hexagram_html(hexagram_code, changing_line_numbers)}
            </div>
            """
            
            # 如果有动爻，生成变卦图
            if changing_line_numbers:
                changed_code = calculate_changed_hexagram(hexagram_code, changing_line_numbers)
                changed_hexagram = get_hexagram_name(changed_code)
                hexagram_html += f"""
                <div class="hexagram-section">
                    <h3>变卦：{changed_hexagram}</h3>
                    {generate_hexagram_html(changed_code)}
                </div>
                """
            
            # 生成交互卦图
            mutual_code = calculate_mutual_hexagram(hexagram_code)
            mutual_hexagram = get_hexagram_name(mutual_code)
            hexagram_html += f"""
            <div class="hexagram-section">
                <h3>交互卦：{mutual_hexagram}</h3>
                {generate_hexagram_html(mutual_code)}
            </div>
            """
            
            # 生成综卦图
            inverse_code = calculate_inverse_hexagram(hexagram_code)
            inverse_hexagram = get_hexagram_name(inverse_code)
            hexagram_html += f"""
            <div class="hexagram-section">
                <h3>综卦：{inverse_hexagram}</h3>
                {generate_hexagram_html(inverse_code)}
            </div>
            """
        
        # 创建完整的HTML文档
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>解卦报告</title>
            <style>
                body {{
                    font-family: "Microsoft YaHei", SimSun, sans-serif;
                    margin: 2cm;
                    background-color: #FFFAF0;
                    color: #333;
                }}
                h1 {{
                    text-align: center;
                    font-size: 24px;
                    color: #8B4513;
                    margin-bottom: 20px;
                    border-bottom: 1px solid #D2B48C;
                    padding-bottom: 10px;
                }}
                h2 {{
                    font-size: 18px;
                    color: #A0522D;
                    margin-top: 20px;
                    border-left: 4px solid #D2B48C;
                    padding-left: 10px;
                }}
                h3 {{
                    font-size: 16px;
                    color: #A0522D;
                    margin-top: 15px;
                }}
                p {{
                    text-indent: 2em;
                    line-height: 1.6;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                    margin-top: 30px;
                    border-top: 1px solid #D2B48C;
                    padding-top: 10px;
                }}
                @media print {{
                    body {{
                        background-color: white;
                    }}
                    .print-button {{
                        display: none;
                    }}
                }}
                .print-button {{
                    display: block;
                    text-align: center;
                    margin: 20px auto;
                    padding: 10px 20px;
                    background-color: #8B4513;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }}
                .print-button:hover {{
                    background-color: #A0522D;
                }}
                .decoration {{
                    text-align: center;
                    margin: 20px 0;
                    color: #8B4513;
                    font-size: 24px;
                }}
                .hexagram-container {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    margin: 20px 0;
                    padding: 10px;
                    background-color: #FFF8DC;
                    border-radius: 10px;
                }}
                .hexagram-section {{
                    margin: 10px 20px;
                    text-align: center;
                }}
                .hexagram {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin: 10px 0;
                }}
                .line {{
                    width: 100px;
                    height: 10px;
                    margin: 5px 0;
                    display: flex;
                }}
                .yang {{
                    background-color: black;
                    width: 100%;
                }}
                .yin {{
                    display: flex;
                    width: 100%;
                }}
                .yin-left, .yin-right {{
                    background-color: black;
                    width: 45%;
                }}
                .yin-middle {{
                    width: 10%;
                }}
                .changing {{
                    background-color: red;
                }}
            </style>
        </head>
        <body>
            <div class="decoration">☯ ☯ ☯</div>
            <h1>解卦报告</h1>
            
            <div class="hexagram-container">
                {hexagram_html}
            </div>
            
            <div>
                {html_content}
            </div>
            <div class="footer">玄机一撮 © 2025 | 周易解卦系统</div>
            <div class="decoration">☯ ☯ ☯</div>
            <button class="print-button" onclick="window.print()">打印为PDF</button>
            <script>
                // 自动调整内容格式
                document.addEventListener('DOMContentLoaded', function() {{
                    // 查找所有引用块并添加样式
                    const paragraphs = document.querySelectorAll('p');
                    paragraphs.forEach(p => {{
                        if (p.textContent.includes('"') && p.textContent.includes('"')) {{
                            p.style.fontStyle = 'italic';
                            p.style.borderLeft = '3px solid #D2B48C';
                            p.style.paddingLeft = '10px';
                            p.style.backgroundColor = '#FFF8DC';
                        }}
                    }});
                }});
            </script>
        </body>
        </html>
        """
        
        # 保存HTML文件
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        return html_filename
    except Exception as e:
        # 如果HTML生成失败，创建文本文件作为备选
        try:
            # 创建一个简单的文本文件作为备选
            txt_filename = filename.replace('.pdf', '.txt')
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(content)
            st.error(f"HTML生成失败: {str(e)}，已创建文本文件作为替代")
            return txt_filename
        except:
            raise Exception(f"无法创建HTML或文本文件: {str(e)}")

def set_custom_theme():
    """设置自定义主题"""
    # 设置自定义CSS样式
    st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #8B4513;
            font-family: "STKaiti", "KaiTi", "Microsoft YaHei", sans-serif;
            text-align: center;
            padding: 20px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        h2, h3, h4 {
            color: #A0522D;
            font-family: "STKaiti", "KaiTi", "Microsoft YaHei", sans-serif;
        }
        .stSubheader {
            color: #A0522D;
            font-family: "STKaiti", "KaiTi", "Microsoft YaHei", sans-serif;
            text-align: center;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #8B4513;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #A0522D;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .stTextArea>div>div>textarea {
            border: 1px solid #D2B48C;
            border-radius: 5px;
            background-color: #FFFAF0;
        }
        .stSelectbox>div>div {
            border: 1px solid #D2B48C;
            border-radius: 5px;
            background-color: #FFFAF0;
        }
        .stMultiSelect>div>div {
            border: 1px solid #D2B48C;
            border-radius: 5px;
            background-color: #FFFAF0;
        }
        .decoration-top {
            text-align: center;
            margin-bottom: 20px;
        }
        .decoration-bottom {
            text-align: center;
            margin-top: 20px;
        }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #777;
            font-size: 0.8em;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    # 应用自定义主题
    set_custom_theme()
    
    # 添加装饰元素
    st.markdown('<div class="decoration-top">☯ ☯ ☯</div>', unsafe_allow_html=True)
    
    st.title("玄机一撮")
    st.subheader("基于邵康节一撮金的周易解卦系统")
    
    # 创建卡片式布局
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 创建两列布局：左侧输入区，右侧卦图
    col1, col2 = st.columns([3, 2])
    
    with col1:
        question = st.text_area("所问何事", height=100, 
                               placeholder="例如：我近期的事业发展如何？")
        background = st.text_area("是何因缘", height=100,
                                placeholder="例如：我目前在一家科技公司工作，正考虑转行...")
        external_signs = st.text_area("外应", height=100,
                                    placeholder="例如：最近梦见水流，路上遇到黑猫...")
        
        hexagram = st.selectbox("得卦", HEXAGRAMS)
        changing_lines = st.multiselect(
            "请选择动爻（可多选）",
            ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
        )
    
    with col2:
        # 获取卦象编码
        hexagram_code = get_hexagram_code(hexagram)
        
        # 将动爻文本转换为数字列表
        changing_line_numbers = []
        for line in changing_lines:
            if line == "初爻":
                changing_line_numbers.append(1)
            elif line == "二爻":
                changing_line_numbers.append(2)
            elif line == "三爻":
                changing_line_numbers.append(3)
            elif line == "四爻":
                changing_line_numbers.append(4)
            elif line == "五爻":
                changing_line_numbers.append(5)
            elif line == "上爻":
                changing_line_numbers.append(6)
        
        # 显示卦图
        if hexagram_code:
            st.markdown("### 本卦")
            hexagram_html = generate_hexagram_html(hexagram_code, changing_line_numbers)
            st.components.v1.html(hexagram_html, height=200)
            
            # 如果有动爻，显示变卦
            if changing_line_numbers:
                changed_code = calculate_changed_hexagram(hexagram_code, changing_line_numbers)
                changed_hexagram = get_hexagram_name(changed_code)
                st.markdown(f"### 变卦：{changed_hexagram}")
                changed_hexagram_html = generate_hexagram_html(changed_code)
                st.components.v1.html(changed_hexagram_html, height=200)
    
    # 居中显示按钮
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        start_button = st.button("开始解卦", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if start_button:
        if not all([question, hexagram]):
            st.error("请至少输入问题和选择卦象")
            return
            
        # 创建结果卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 解卦结果")
        
        # 流式生成解卦结果
        interpretation = get_interpretation(
            question, background, external_signs, hexagram, 
            "、".join(changing_lines) if changing_lines else "无动爻"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if interpretation and not interpretation.startswith("解读生成出错"):
            # 导出按钮
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            # 创建唯一文件名
            import uuid
            file_id = str(uuid.uuid4())[:8]
            md_filename = f"解卦报告_{file_id}.md"
            pdf_filename = f"解卦报告_{file_id}.pdf"
            
            with col1:
                md_file = create_markdown(interpretation, md_filename)
                with open(md_file, "r", encoding="utf-8") as f:
                    st.download_button(
                        "导出为Markdown",
                        f.read(),
                        file_name=md_filename,
                        mime="text/markdown",
                        use_container_width=True
                    )
            
            with col2:
                try:
                    # 获取卦象编码
                    hexagram_code = get_hexagram_code(hexagram)
                    
                    # 创建HTML文件，传入卦象编码和动爻列表
                    html_file = create_pdf(
                        interpretation, 
                        pdf_filename, 
                        hexagram_code, 
                        changing_line_numbers
                    )
                    
                    with open(html_file, "r", encoding="utf-8") as f:
                        st.download_button(
                            "导出为HTML (可打印为PDF)",
                            f.read(),
                            file_name=html_file.split("\\")[-1],
                            mime="text/html",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"HTML生成失败: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 添加页脚
    st.markdown('<div class="footer">玄机一撮 © 2025 | 周易解卦系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="decoration-bottom">☯ ☯ ☯</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()