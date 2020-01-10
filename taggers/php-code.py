class Tagger:
    def tag(text):
        if "<?php" in text.lower():
            return ["php-code"]
        else:
            return []