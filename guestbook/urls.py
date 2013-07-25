from views import *
import re

urls = (
    (re.compile(r'^/$'), view, False),
    (re.compile(r'^add_message$'), add_message, False),
    (re.compile(r'^add_message/save$'), save_message, False),
    (re.compile(r'^delete$'), delete_message, False),
)