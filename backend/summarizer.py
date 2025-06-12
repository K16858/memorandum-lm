def summarize_text(llm, target_text):
    summarize_template = f"""
    以下のテキストを簡潔に要約してください。元のテキストの重要なポイントを含めて、最大3段落でまとめてください。
    テキスト:
    {target_text}
    要約:
    """
    result = llm(summarize_template, max_tokens=1000, stop=["\n\n"])
    
    return result["choices"][0]["text"].strip()
    