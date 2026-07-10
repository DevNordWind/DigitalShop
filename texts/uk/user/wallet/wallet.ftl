wallet-row = <b>{ currency }:</b> <code>{ $amount }{ currency.symbol }</code>

wallet-row-selector = { $is_current ->
    [True] { -current } { wallet-row } { -current }
    *[False] { wallet-row }
}

wallet = <b>👝 Гаманець</b>

    { $show_all ->
        [True] { $rows }

            <b>Баланс:</b> { $amount }{ currency.symbol }
            └ Всього: ≈ { $total }{ currency.symbol }
        *[False] <b>Баланс:</b> { $amount }{ currency.symbol }
            └ Всього: ≈ { $total }{ currency.symbol }
    }
    .show-all-btn = { $show_all ->
        [True] { -current } Показати все { -current }
        *[False] Показати все
    }
    .top-up-btn = 📥 Поповнити
    .change-wallet-btn = 👝 Змінити гаманець
    .rates-btn = 💱 Курси валют

wallet-change-wallet = <b>👝 Зміна гаманця</b>

    <blockquote>ℹ️ Оплата товарів і поповнення здійснюються у валюті вибраного вами гаманця</blockquote>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }
