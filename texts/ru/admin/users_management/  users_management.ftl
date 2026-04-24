users-management = <b>👥 Пользователи</b>
    .broadcast-btn = 📢 Рассылка
    .find-btn = 🔎 Поиск

users-management-find = <b>🔎 Поиск</b>

    <blockquote>✏️ Введи внутренний идентификатор пользователя, либо его Telegram ID</blockquote>

users-management-wallet-row = { $is_last ->
    [False] ├ <code>{ $amount }{ currency.symbol }</code>
    *[True] └ <code>{ $amount }{ currency.symbol }</code>
}

users-management-user = <b>👤 Пользователь</b>

    🆔 ID: <code>{ $user_id }</code>
    └ Роль: { user-role-lower-case }
    ➖➖➖➖➖➖➖➖➖➖
    <b>👝 Балансы кошельков</b>
    { $wallets_rows }
    ➖➖➖➖➖➖➖➖➖➖
    🛒 Покупок: <code>{ $orders_count }</code>
    📥 Пополнений: <code>{ $top_ups_count }</code>

    <blockquote>🕰 Регистрация: <code>{ $reg_at }</code></blockquote>
    .promote-to-admin-btn = ⭐️ Повысить до админа
    .demote-to-user-btn = 👤 Понизить до пользователя
    .top-up-btn = 📥 Пополнить баланс
    .orders-btn = 🛒 Заказы

users-management-top-up = <b>✏️ Введи сумму пополнения</b>

    <blockquote>ℹ️ Не забудь выбрать валюту для пополнения</blockquote>
    .unselected-currency = <b>❌ Выбери валюту для пополнения</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency}
    }
