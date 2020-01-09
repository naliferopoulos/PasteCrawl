class Tagger:
    def tag(text):
        if "int main(" in text.lower():
            return ["c-cpp-code-main-function"]
        else:
            return []