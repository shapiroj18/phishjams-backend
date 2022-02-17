import re

# to manage apostrophe's, from python's docs: https://docs.python.org/3/library/stdtypes.html#str.title
def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)