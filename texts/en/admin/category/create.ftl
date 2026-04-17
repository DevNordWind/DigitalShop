admin-category-create-view =  <b> { -category-emoji } Create category</b>

    <b>📜 Basic information:</b>
    { admin-category-name }
    { admin-category-description }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -media-emoji } Media:</b> { $has_media ->
        [False] Not added
        *[True] Added
    }

    <blockquote>🤔 Is everything correct?</blockquote>
    .show-language-btn = Show in:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Name
    .description-btn = Description
    .media-btn = Media

admin-category-create-name = <b>✏️ Enter category name</b>

    { -current } Current name: <code>{ $name ->
        [None] { unknown.emoji } Not specified
        *[other] { $name }
    }</code>

    <blockquote>ℹ️ Filling the name in <i>{ lang.ins-lower-case }</i> is <b>required</b></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-category-create-description = <b>✏️ Enter category description</b>

    { -current } Current description: { $description ->
        [None] { unknown.emoji } Not specified
        *[other] { $description }
    }

    <blockquote>ℹ️ Filling the description in <i>{ lang.ins-lower-case }</i> is <b>required</b>. <i>HTML formatting is supported</i></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-category-create-media = <b>{ -media-emoji } Adding media</b>

    <blockquote>ℹ️ Send a photo, video or GIF</blockquote>