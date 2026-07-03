WalletPermissionDeniedError =
    <b>❌ Доступ запрещён</b>

    <blockquote>ℹ️ Вы не можете просматривать или управлять этим кошельком</blockquote>
    .call = ❌ Доступ запрещён

WalletNotFoundError =
    <b>❌ Кошелёк не найден</b>

    <blockquote>ℹ️ Запрашиваемый кошелёк не существует или был удален</blockquote>
    .call = ❌ Кошелёк не найден

InsufficientFundsError =
    <b>❌ Недостаточно средств на кошельке</b>

    <blockquote>ℹ️ Доступный баланс: <code>{ $available_amount }{ currency.symbol }</code>.</blockquote>
    .call = ❌ Недостаточно средств. Доступно: { $available_amount }{ currency.symbol }
