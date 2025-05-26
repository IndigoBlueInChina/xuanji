"""
玄机一撮 - 解卦服务模块
包含调用LLM API获取卦象解读的函数
"""
import streamlit as st
from openai import OpenAI
import os
# 在导入部分添加新函数
from hexagram_codes import get_hexagram_code, get_hexagram_name, calculate_changed_hexagram, calculate_inverse_hexagram, calculate_mutual_hexagram, get_yicuojin_sentence, analyze_tiyu_wuxing

# Remove the global client initialization
# client = OpenAI(...)

# 配置LLM模型名称
LLM_MODEL = os.getenv("LLM_SERVICE_MODEL", "qwen-plus")

def get_openai_client():
    """Get OpenAI client with lazy initialization"""
    return OpenAI(
        api_key=os.getenv("LLM_SERVICE_API_KEY"),
        base_url=os.getenv("LLM_SERVICE_BASE_URL")
    )

# 在get_interpretation函数中，添加五行生克分析
def get_interpretation(question, background, external_signs, hexagram, changing_lines):
    """调用OpenAI API获取卦象解读"""
    # Initialize client when needed
    client = get_openai_client()
    
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
        
        # 分析本卦的体用五行生克关系
        # tiyu_analysis = analyze_tiyu_wuxing(original_code, changing_line_numbers)
        
        # 分析交互卦的体用五行生克关系
        mutual_tiyu_analysis = analyze_tiyu_wuxing(mutual_code, changing_line_numbers)
        
        # 分析变卦的体用五行生克关系
        changed_tiyu_analysis = analyze_tiyu_wuxing(changed_code, changing_line_numbers)
        
        # 添加到提示中
        if yicuojin_sentence:
            prompt_parts.append(f"一撮金原文：{yicuojin_sentence}")
        if mutual_hexagram:
            prompt_parts.append(f"交互卦：{mutual_hexagram}")
            prompt_parts.append(f"交互卦体用五行：{mutual_tiyu_analysis}")
        if changed_hexagram:
            prompt_parts.append(f"变卦：{changed_hexagram}")
            prompt_parts.append(f"变卦体用五行：{changed_tiyu_analysis}")
        if inverse_hexagram:
            prompt_parts.append(f"综卦：{inverse_hexagram}")
        
        # 添加本卦的体用五行分析
        # prompt_parts.append(f"本卦体用五行：{tiyu_analysis}")
    
    prompt_parts.append("""
请作为精通周易、邵康节一撮金、五行能量属性以及生克体用的专家，从以下五个维度进行系统解读各个卦象所表达的内容，不要添加额外的解释：

1. 本卦：立足当下，直指核心 
   - 现状本质：当前问题的直接表现是什么？本卦的卦名、卦辞、爻辞如何描述现状？ 
   - 关键矛盾：六爻中哪一爻（动爻/静爻）是核心？爻位（初至上）对应的身份、阶段有何启示？ 
   - 能量特性：本卦的上下卦（如天、地、水、火）象征何种力量的互动？如何影响当前状态？
   - 一撮金原文：分析动爻的位置、所附带的评价（如‘上上’、‘下下’等），以及具体的爻辞内容，解读当前卦象对问题的核心指引。

2. 互卦：洞察过程，挖掘动因 
   - 内在逻辑：揭示了哪些隐藏的因果或中间阶段？ 
   - 潜在动力与五行能量：互卦的卦象是否暗示了推动当前局面的深层因素（如冲突、合作、转折）？ 互卦的体用五行能量对应的力量、能量如何影响当前状态？
   - 行动警示：互卦的卦义是否提示了需注意的策略或风险？

3. 变卦：预见未来，调整方向 
   - 趋势结果：变卦与本卦的差异在哪里？未来的主要变化方向是什么？ 
   - 爻变与五行能量启示：若存在动爻，其爻辞如何指导行动？变卦的体用五行能量如何影响未来的发展？
   - 趋吉避凶：如何通过当前行动（本卦）向变卦的结果靠拢？需强化或避免哪些行为？ 

4. 综卦：逆转视角，破除盲区 
   - 对立面观察：综卦的卦义是否与本卦形成互补或对立？ 
   - 反向思考：若从对方立场、相反角度查看问题，是否会有新发现？ 
   - 平衡之道：综卦是否提醒了本卦可能忽略的隐患或过度倾向？

5. 综合联结与实践指导 
   - 发展链条：本卦→互卦→变卦是否构成"现状—过程—结果"的完整逻辑链？ 
   - 对立统一：综卦与本卦如何共同构成事物的两面？如何辩证统一地理解？ 
   - 时间指示：卦象是否暗示特定的时间节点或周期？（如有则说明，无则略过）
   - 结论：从趋利避害的角度，给出明确的结论。
   - 行动建议：基于四卦综合分析，对问题的解决路径提出具体、可操作的建议。

请在解读过程中，引用相关的系辞、卦辞、爻辞、彖辞、象辞和一撮金原文，使解读既有理论依据，又有实践指导意义。
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