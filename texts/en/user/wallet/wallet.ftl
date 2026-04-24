wallet-row = <b>{ currency }:</b> <code>{ $amount }{ currency.symbol }</code>

wallet-row-selector = { $is_current ->
    [True] { -current } { wallet-row } { -current }
    *[False] { wallet-row }
}

wallet = <b>👝 Wallet</b>

    { $show_all ->
        [True] { $rows }

            <b>Balance:</b> { $amount }{ currency.symbol }
            └ Total: ≈ { $total }{ currency.symbol }
        *[False] <b>Balance:</b> { $amount }{ currency.symbol }
            └ Total: ≈ { $total }{ currency.symbol }
    }
    .show-all-btn = { $show_all ->
        [True] { -current } Show all { -current }
        *[False] Show all
    }
    .top-up-btn = 📥 Top up
    .change-wallet-btn = 👝 Change wallet
    .rates-btn = 💱 Exchange rates

wallet-change-wallet = <b>👝 Change wallet</b>

    <blockquote>ℹ️ Payments for products and top-ups are processed in the currency of your selected wallet</blockquote>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }
