class Tagger:
    def tag(text):
        if "create procedure" in text.lower() or "create database" in text.lower() or "create table" in text.lower():
            return ["sql-query"]
        else:
            return []