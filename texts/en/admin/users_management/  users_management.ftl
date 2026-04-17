users-management = <b>👥 Users</b>
    .broadcast-btn = 📢 Broadcast
    .find-btn = 🔎 Search

users-management-find = <b>🔎 Search</b>

    <blockquote>✏️ Enter the internal user ID or their Telegram ID</blockquote>

users-management-wallet-row = { $is_last ->
    [False] ├ <code>{ $amount }{ currency.symbol }</code>
    *[True] └ <code>{ $amount }{ currency.symbol }</code>
}

users-management-user = <b>👤 User</b>

    🆔 ID: <code>{ $user_id }</code>
    └ Role: { user-role-lower-case }
    ➖➖➖➖➖➖➖➖➖➖
    <b>👝 Wallet balances</b>
    { $wallets_rows }
    ➖➖➖➖➖➖➖➖➖➖
    🛒 Purchases: <code>{ $orders_count }</code>
    📥 Top-ups: <code>{ $top_ups_count }</code>

    <blockquote>🕰 Registration: <code>{ $reg_at }</code></blockquote>
    .promote-to-admin-btn = ⭐️ Promote to admin
    .demote-to-user-btn = 👤 Demote to user
    .top-up-btn = 📥 Top up balance
    .orders-btn = 🛒 Orders

users-management-top-up = <b>✏️ Enter top-up amount</b>

    <blockquote>ℹ️ Don’t forget to select a currency for the top-up</blockquote>
    .unselected-currency = <b>❌ Select a currency for top-up</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }