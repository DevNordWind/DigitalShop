admin-category-edit-name = <b>✏️ Enter new category name</b>

    { -current } Current name: <code>{ $name ->
        [None] Not specified in this language
        *[other] { $name }
    }</code>
    .default-lang-btn = { -langs-emoji } Default language
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-category-edit-name-default-lang = <b>{ -langs-emoji } Default language</b>

    <blockquote>⚠️ Before changing the default language, make sure it is filled</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-category-edit-description = <b>✏️ Enter new category description</b>

    { -current } Current description: { $has_description ->
        [True] { $description ->
            [None] Not specified in this language
            *[other] { $description }
        }
        *[False] { unknown.emoji } Missing.

            <blockquote>⚠️ Selected language will become the default language</blockquote>
    }

    .default-lang-btn = { -langs-emoji } Default language
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-category-edit-description-default-lang = <b>{ -langs-emoji } Default language</b>

    <blockquote>⚠️ Before changing the default language, make sure it is filled</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-category-edit-media = <b>{ -media-emoji } Edit media</b>

    <blockquote>ℹ️ Send photo, video or GIF</blockquote>
