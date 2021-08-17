JS_HEADERS_SCRIPT = """
var req = new XMLHttpRequest();
req.open('GET', document.location, false);
req.send(null);
return req.getAllResponseHeaders()
"""

JS_SET_ATTRIBUTE_VALUE = """arguments[0].setAttribute(arguments[1], arguments[2]);"""
JS_CLASS_ACTION_SCRIPT = """arguments[0].classList.{action}(arguments[1]);"""

HIGHLIGHT_CLASS_NAME = "tester-kit-selenium-highlight"
HIGHLIGHT_STYLE = "background: yellow ! important"
HIGHLIGHT_CLASS_DEFINITION = f".{HIGHLIGHT_CLASS_NAME} {{ {HIGHLIGHT_STYLE} }}"
STYLES_INSERT_SCRIPT = f"""
document.getElementsByTagName('head')[0].innerHTML += '<style type="text/css">{HIGHLIGHT_CLASS_DEFINITION}</style>'
"""
