class Tagger:
    def tag(text):
        if "http://" in text.lower() or "https://" in text.lower():
            return ["url"]
        else:
            return []