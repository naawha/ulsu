from views import *
import re

urls = (
    (re.compile(r'^/$'), view),
    (re.compile(r'^edit$'), edit),
)