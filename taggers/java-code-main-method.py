class Tagger:
    def tag(text):
        if "public static void main" in text.lower():
            return ["java-code-main-method"]
        else:
            return []