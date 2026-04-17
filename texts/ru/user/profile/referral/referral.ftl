referral-default = { -current } Приглашай рефералов и получай <b>{ $percent }%</b> от суммы заказов

referral-time-unit = { $unit ->
    [WEEK] За неделю
    [MONTH] За месяц
    [TODAY] За сегодня
    [None] За всё время
    *[other] { unknown }
}

referral = <b>👥 Рефералка</b>

    { $is_referrer ->
        [False] { referral-default }
        *[True]  { referral-default }

        <b>📊 Статистика</b>:
        ├ Приглашено: <code>{ $referral_count }</code>
        ├ Кол-во вознаграждений: <code>{ $awards_count }</code>
        └ Заработано: <code>{ $total_amount }{ currency.symbol }</code>

        <b>🔗 Твоя реферальная ссылка:</b> { $link }
    }
    .time-unit-btn = { $is_current ->
        [True] { -current } { referral-time-unit } { -current }
        *[False] { referral-time-unit }
    }
    .get-link-btn = 🔗 Получить ссылку
    .my-awards-btn = 🏆 Мои вознаграждения
    .change-currency-btn = 💱 Сменить валюту
    .notifications-btn = { $send_notifications ->
        [True] 🔕 Выключить уведомления
        *[False] 🔔 Включить уведомления
    }

referral-change-currency = <b>{ -wallet-emoji } Выбери валюту, в которой хочешь получать вознаграждение</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }

referral-my-awards = <b>🏆 Мои вознаграждения</b>
    .btn = { $status ->
        [COMPLETED] { $amount }{ currency.symbol } | { DATETIME($created_at, dateStyle: "short")} { referral-award-status.emoji }
        [PENDING] { DATETIME($created_at, dateStyle: "short")} { referral-award-status.emoji }
        *[other] { unknown }
    }
    .order-btn = { -current } { sorting-order } { -current }

referral-my-award-completed =
    <b>💸 Сумма вознаграждения: <code>{ $amount }{ currency.symbol }</code></b>
    └ Процент: <code>{ $percent }%</code>

    <blockquote>{ -time-emoji } Зачислено на баланс { DATETIME($completed_at, dateStyle: "medium", timeStyle: "medium")}</blockquote>

referral-my-award-pending =
    <blockquote>{ -time-emoji } Находится в обработке с { DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</blockquote>

referral-my-award = <b>🏆 Вознаграждение</b>

    { $status ->
        [COMPLETED] { referral-my-award-completed }
        [PENDING] { referral-my-award-pending }
        *[other] { Unknown }
    }
