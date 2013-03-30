from views import *
import re

urls = (
    (re.compile(r'^/$'), view, False),
    (re.compile(r'^edit$'), edit, 'edit'),
)