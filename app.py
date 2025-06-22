import streamlit as st
import os
import subprocess
import datetime
from dotenv import load_dotenv
from hexagram_codes import HEXAGRAM_CODES, get_hexagram_code, get_hexagram_name, calculate_changed_hexagram, calculate_inverse_hexagram, calculate_mutual_hexagram
# 导入新的卦象属性模块
from hexagram_attributes import get_hexagram_display, get_all_hexagram_displays, get_hexagram_name_from_display

# 导入拆分出去的模块
from services.interpretation_service import get_interpretation
from utils.hexagram_renderer import generate_hexagram_html
from utils.report_generator import create_markdown, create_pdf
from styles.theme import get_main_theme, get_hexagram_container_style

# 设置页面配置（必须是第一个Streamlit命令）
st.set_page_config(page_title="玄机一撮", page_icon="🎴", layout="wide")

# 加载环境变量
load_dotenv()

# 六十四卦列表
HEXAGRAMS = list(HEXAGRAM_CODES.keys())

# 在set_custom_theme函数中添加以下代码
def set_custom_theme():
    """设置自定义主题"""
    # 设置自定义CSS样式
    st.markdown(get_main_theme(), unsafe_allow_html=True)
    
    # 添加额外的CSS来覆盖Streamlit默认样式
    st.markdown("""
    <style>
    /* 版本信息样式 */
    .version-info {
        color: #8b7355;
        font-size: 0.8rem;
        text-align: right;
        margin-top: 20px;
        font-family: 'Courier New', monospace;
    }
    
    /* 覆盖Streamlit默认样式 */
    .stMultiselect [data-baseweb="tag"] {
        background-color: #d4a76a !important;
        border-color: #d4a76a !important;
    }
    
    .stMultiselect [data-baseweb="tag"] span {
        color: white !important;
        font-size: 0.9rem !important;
    }
    
    /* 调整下拉菜单样式 */
    [data-baseweb="select"] {
        font-size: 0.95rem !important;
    }
    
    [data-baseweb="popover"] {
        background-color: #fffdf7 !important;
    }
    
    /* 调整选择框高度 */
    .stSelectbox, .stMultiselect {
        margin-bottom: 1rem !important;
    }
    
    /* 调整多选列表项的字体大小 */
    [data-baseweb="menu"] [role="option"] {
        font-size: 0.9rem !important;
    }
    
    /* 调整选择标签的样式 */
    [data-baseweb="tag"] {
        background-color: #d4a76a !important;
        border-color: #d4a76a !important;
        font-size: 0.85rem !important;
        padding: 2px 8px !important;
    }
    
    /* 调整删除标签按钮的大小 */
    [data-baseweb="tag"] [data-baseweb="icon"] {
        width: 14px !important;
        height: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # 应用自定义主题
    set_custom_theme()
    
    # 添加装饰元素
    st.markdown('<div class="decoration-top">☯ ☯ ☯</div>', unsafe_allow_html=True)
    
    # 标题区域和版本信息
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1>玄机一撮</h1>', unsafe_allow_html=True)
    with col2:
        version_info = get_version_info()
        st.markdown(f'<div style="text-align: right; color: #8b7355; font-size: 0.8rem; margin-top: 20px;">版本: {version_info}</div>', unsafe_allow_html=True)
    
    # 创建卡片式布局
    st.markdown('---', unsafe_allow_html=True)
    
    # 创建两列布局：左侧输入区，右侧卦图

    

    st.markdown('<div class="section-title">问卦信息</div>', unsafe_allow_html=True)
    question = st.text_area("所问何事", height=100, 
                        placeholder="例如：我近期的事业发展如何？")
    background = st.text_area("是何因缘", height=100,
                            placeholder="例如：我目前在一家科技公司工作，正考虑转行...")
    external_signs = st.text_area("外应", height=100,
                                placeholder="例如：最近梦见水流，路上遇到黑猫...")
    
    st.markdown('<div class="section-title">卦象选择</div>', unsafe_allow_html=True)
    
    # 使用带符号的卦象显示列表
    hexagram_displays = get_all_hexagram_displays()
    selected_display = st.selectbox("得卦", hexagram_displays)
    
    # 从显示名称中提取实际卦名
    hexagram = get_hexagram_name_from_display(selected_display)
    
    changing_lines = st.multiselect(
        "请选择动爻",  # 移除"（可多选）"，因为多选框本身就暗示可以多选
        ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
    )
    
    # 移除"已选动爻"标签和显示
    # 以下代码应该被删除：
    # if changing_lines:
    #     st.markdown("<div>已选动爻：</div>", unsafe_allow_html=True)
    #     tags_html = ""
    #     for line in changing_lines:
    #         tags_html += f'<span class="changing-line-tag">{line}</span>'
    #     st.markdown(tags_html, unsafe_allow_html=True)


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
        # 添加卦图容器样式
        st.markdown(get_hexagram_container_style(), unsafe_allow_html=True)
        
        # 创建四列布局显示卦图
        col1, col2, col3, col4 = st.columns(4)
        
        # 本卦
        with col1:
            st.markdown(f'<div class="hexagram-container"><div class="hexagram-title">本卦：{get_hexagram_display(hexagram)}</div>', unsafe_allow_html=True)
            hexagram_html = generate_hexagram_html(hexagram_code, changing_line_numbers)
            st.components.v1.html(hexagram_html, height=150)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 交互卦
        with col2:
            mutual_code = calculate_mutual_hexagram(hexagram_code)
            mutual_hexagram = get_hexagram_name(mutual_code)
            st.markdown(f'<div class="hexagram-container"><div class="hexagram-title">交互卦：{get_hexagram_display(mutual_hexagram)}</div>', unsafe_allow_html=True)
            mutual_hexagram_html = generate_hexagram_html(mutual_code)
            st.components.v1.html(mutual_hexagram_html, height=150)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 变卦（如果有动爻）
        with col3:
            if changing_line_numbers:
                changed_code = calculate_changed_hexagram(hexagram_code, changing_line_numbers)
                changed_hexagram = get_hexagram_name(changed_code)
                st.markdown(f'<div class="hexagram-container"><div class="hexagram-title">变卦：{get_hexagram_display(changed_hexagram)}</div>', unsafe_allow_html=True)
                changed_hexagram_html = generate_hexagram_html(changed_code, changing_line_numbers, mark_changed_lines=True)
                st.components.v1.html(changed_hexagram_html, height=150)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # 综卦
        with col4:
            inverse_code = calculate_inverse_hexagram(hexagram_code)
            inverse_hexagram = get_hexagram_name(inverse_code)
            st.markdown(f'<div class="hexagram-container"><div class="hexagram-title">综卦：{get_hexagram_display(inverse_hexagram)}</div>', unsafe_allow_html=True)
            inverse_hexagram_html = generate_hexagram_html(inverse_code)
            st.components.v1.html(inverse_hexagram_html, height=150)
            st.markdown('</div>', unsafe_allow_html=True)
    
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
        st.markdown('<h2>解卦结果</h2>', unsafe_allow_html=True)
        
        # 显示问题摘要
        st.markdown(f"""
        <div style="background-color: #f0e6d2; padding: 1rem; border-radius: 5px; margin-bottom: 1.5rem;">
            <strong>问题：</strong>{question}<br>
            <strong>卦象：</strong>{get_hexagram_display(hexagram)} {' '.join([f'<span class="changing-line-tag">{line}</span>' for line in changing_lines]) if changing_lines else '(无动爻)'}
        </div>
        """, unsafe_allow_html=True)
        
        # 流式生成解卦结果
        st.markdown('<div class="interpretation">', unsafe_allow_html=True)
        interpretation = get_interpretation(
            question, background, external_signs, hexagram, 
            "、".join(changing_lines) if changing_lines else "无动爻"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if interpretation and not interpretation.startswith("解读生成出错"):
            # 导出按钮
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">导出报告</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            # 创建唯一文件名
            import uuid
            file_id = str(uuid.uuid4())[:8]
            md_filename = f"解卦报告_{file_id}.md"
            pdf_filename = f"解卦报告_{file_id}.pdf"
            
            with col1:
                md_file = create_markdown(
                    interpretation, 
                    md_filename,
                    question=question,
                    background=background,
                    external_signs=external_signs,
                    hexagram=hexagram,
                    changing_lines="、".join(changing_lines) if changing_lines else "无动爻"
                )
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
                        changing_line_numbers,
                        question=question,
                        background=background,
                        external_signs=external_signs,
                        hexagram=hexagram,
                        changing_lines="、".join(changing_lines) if changing_lines else "无动爻"
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

def get_version_info():
    """获取版本信息"""
    try:
        # 获取最新的commit哈希值（短版本）
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'], 
            cwd=os.path.dirname(__file__),
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # 获取最新commit的时间戳
        commit_time = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ci'], 
            cwd=os.path.dirname(__file__),
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # 转换为更友好的格式
        commit_datetime = datetime.datetime.strptime(commit_time[:19], '%Y-%m-%d %H:%M:%S')
        formatted_time = commit_datetime.strftime('%Y-%m-%d %H:%M')
        
        return f"v{commit_hash} ({formatted_time})"
    except:
        # 如果获取Git信息失败，使用当前时间戳
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        return f"dev ({current_time})"

if __name__ == "__main__":
    main()