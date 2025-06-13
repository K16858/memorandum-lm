def summarize_text(llm, target_text, n_paragraphs=3):
    template = f"""
    テキスト:
    {target_text}
    
    このテキストを簡潔に要約してください。元のテキストの重要なポイントを含めて、{n_paragraphs}段落でまとめてください。
    ただし、各段落は短く、要点を押さえた形で記述し、段落の最後には改行を入れてください。
    要約:
    """
    result = llm(template, max_tokens=1000, stop=["\n\n"])
    
    return result["choices"][0]["text"].strip()
