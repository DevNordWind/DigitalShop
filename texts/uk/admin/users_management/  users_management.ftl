users-management = <b>👥 Користувачі</b>
    .broadcast-btn = 📢 Розсилка
    .find-btn = 🔎 Пошук

users-management-find = <b>🔎 Пошук</b>

    <blockquote>✏️ Введи внутрішній ідентифікатор користувача або його Telegram ID</blockquote>

users-management-wallet-row = { $is_last ->
    [False] ├ <code>{ $amount }{ currency.symbol }</code>
    *[True] └ <code>{ $amount }{ currency.symbol }</code>
}

users-management-user = <b>👤 Користувач</b>

    🆔 ID: <code>{ $user_id }</code>
    └ Роль: { user-role-lower-case }
    ➖➖➖➖➖➖➖➖➖➖
    <b>👝 Баланси гаманців</b>
    { $wallets_rows }
    ➖➖➖➖➖➖➖➖➖➖
    🛒 Покупок: <code>{ $orders_count }</code>
    📥 Поповнень: <code>{ $top_ups_count }</code>

    <blockquote>🕰 Реєстрація: <code>{ $reg_at }</code></blockquote>
    .promote-to-admin-btn = ⭐️ Підвищити до адміна
    .demote-to-user-btn = 👤 Понизити до користувача
    .top-up-btn = 📥 Поповнити баланс
    .orders-btn = 🛒 Замовлення

users-management-top-up = <b>✏️ Введи суму поповнення</b>

    <blockquote>ℹ️ Не забудь вибрати валюту для поповнення</blockquote>
    .unselected-currency = <b>❌ Вибери валюту для поповнення</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency}
    }
