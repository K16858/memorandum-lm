def extract_keypoints(llm, target_text, n_points=3):
    template = f"""
    テキスト:
    {target_text}
    
    このテキストを簡潔から重要なポイントを{n_points}個抽出してください。各ポイントは箇条書きかつ一文で簡潔に記述してください。
    ただし、以下のような形式で出力してください:
    - ポイント1
    - ポイント2
    - ポイント3
    
    重要なポイント:
    """
    result = llm(template, max_tokens=1000, stop=["\n\n"])
    keypoints = result["choices"][0]["text"].strip().split("\n")
    return [point.strip() for point in keypoints if point.strip().startswith("-")]

def extract_keywords(llm, target_text, n_keywords=5):
    template = f"""
    テキスト:
    {target_text}
    
    このテキストから重要なキーワードを{n_keywords}個抽出してください。各キーワードは以下のようにカンマで区切ってください。
    キーワード1, キーワード2, キーワード3, キーワード4, キーワード5
    ただし、キーワードは短く、テキストの内容を反映したものにしてください。
    
    キーワード:
    """
    result = llm(template, max_tokens=50*n_keywords, stop=["\n\n"])
    keywords = result["choices"][0]["text"].strip().split(",")
    return [keyword.strip() for keyword in keywords if keyword.strip() != ""]

