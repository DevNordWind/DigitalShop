WalletError =
    <b>❌ Ошибка кошелька</b>

    <blockquote>ℹ️ Произошла ошибка при работе с кошельком. Проверьте данные и попробуйте снова.</blockquote>
    .call = ❌ Ошибка кошелька

WalletCurrencyMismatchError =
    <b>❌ Несовпадение валюты кошелька</b>

    <blockquote>ℹ️ Ожидаемая валюта: { $expected }, фактическая валюта: { $actual }.</blockquote>
    .call = ❌ Несовпадение валюты

InsufficientFunds =
    <b>❌ Недостаточно средств на кошельке</b>

    <blockquote>ℹ️ Доступный баланс: <code>{ $available_balance }{ currency.symbol }</code>.</blockquote>
    .call = ❌ Недостаточно средств