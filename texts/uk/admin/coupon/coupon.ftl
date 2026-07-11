admin-coupons = <b>{ -coupon-emoji } Купони</b>

    <blockquote>⚙️ Обери купон для відкликання або детальної інформації</blockquote>
    .filters = { -filter-emoji } Фільтри
    .btn = { $code } | { $type ->
        [FIXED] Фіксований
        [COEFFICIENT] { $percent }%
        *[other] { unknown }
    }

admin-coupon = <b>🎫 Купон { $code }</b>

    <b>{ -current } Тип:</b> { coupon-type }
    { $type ->
        [COEFFICIENT]└ Відсоток: <code>{ $percent }%</code>
        [FIXED] { $amounts }
        *[other] { unknown }
    }
    { $is_revoked ->
        [True]{""}
            <blockquote>♻️ Купон відкликано</blockquote>
        *[False]
            ➖➖➖➖➖➖➖➖➖➖
            <b>⏳ Діє з:</b> <code>{ DATETIME($valid_from, dateStyle: "medium", timeStyle: "medium")}</code>
            <i> └ Діє до:</i> <code>{ coupon-valid-until }</code>
    }
    .revoke-btn = ♻️ Відкликати

admin-coupons-filters = <b>{ -filter-emoji } Фільтри</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { coupon-status } { -current }
        *[other] { coupon-status }
    }
