import json

class Tagger:
    def tag(text):
        if text.strip().startswith('{') or text.strip().endswith('}'):
            try:
                json.loads(text.strip())
                return ["json"]
            except:
                pass
        
        return []