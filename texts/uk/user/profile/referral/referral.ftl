referral-default = { -current } Запрошуй рефералів і отримуй <b>{ $percent }%</b> від суми замовлень

referral-time-unit = { $unit ->
    [WEEK] За тиждень
    [MONTH] За місяць
    [TODAY] За сьогодні
    [None] За весь час
    *[other] { unknown }
}

referral = <b>👥 Рефералка</b>

    { $is_referrer ->
        [False] { referral-default }
        *[True]  { referral-default }

        <b>📊 Статистика</b>:
        ├ Запрошено: <code>{ $referral_count }</code>
        ├ Кількість винагород: <code>{ $awards_count }</code>
        └ Зароблено: <code>{ $total_amount }{ currency.symbol }</code>

        <b>🔗 Твоє реферальне посилання:</b> { $link }
    }
    .time-unit-btn = { $is_current ->
        [True] { -current } { referral-time-unit } { -current }
        *[False] { referral-time-unit }
    }
    .get-link-btn = 🔗 Отримати посилання
    .my-awards-btn = 🏆 Мої винагороди
    .change-currency-btn = 💱 Змінити валюту
    .notifications-btn = { $send_notifications ->
        [True] 🔕 Вимкнути сповіщення
        *[False] 🔔 Увімкнути сповіщення
    }

referral-change-currency = <b>{ -wallet-emoji } Вибери валюту, в якій хочеш отримувати винагороду</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }

referral-my-awards = <b>🏆 Мої винагороди</b>
    .btn = { $status ->
        [COMPLETED] { $amount }{ currency.symbol } | { DATETIME($created_at, dateStyle: "short")} { referral-award-status.emoji }
        [PENDING] { DATETIME($created_at, dateStyle: "short")} { referral-award-status.emoji }
        *[other] { unknown }
    }
    .order-btn = { -current } { sorting-order } { -current }

referral-my-award-completed =
    <b>💸 Сума винагороди: <code>{ $amount }{ currency.symbol }</code></b>
    └ Відсоток: <code>{ $percent }%</code>

    <blockquote>{ -time-emoji } Зараховано на баланс { DATETIME($completed_at, dateStyle: "medium", timeStyle: "medium")}</blockquote>

referral-my-award-pending =
    <blockquote>{ -time-emoji } Перебуває в обробці з { DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</blockquote>

referral-my-award = <b>🏆 Винагорода</b>

    { $status ->
        [COMPLETED] { referral-my-award-completed }
        [PENDING] { referral-my-award-pending }
        *[other] { Unknown }
    }
