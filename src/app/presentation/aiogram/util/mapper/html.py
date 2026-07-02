import re
from html import escape
from html.parser import HTMLParser
from typing import NamedTuple, override

_ALLOWED_TAGS = frozenset(
    {
        "b",
        "strong",
        "i",
        "em",
        "u",
        "ins",
        "s",
        "strike",
        "del",
        "span",
        "tg-spoiler",
        "a",
        "tg-emoji",
        "code",
        "pre",
        "blockquote",
    }
)

_HREF_ALLOWED_SCHEMES = frozenset({"http", "https", "tg", "mailto"})
_LANGUAGE_CLASS_RE = re.compile(r"^language-[\w+-]+$")
_EMOJI_ID_RE = re.compile(r"^\d+$")


class _OpenTag(NamedTuple):
    name: str


class _TelegramHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._stack: list[_OpenTag] = []
        self._output: list[str] = []

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in _ALLOWED_TAGS:
            raise ValueError

        rendered_attrs = self._validate_attrs(tag, attrs)
        self._stack.append(_OpenTag(tag))
        self._output.append(f"<{tag}{rendered_attrs}>")

    @override
    def handle_endtag(self, tag: str) -> None:
        if tag not in _ALLOWED_TAGS:
            return

        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i].name == tag:
                for _ in range(len(self._stack) - i):
                    self._output.append(f"</{self._stack.pop().name}>")
                return

    @override
    def handle_data(self, data: str) -> None:
        self._output.append(escape(data, quote=False))

    @override
    def close(self) -> None:
        super().close()
        while self._stack:
            self._output.append(f"</{self._stack.pop().name}>")

    def get_html(self) -> str:
        return "".join(self._output)

    @staticmethod
    def _validate_attrs(tag: str, attrs: list[tuple[str, str | None]]) -> str:  # noqa: PLR0911
        attrs_dict = {name.lower(): (value or "") for name, value in attrs}

        if tag == "a":
            href = attrs_dict.get("href", "")
            scheme = href.split(":", 1)[0].lower() if ":" in href else ""
            if not href or scheme not in _HREF_ALLOWED_SCHEMES:
                raise ValueError
            return f' href="{escape(href, quote=True)}"'

        if tag == "span":
            if attrs_dict.get("class") != "tg-spoiler":
                raise ValueError
            return ' class="tg-spoiler"'

        if tag == "tg-emoji":
            emoji_id = attrs_dict.get("emoji-id", "")
            if not _EMOJI_ID_RE.match(emoji_id):
                raise ValueError
            return f' emoji-id="{escape(emoji_id, quote=True)}"'

        if tag == "code":
            css_class = attrs_dict.get("class", "")
            if css_class and _LANGUAGE_CLASS_RE.match(css_class):
                return f' class="{escape(css_class, quote=True)}"'
            return ""

        if tag == "blockquote":
            return " expandable" if "expandable" in attrs_dict else ""

        return ""


def validate_html(value: str) -> str:
    parser = _TelegramHTMLParser()
    parser.feed(value)
    parser.close()
    return parser.get_html()
