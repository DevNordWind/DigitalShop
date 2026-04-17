wallet-row = <b>{ currency }:</b> <code>{ $amount }{ currency.symbol }</code>

wallet-row-selector = { $is_current ->
    [True] { -current } { wallet-row } { -current }
    *[False] { wallet-row }
}

wallet = <b>👝 Кошелёк</b>

    { $show_all ->
        [True] { $rows }

            <b>Баланс:</b> { $amount }{ currency.symbol }
            └ Всего: ≈ { $total }{ currency.symbol }
        *[False] <b>Баланс:</b> { $amount }{ currency.symbol }
            └ Всего: ≈ { $total }{ currency.symbol }
    }
    .show-all-btn = { $show_all ->
        [True] { -current } Показать всё { -current }
        *[False] Показать всё
    }
    .top-up-btn = 📥 Пополнить
    .change-wallet-btn = 👝 Сменить кошелёк
    .rates-btn = 💱 Курсы валют

wallet-change-wallet = <b>👝 Смена кошелька</b>

    <blockquote>ℹ️ Оплата товаров и пополнение осуществляются в валюте выбранного вами кошелька</blockquote>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }




