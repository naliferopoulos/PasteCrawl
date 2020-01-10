class Tagger:
    def tag(text):
        if "<html" in text.lower() or "<head" in text.lower() or "<body" in text.lower() or "<script" in text.lower():
            return ["html"]
        else:
            return []