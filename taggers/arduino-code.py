class Tagger:
    def tag(text):
        if "pinmode" in text.lower() or "digitalwrite" in text.lower() or "digitalread" in text.lower():
            return ["bash-script"]
        else:
            return []