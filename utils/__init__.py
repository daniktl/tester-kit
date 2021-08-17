import re


CONTENT_TYPE_REGEX = re.compile(r"content-type:\s(.*)\n")


class ContentType:
    UNDEFINED = "undefined"
    JSON = "json"
    XML = "xml"
    HTML = "html"


def check_response_content_type(response_headers: str) -> str:
    content_type_search = CONTENT_TYPE_REGEX.search(response_headers)
    if not content_type_search:
        return ContentType.UNDEFINED
    content_type: str = content_type_search.group(0)
    if "text/html" in content_type:
        return ContentType.HTML
    elif "xml" in content_type:
        return ContentType.XML
    elif "json" in content_type:
        return ContentType.JSON
