admin-position-create-view =  <b> { -position-emoji } Создание позиции</b>

    <b>📜 Основная информация:</b>
    { admin-position-name }
    { admin-position-description }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -position-price-emoji } Цены:</b>{ $prices ->
        [None] { unknown.emoji } Отсутствуют
        *[other] {""}
            { $prices }
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -media-emoji } Медиа:</b> { $has_media ->
        [False] Не добавлено
        *[True] Добавлено
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -category-emoji } Категория:</b> <code>{ $category_name }</code>

    <blockquote>🤔 Всё ли верно?</blockquote>
    .show-language-btn = Показать на:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Название
    .description-btn = Описание
    .media-btn = Медиа
    .price-btn = Цены
    .items-btn = Товары

admin-position-create-name = <b>✏️ Введи название позиции</b>

    { -current } Текущее название: <code>{ $name ->
        [None] { unknown.emoji } Не указано
        *[other] { $name }
    }</code>

    <blockquote>ℹ️ Заполнение имени на <i>{ lang.ins-lower-case }</i> является <b>обязательным</b></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перевести на остальные языки

admin-position-create-description = <b>✏️ Введи описание позиции</b>

    { -current } Текущее описание: { $description ->
        [None] { unknown.emoji } Не указано
        *[other] { $description }
    }

    <blockquote>ℹ️ Заполнение описания на <i>{ lang.ins-lower-case }</i> является <b>обязательным</b>. <i>Поддерживается HTML форматирование</i></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перевести на остальные языки

admin-position-create-price = <b>✏️ Введи цену позиции в <i>{ $currency }</i></b>

    <b>{ -current } Текущие цены:</b> { $prices ->
        [None] Отсутствуют
        *[other] {""}
            { $prices }
    }

    <blockquote>ℹ️ Заполнение цен является <b>обязательным</b> во всех валютах</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .convert-btn = Конвертировать в остальные валюты


admin-position-create-media = <b>{ -media-emoji } Добавление медиа</b>

    <blockquote>ℹ️ Отправь фото, видео или GIF</blockquote>

admin-position-create-warehouse = <b>{ -item-emoji } Хранилище товаров</b>

    { -current } <b>Фиксированное</b> - у позиции только один, неиссякаемый товар

    { -current } <b>Пополняемое</b> - у позиции может быть неограниченное количество товаров, считающихся проданными после покупки

    <blockquote>ℹ️ Добавление товаров станет доступным после создания позиции</blockquote>
    .btn = { $is_current ->
        [True] { -current } { warehouse-type } { -current }
        *[False] { warehouse-type }
    }
