import pytest

from app.presentation.aiogram.util.mapper.html import validate_html


class TestValidateHtml:
    @pytest.mark.parametrize("value", [pytest.param("<script>", id="unclose tag")])
    def test_raise_on_prohibited_html_tag(self, value: str) -> None:
        with pytest.raises(ValueError):
            validate_html(value=value)

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("<script>alert(1)</script>", id="script"),
            pytest.param("<div>text</div>", id="div"),
            pytest.param("<br>", id="br, void element"),
            pytest.param("<img src='x'>", id="img"),
            pytest.param("<style>body{}</style>", id="style"),
            pytest.param("<iframe src='x'></iframe>", id="iframe"),
            pytest.param(
                "<b><script>x</script></b>", id="forbidden tag nested in allowed"
            ),
        ],
    )
    def test_raises_value_error_on_prohibited_tag(self, value: str) -> None:
        with pytest.raises(ValueError):
            validate_html(value)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            pytest.param("<b>bold</b>", "<b>bold</b>", id="b"),
            pytest.param("<strong>bold</strong>", "<strong>bold</strong>", id="strong"),
            pytest.param("<i>italic</i>", "<i>italic</i>", id="i"),
            pytest.param("<em>italic</em>", "<em>italic</em>", id="em"),
            pytest.param("<u>underline</u>", "<u>underline</u>", id="u"),
            pytest.param("<ins>underline</ins>", "<ins>underline</ins>", id="ins"),
            pytest.param("<s>strike</s>", "<s>strike</s>", id="s"),
            pytest.param(
                "<strike>strike</strike>", "<strike>strike</strike>", id="strike"
            ),
            pytest.param("<del>strike</del>", "<del>strike</del>", id="del"),
            pytest.param(
                "<tg-spoiler>hidden</tg-spoiler>",
                "<tg-spoiler>hidden</tg-spoiler>",
                id="tg-spoiler",
            ),
            pytest.param("<pre>code block</pre>", "<pre>code block</pre>", id="pre"),
            pytest.param(
                "<code>inline</code>", "<code>inline</code>", id="code without class"
            ),
            pytest.param(
                "<blockquote>quote</blockquote>",
                "<blockquote>quote</blockquote>",
                id="blockquote",
            ),
            pytest.param(
                "<b>bold <i>and italic</i></b>",
                "<b>bold <i>and italic</i></b>",
                id="properly nested tags",
            ),
        ],
    )
    def test_allowed_tags_pass_through_unchanged(
        self, value: str, expected: str
    ) -> None:
        assert validate_html(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            pytest.param("<b>bold", "<b>bold</b>", id="single unclosed tag"),
            pytest.param("<b><i>text", "<b><i>text</i></b>", id="nested unclosed tags"),
            pytest.param(
                "<b>bold <i>both</b> italic</i>",
                "<b>bold <i>both</i></b> italic",
                id="overlapping tags closed by stack, trailing italic lost",
            ),
            pytest.param(
                "</b>orphan closing tag",
                "orphan closing tag",
                id="orphan closing tag ignored",
            ),
            pytest.param(
                "<i>ok</i></b>",
                "<i>ok</i>",
                id="orphan closing tag after valid pair",
            ),
        ],
    )
    def test_repairs_malformed_markup(self, value: str, expected: str) -> None:
        assert validate_html(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            pytest.param("<b", "&lt;b", id="truncated open tag without gt"),
            pytest.param("<b ", "&lt;b ", id="truncated open tag with trailing space"),
            pytest.param("<b/", "&lt;b/", id="truncated self-closing-looking tag"),
            pytest.param(
                "text<spoiler", "text&lt;spoiler", id="truncated tag after text"
            ),
        ],
    )
    def test_recovers_truncated_trailing_tag_as_text(
        self, value: str, expected: str
    ) -> None:
        assert validate_html(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            pytest.param("a < b", "a &lt; b", id="raw less-than in text"),
            pytest.param("a > b", "a &gt; b", id="raw greater-than in text"),
            pytest.param("Tom & Jerry", "Tom &amp; Jerry", id="raw ampersand in text"),
            pytest.param(
                "<b>Tom & Jerry</b>",
                "<b>Tom &amp; Jerry</b>",
                id="ampersand inside allowed tag",
            ),
        ],
    )
    def test_escapes_special_characters_in_text(
        self, value: str, expected: str
    ) -> None:
        assert validate_html(value) == expected

    @pytest.mark.parametrize(
        "href",
        [
            pytest.param("https://example.com", id="https"),
            pytest.param("http://example.com", id="http"),
            pytest.param("tg://resolve?domain=durov", id="tg deep link"),
            pytest.param("mailto:user@example.com", id="mailto"),
        ],
    )
    def test_a_tag_allows_supported_schemes(self, href: str) -> None:
        result = validate_html(f'<a href="{href}">link</a>')
        assert result == f'<a href="{href}">link</a>'

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(
                '<a href="javascript:alert(1)">click</a>', id="javascript scheme"
            ),
            pytest.param('<a href="data:text/html,x">click</a>', id="data scheme"),
            pytest.param("<a>no href</a>", id="missing href"),
            pytest.param('<a href="">empty href</a>', id="empty href"),
        ],
    )
    def test_a_tag_rejects_unsupported_or_missing_href(self, value: str) -> None:
        with pytest.raises(ValueError):
            validate_html(value)

    def test_span_with_tg_spoiler_class_is_allowed(self) -> None:
        result = validate_html('<span class="tg-spoiler">hidden</span>')
        assert result == '<span class="tg-spoiler">hidden</span>'

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("<span>no class</span>", id="span without class"),
            pytest.param(
                '<span class="other">wrong class</span>', id="span with wrong class"
            ),
        ],
    )
    def test_span_without_tg_spoiler_class_raises(self, value: str) -> None:
        with pytest.raises(ValueError):
            validate_html(value)

    def test_tg_emoji_with_numeric_id_is_allowed(self) -> None:
        value = '<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>'
        assert validate_html(value) == value

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("<tg-emoji>👍</tg-emoji>", id="missing emoji-id"),
            pytest.param(
                '<tg-emoji emoji-id="not-a-number">👍</tg-emoji>',
                id="non-numeric emoji-id",
            ),
        ],
    )
    def test_tg_emoji_without_valid_id_raises(self, value: str) -> None:
        with pytest.raises(ValueError):
            validate_html(value)

    def test_code_with_valid_language_class_is_kept(self) -> None:
        value = '<pre><code class="language-python">print(1)</code></pre>'
        assert validate_html(value) == value

    def test_code_with_invalid_class_is_dropped_silently(self) -> None:
        result = validate_html('<code class="not-a-language">x</code>')
        assert result == "<code>x</code>"

    def test_blockquote_expandable_is_kept(self) -> None:
        value = "<blockquote expandable>quote</blockquote>"
        assert validate_html(value) == value

    def test_blockquote_other_attributes_are_dropped(self) -> None:
        result = validate_html('<blockquote data-x="1">quote</blockquote>')
        assert result == "<blockquote>quote</blockquote>"

    def test_empty_string_returns_empty_string(self) -> None:
        assert validate_html("") == ""

    def test_plain_text_without_tags_is_only_escaped(self) -> None:
        assert validate_html("just text") == "just text"

    @pytest.mark.parametrize(
        "value",
        [
            "<b>bold</b>",
            "<b>bold",
            "Tom & Jerry",
            '<a href="https://example.com">link</a>',
        ],
    )
    def test_result_is_idempotent(self, value: str) -> None:
        once = validate_html(value)
        twice = validate_html(once)
        assert once == twice
