class Tagger:
    def tag(text):
        if "#!/bin/bash" in text.lower() or "-eq" in text.lower() or "#! /bin/bash" in text.lower():
            return ["bash-script"]
        else:
            return []