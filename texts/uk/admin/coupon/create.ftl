admin-coupon-create-view = <b>{ -coupon-emoji } Создание купона</b>

    <b>{ -current } Код:</b> <code>{ $code ->
        [None] { unknown.emoji } Не указан
        *[other] { $code }
    }</code>
    <b>{ -current } Тип:</b> { $type ->
            [None] { unknown.emoji } Не указан
            *[other] { coupon-type } { $type ->
                [COEFFICIENT] {""}
                    └ Процент: <code>{ $percent }%</code>
                [FIXED] {""}
                    { $amounts }
                *[other] { unknown }
            }
        }
    ➖➖➖➖➖➖➖➖➖➖
    <b>⏳ Действует с:</b> { $valid_from ->
        [None] создания
        *[other] <code>{ DATETIME($valid_from, dateStyle: "medium", timeStyle: "medium")}</code>
    }
    <i> └ Действует до:</i> <code>{ coupon-valid-until }</code>

    <blockquote>🤔 Всё ли верно?</blockquote>
    .code-btn = Код
    .valid-from-btn = { -time-emoji } Действует с
    .valid-until-btn = { -time-emoji } Действует до
    .type-btn = Тип

admin-coupon-create-code = <b>✏️ Введи код активации купона</b>

    <b>{ -current } Текущий код:</b> { $code ->
        [None] { unknown.emoji } Не указан
        *[other] { $code }
    }

    <blockquote>ℹ️ Например: «СКИДКА»</blockquote>

admin-coupon-create-type =
    { $type ->
        [None] <b>Выбери тип промокода</b>
        *[other] <b>Выбери тип промокода</b>

            <b>{ -current } Текущий тип:</b> { coupon-type }
            { $type ->
                [COEFFICIENT]  └ Процент: <code>{ $percent }%</code>
                [FIXED]  { $amounts }
                *[other] { unknown }
            }
    }
    .btn = { coupon-type }

admin-coupon-create-coefficient = <b>✏️ Введи размер скидки в процентах</b>

admin-coupon-create-fixed = <b>✏️ Введи сумму скидки</b>

    <b>{ -current } Текущие суммы:</b> { $amounts ->
        [None] Отсутствуют
        *[other] {""}
            { $amounts }
    }
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .convert-btn = Конвертировать в остальные валюты

admin-coupon-create-invalid-date = <b>❌ Неверный формат даты</b>

admin-coupon-create-valid-from = <b>✏️ Введи когда начнёт действовать купон</b>

    <blockquote>ℹ️ Формат даты: <code>ДД.ММ.ГГ ЧЧ:ММ</code></blockquote>

admin-coupon-create-valid-until = <b>✏️ Введи когда купон закончит действовать</b>

    <blockquote>ℹ️ Формат даты: <code>ДД.ММ.ГГ ЧЧ:ММ</code></blockquote>
