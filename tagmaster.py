import os
import importlib

# The list of taggers
taggers = []

def collect_taggers(dir):
    files = os.listdir(dir)

    for file in files:
        if file.endswith(".py"):
            module = importlib.import_module(dir + '.' + file[:-3])
            tagger = my_class = getattr(module, 'Tagger')
            taggers.append(tagger)

def run_taggers(text):
    tags = []

    for tagger in taggers:
        for tag in tagger.tag(text):
            tags.append(tag)

    return tags

