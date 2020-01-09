class Tagger:
    def tag(text):
        if "begin ssh" in text.lower() or "end ssh" in text.lower():
            return ["ssh-key"]
        else:
            return []