class Tagger:
    def tag(text):
        if "<?xml" in text.lower():
            return ["xml"]
        else:
            return []