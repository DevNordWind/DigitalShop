PaymentNotFoundError =
    <b>❌ Payment not found</b>

    <blockquote>ℹ️ The requested payment was not found.</blockquote>
    .call = ❌ Payment not found

PaymentPermissionDeniedError =
    <b>❌ Insufficient permissions</b>

    <blockquote>ℹ️ You do not have permission to perform this action on the payment.</blockquote>
    .call = ❌ Insufficient permissions

PaymentStartForbiddenError =
    <b>❌ Payment start forbidden</b>

    <blockquote>ℹ️ This payment cannot be started.</blockquote>
    .call = ❌ Payment start forbidden

PaymentCancellationForbiddenError =
    <b>❌ Payment cancellation forbidden</b>

    <blockquote>ℹ️ This payment cannot be cancelled.</blockquote>
    .call = ❌ Cancellation forbidden

PaymentCheckForbiddenError =
    <b>❌ Payment check forbidden</b>

    <blockquote>ℹ️ Checking this payment is not available.</blockquote>
    .call = ❌ Check forbidden

PaymentConfirmationForbiddenError =
    <b>❌ Payment confirmation forbidden</b>

    <blockquote>ℹ️ This payment cannot be confirmed.</blockquote>
    .call = ❌ Confirmation forbidden

PaymentFailureForbiddenError =
    <b>❌ Marking payment as failed is forbidden</b>

    <blockquote>ℹ️ This payment cannot be marked as failed.</blockquote>
    .call = ❌ Mark as failed forbidden

PaymentMethodGatewayError =
    <b>❌ Payment gateway error</b>

    <blockquote>ℹ️ Failed to process the payment method. Please try again later or choose a different payment method.</blockquote>
    .call = ❌ Payment error

UnsupportedPaymentMethodError =
    <b>❌ Payment method not supported</b>

    <blockquote>ℹ️ The selected payment method is not available for this payment gateway.</blockquote>
    .call = ❌ Not supported

CommissionCoefficientRequiredError =
    <b>❌ Commission rate is required</b>

    <blockquote>ℹ️ A commission rate must be specified for this commission type.</blockquote>
    .call = ❌ Commission rate is required
