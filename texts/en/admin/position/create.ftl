admin-position-create-view = <b>{ -position-emoji } Creating position</b>

    <b>📜 General information:</b>
    { admin-position-name }
    { admin-position-description }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -position-price-emoji } Prices:</b>{ $prices ->
        [None] { unknown.emoji } Not set
        *[other] {""}
            { $prices }
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -media-emoji } Media:</b> { $has_media ->
        [False] Not added
        *[True] Added
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -category-emoji } Category:</b> <code>{ $category_name }</code>

    <blockquote>🤔 Is everything correct?</blockquote>
    .show-language-btn = Show in:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Name
    .description-btn = Description
    .media-btn = Media
    .price-btn = Prices
    .items-btn = Items

admin-position-create-name = <b>✏️ Enter position name</b>

    { -current } Current name: <code>{ $name ->
        [None] { unknown.emoji } Not set
        *[other] { $name }
    }</code>

    <blockquote>ℹ️ Name in <i>{ lang.ins-lower-case }</i> is <b>required</b></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-position-create-description = <b>✏️ Enter position description</b>

    { -current } Current description: { $description ->
        [None] { unknown.emoji } Not set
        *[other] { $description }
    }

    <blockquote>ℹ️ Description in <i>{ lang.ins-lower-case }</i> is <b>required</b>. <i>HTML formatting is supported</i></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Translate to other languages

admin-position-create-price = <b>✏️ Enter position price in <i>{ $currency }</i></b>

    <b>{ -current } Current prices:</b> { $prices ->
        [None] Not set
        *[other] {""}
            { $prices }
    }

    <blockquote>ℹ️ Prices are required in all currencies</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .convert-btn = Convert to other currencies

admin-position-create-media = <b>{ -media-emoji } Adding media</b>

    <blockquote>ℹ️ Send a photo, video or GIF</blockquote>

admin-position-create-warehouse = <b>{ -item-emoji } Warehouse type</b>

    { -current } <b>Fixed</b> - the position has one permanent item

    { -current } <b>Stock</b> - the position can have unlimited items, which are deducted after purchase

    <blockquote>ℹ️ Adding items will become available after creating the position</blockquote>
    .btn = { $is_current ->
        [True] { -current } { warehouse-type } { -current }
        *[False] { warehouse-type }
    }
