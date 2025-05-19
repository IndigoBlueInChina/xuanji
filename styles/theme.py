def get_main_theme():
    """获取主应用的CSS样式"""
    return """
    <style>
        /* 全局样式 */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');
        
        body {
            font-family: 'Noto Serif SC', serif;
            background-color: #f8f5e6;
            color: #333;
        }
        
        h1, h2, h3 {
            font-family: 'Noto Serif SC', serif;
            color: #8b4513;
        }
        
        h1 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        h2 {
            font-size: 1.8rem;
            border-bottom: 2px solid #d4a76a;
            padding-bottom: 0.5rem;
            margin-top: 1.5rem;
        }
        
        .subheader {
            text-align: center;
            color: #6b5344;
            margin-bottom: 2rem;
            font-style: italic;
        }
        
        /* 卡片样式 */
        .card {
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid #e8d8c0;
        }
        
        /* 输入区域样式 */
        .stTextArea textarea, .stSelectbox, .stMultiselect {
            background-color: #fffdf7;
            border: 1px solid #d4a76a;
            border-radius: 5px;
            transition: all 0.3s;
        }
        
        .stTextArea textarea:focus, .stSelectbox:focus, .stMultiselect:focus {
            border-color: #8b4513;
            box-shadow: 0 0 0 2px rgba(139, 69, 19, 0.2);
        }
        
        /* 标签样式 */
        label {
            font-weight: bold;
            color: #6b5344;
            font-size: 1.05rem;
        }
        
        /* 按钮样式 */
        .stButton button {
            background-color: #8b4513;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1.5rem;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .stButton button:hover {
            background-color: #a05a2c;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        /* 装饰元素 */
        .decoration-top, .decoration-bottom {
            text-align: center;
            font-size: 1.8rem;
            color: #8b4513;
            margin: 1rem 0;
            letter-spacing: 1rem;
        }
        
        /* 页脚样式 */
        .footer {
            text-align: center;
            color: #6b5344;
            font-size: 0.9rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #e8d8c0;
        }
        
        /* 解卦结果样式 */
        .interpretation {
            line-height: 1.8;
            font-size: 1.05rem;
        }
        
        /* 分区标题 */
        .section-title {
            background-color: #f0e6d2;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            margin: 1.5rem 0 1rem 0;
            font-weight: bold;
            color: #6b5344;
        }
        
        /* 动爻标签样式 */
        .changing-line-tag {
            display: inline-block;
            background-color: #d4a76a;  /* 改为更柔和的颜色，从红色改为棕色 */
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-size: 0.9rem;
            margin-right: 0.5rem;
        }
        
        /* 添加选择框样式 */
        .stSelectbox > div > div {
            font-size: 0.95rem !important;  /* 减小字号 */
        }
        
        .stMultiselect > div > div {
            font-size: 0.95rem !important;  /* 减小字号 */
        }
        
        /* 调整选择框背景颜色 */
        .stSelectbox > div, .stMultiselect > div {
            background-color: #fffdf7 !important;  /* 使用更和谐的背景色 */
            border: 1px solid #d4a76a !important;
        }
        
        /* 响应式调整 */
        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
            
            .card {
                padding: 1rem;
            }
        }
    </style>
    """

def get_hexagram_container_style():
    """获取卦图容器的CSS样式"""
    return """
    <style>
        .hexagram-container {
            background-color: #fffdf7;
            border: 1px solid #e8d8c0;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            text-align: center;
            transition: all 0.3s;
        }
        
        .hexagram-container:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-3px);
        }
        
        .hexagram-title {
            font-weight: bold;
            color: #8b4513;
            margin-bottom: 0.8rem;
            font-size: 1.1rem;
            border-bottom: 1px dashed #d4a76a;
            padding-bottom: 0.5rem;
        }
    </style>
    """

def get_hexagram_style():
    """获取卦象的CSS样式"""
    return """
    <style>
        .hexagram {
            display: flex;
            flex-direction: column-reverse;
            align-items: center;
            gap: 10px;
        }
        
        .line {
            width: 100px;
            height: 12px;
            display: flex;
            justify-content: space-between; /* 修改：使阴爻两段均匀分布 */
            gap: 10px; /* 修改：增加间隔，使阴爻总长度与阳爻相同 */
        }
        
        .yang {
            background-color: #000;
            width: 100%;
            height: 100%;
        }
        
        .yin {
            background-color: #000;
            width: 45%; /* 修改：从45%调整为47.5%，使两段加起来接近阳爻长度 */
            height: 100%;
        }
        
        .changing {
            background-color: #e60000;
        }
        
        .hexagram-name {
            margin-top: 15px;
            font-weight: bold;
            font-size: 1.2rem;
            color: #8b4513;
        }
    </style>
    """

def get_report_html_style():
    """获取报告HTML的CSS样式"""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');
        
        body {
            font-family: 'Noto Serif SC', serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f8f5e6;
        }
        
        .report-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border: 1px solid #e8d8c0;
        }
        
        h1 {
            text-align: center;
            color: #8b4513;
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
            border-bottom: 2px solid #d4a76a;
            padding-bottom: 1rem;
        }
        
        h2 {
            color: #8b4513;
            font-size: 1.5rem;
            margin-top: 2rem;
            border-left: 5px solid #d4a76a;
            padding-left: 1rem;
        }
        
        h3 {
            color: #6b5344;
            font-size: 1.2rem;
            margin-top: 1.5rem;
        }
        
        .hexagram-display {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        
        .hexagram-item {
            text-align: center;
        }
        
        .hexagram-title {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #6b5344;
        }
        
        blockquote {
            background-color: #f0e6d2;
            border-left: 4px solid #d4a76a;
            padding: 1rem;
            margin: 1.5rem 0;
            font-style: italic;
        }
        
        .section {
            margin: 2rem 0;
            padding-bottom: 1rem;
            border-bottom: 1px dashed #e8d8c0;
        }
        
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: #6b5344;
            font-size: 0.9rem;
        }
        
        @media print {
            body {
                background-color: white;
                padding: 0;
            }
            
            .report-container {
                box-shadow: none;
                border: none;
                padding: 0;
            }
            
            @page {
                margin: 2cm;
            }
        }
    </style>
    """