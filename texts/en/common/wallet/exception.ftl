WalletPermissionDeniedError =
    <b>❌ Access denied</b>

    <blockquote>ℹ️ You do not have permission to view or manage this wallet</blockquote>
    .call = ❌ Access denied

WalletNotFoundError =
    <b>❌ Wallet not found</b>

    <blockquote>ℹ️ The requested wallet does not exist or has been deleted</blockquote>
    .call = ❌ Wallet not found

InsufficientFundsError =
    <b>❌ Insufficient wallet funds</b>

    <blockquote>ℹ️ Available balance: <code>{ $available_amount }{ currency.symbol }</code>.</blockquote>
    .call = ❌ Insufficient funds. Available: { $available_amount }{ currency.symbol }
