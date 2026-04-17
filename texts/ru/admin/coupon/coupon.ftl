admin-coupons = <b>{ -coupon-emoji } Купоны</b>

    <blockquote>⚙️ Выбери купон для отзыва или детальной информации</blockquote>
    .filters = { -filter-emoji } Фильтры
    .btn = { $code } | { $type ->
        [FIXED] Фиксированный
        [COEFFICIENT] { $percent }%
        *[other] { unknown }
    }

admin-coupon = <b>🎫 Купон { $code }</b>

    <b>{ -current } Тип:</b> { coupon-type }
    { $type ->
        [COEFFICIENT]└ Процент: <code>{ $percent }%</code>
        [FIXED] { $amounts }
        *[other] { unknown }
    }
    { $is_revoked ->
        [True]{""}
            <blockquote>♻️ Купон отозван</blockquote>
        *[False]
            ➖➖➖➖➖➖➖➖➖➖
            <b>⏳ Действует с:</b> <code>{ DATETIME($valid_from, dateStyle: "medium", timeStyle: "medium")}</code>
            <i> └ Действует до:</i> <code>{ coupon-valid-until }</code>
    }
    .revoke-btn = ♻️ Отозвать


admin-coupons-filters = <b>{ -filter-emoji } Фильтры</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { coupon-status } { -current }
        *[other] { coupon-status }
    }
