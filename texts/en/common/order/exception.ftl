OrderNotFoundError =
    <b>❌ Order not found</b>

    <blockquote>ℹ️ The requested order does not exist or has been deleted.</blockquote>
    .call = ❌ Order not found

OrderPermissionDeniedError =
    <b>❌ Insufficient permissions</b>

    <blockquote>ℹ️ You do not have permission to perform this action on the order.</blockquote>
    .call = ❌ Insufficient permissions

OrderCouponApplicationForbiddenError =
    <b>❌ Coupon application forbidden</b>

    <blockquote>ℹ️ A coupon can only be applied to a new order.</blockquote>
    .call = ❌ Coupon unavailable

OrderCancellationForbiddenError =
    <b>❌ Order cancellation forbidden</b>

    <blockquote>ℹ️ The order cannot be cancelled in its current status.</blockquote>
    .call = ❌ Cancellation forbidden

OrderFailureForbiddenError =
    <b>❌ Marking order as failed is forbidden</b>

    <blockquote>ℹ️ The order cannot be marked as failed in its current state.</blockquote>
    .call = ❌ Invalid status change

OrderExpirationForbiddenError =
    <b>❌ Expiration forbidden</b>

    <blockquote>ℹ️ The order cannot expire automatically (expiration is not available in the current state or at the current time).</blockquote>
    .call = ❌ Expiration forbidden

OrderConfirmationForbiddenError =
    <b>❌ Order confirmation forbidden</b>

    <blockquote>ℹ️ The order cannot be confirmed in its current state.</blockquote>
    .call = ❌ Confirmation forbidden

OrderAwaitingPaymentForbiddenError =
    <b>❌ Awaiting payment status forbidden</b>

    <blockquote>ℹ️ The order cannot be moved to the awaiting payment status from its current state.</blockquote>
    .call = ❌ Awaiting payment forbidden

OrderCurrencyChangeForbiddenError =
    <b>❌ Currency change forbidden</b>

    <blockquote>ℹ️ The order currency cannot be changed after the order has been created.</blockquote>
    .call = ❌ Currency unavailable

OrderItemsAmountChangeForbiddenError =
    <b>❌ Item quantity change forbidden</b>

    <blockquote>ℹ️ Item quantities cannot be changed in the current order status.</blockquote>
    .call = ❌ Quantity change forbidden

OrderFreePaymentForbiddenError =
    <b>❌ Free payment unavailable</b>

    <blockquote>ℹ️ This checkout method is not available for free orders.</blockquote>
    .call = ❌ Free payment forbidden

OrderPaymentRequiredError =
    <b>❌ Payment required</b>

    <blockquote>ℹ️ Payment is required to complete the order.</blockquote>
    .call = ❌ Payment required

OrderAppliedCouponRequiredError =
    <b>❌ Coupon required</b>

    <blockquote>ℹ️ A coupon must be applied to use this checkout method.</blockquote>
    .call = ❌ Coupon required
