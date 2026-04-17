admin-broadcast = <b>📢 Broadcast</b>

    <blockquote>ℹ️ The message will be sent only to users whose language is included in the broadcast texts</blockquote>
    .preview-btn = 🖼 Preview
    .buttons-btn = Buttons
    .texts-btn = Texts
    .media-btn = { -media-emoji } Media
    .start-btn = ✅ Start

admin-broadcast-preview-select-lang = <b>🖼 Preview</b>

    <blockquote>ℹ️ Select a language for preview</blockquote>
    .show-language-btn = Show in:
    .lang-btn = { lang.emoji } { lang.ins }

admin-broadcast-preview =
    { $text ->
        [None] <blockquote>⚠️ Messages will not be broadcast in this language</blockquote>
        *[other] { $text }
    }

admin-broadcast-buttons = <b>Buttons</b>

    <blockquote>ℹ️ Added buttons will appear in the broadcast message</blockquote>
    .close-button-btn = Close button { $with_close_button ->
        [True] ✅
        *[False] ❌
    }
    .url-buttons-btn = URL buttons

admin-broadcast-buttons-url = <b>URL buttons</b>
    .btn = { $button_text }

admin-broadcast-buttons-url-create = <b>Create URL button</b>

    <blockquote>⚠️ Make sure that button name languages match broadcast text languages.
    <i>The created button will appear above the current message text</i></blockquote>
    .show-language-btn = Show in:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .names-btn = Names
    .url-btn = URL

admin-broadcast-buttons-url-text = <b>✏️ Enter button name</b>

    { -current } Current name: { $name ->
        [None] { unknown.emoji } Not set
        *[other] <code>{ $name }</code>
    }
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-broadcast-buttons-url-url = <b>✏️ Enter button URL</b>

    { -current } Current URL: { $url ->
        [None] { unknown.emoji } Not set
        *[other] { $url }
    }
    .invalid = <b>❌ Invalid URL format</b>

admin-broadcast-texts = <b>✏️ Enter broadcast text</b>

    { -current } Current text: { $text ->
        [None] { unknown.emoji } Not set
        *[other] { $text }
    }

    <blockquote>ℹ️ HTML formatting is supported</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-broadcast-media = <b>{ -media-emoji } Media upload</b>

    <blockquote>ℹ️ Send a photo, video or GIF</blockquote>