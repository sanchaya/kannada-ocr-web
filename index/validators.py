import re

def validate_pdf(file):
    pattern = '\.pdf$'
    str_file = str(file)
    return re.search(pattern, str_file, flags=re.I)