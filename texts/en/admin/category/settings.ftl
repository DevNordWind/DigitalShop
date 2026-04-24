admin-category-settings = <b>⚙️ Settings️</b>

    .default-lang-btn = { -langs-emoji } Default language
    .show-with-no-items-btn = { -item-emoji } Categories without items
    .show-with-no-items-switcher-btn = { $show_with_no_items ->
        [True] { inl-ui.hide }
        *[False] { inl-ui.show }
    }

admin-category-default-lang = <b>{ -langs-emoji } Default language</b>

    <blockquote>ℹ️ <b>Default language</b> becomes <b>required</b> when creating new categories. <b>Auto-translation</b> to other languages is based on it</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
