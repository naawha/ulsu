from views import *
import re

urls = (
    (re.compile(r'^/$'), view, False),
    (re.compile(r'^edit$'), edit, False),
    (re.compile(r'^history$'), history, False),
)