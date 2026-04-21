from collections import Counter

def generate_summary(text):
    if not text:
        return ""
    return ".".join(text.split(".")[:3])

def format_notes(text, summary, keywords):
    formatted = f"""
📄 ORIGINAL TEXT:
{text}

🧠 SUMMARY:
{summary}

🔑 KEYWORDS:
{keywords}
"""
    return formatted

def get_keywords(text):
    words = [w.lower() for w in text.split() if w.isalpha()]
    return [w for w,_ in Counter(words).most_common(5)]