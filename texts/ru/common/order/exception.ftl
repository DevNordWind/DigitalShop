OrderNotFoundError =
    <b>❌ Заказ не найден</b>

    <blockquote>ℹ️ Запрашиваемый заказ не существует или был удалён.</blockquote>
    .call = ❌ Заказ не найден

OrderPermissionDeniedError =
    <b>❌ Недостаточно прав</b>

    <blockquote>ℹ️ У вас нет прав для выполнения этого действия с заказом.</blockquote>
    .call = ❌ Недостаточно прав

OrderCouponApplicationForbiddenError =
    <b>❌ Применение купона запрещено</b>

    <blockquote>ℹ️ Купон можно применить только к новому заказу.</blockquote>
    .call = ❌ Купон недоступен

OrderCancellationForbiddenError =
    <b>❌ Отмена заказа запрещена</b>

    <blockquote>ℹ️ Заказ нельзя отменить в текущем статусе.</blockquote>
    .call = ❌ Отмена запрещена

OrderFailureForbiddenError =
    <b>❌ Перевод в статус «ошибка» запрещён</b>

    <blockquote>ℹ️ Заказ нельзя пометить как неуспешный в текущем состоянии.</blockquote>
    .call = ❌ Ошибка статуса

OrderExpirationForbiddenError =
    <b>❌ Истечение срока запрещено</b>

    <blockquote>ℹ️ Заказ нельзя автоматически завершить (истечение срока недоступно в текущем состоянии или времени).</blockquote>
    .call = ❌ Истечение срока запрещено

OrderConfirmationForbiddenError =
    <b>❌ Подтверждение заказа запрещено</b>

    <blockquote>ℹ️ Заказ нельзя подтвердить в текущем состоянии.</blockquote>
    .call = ❌ Подтверждение запрещено

OrderAwaitingPaymentForbiddenError =
    <b>❌ Ожидание оплаты запрещено</b>

    <blockquote>ℹ️ Заказ нельзя перевести в статус ожидания оплаты из текущего состояния.</blockquote>
    .call = ❌ Ожидание оплаты запрещено

OrderCurrencyChangeForbiddenError =
    <b>❌ Изменение валюты запрещено</b>

    <blockquote>ℹ️ Валюту заказа нельзя изменить после создания заказа.</blockquote>
    .call = ❌ Валюта недоступна

OrderItemsAmountChangeForbiddenError =
    <b>❌ Изменение количества товаров запрещено</b>

    <blockquote>ℹ️ Нельзя изменить количество товаров в текущем статусе заказа.</blockquote>
    .call = ❌ Изменение количества запрещено

OrderFreePaymentForbiddenError =
    <b>❌ Бесплатная оплата невозможна</b>

    <blockquote>ℹ️ Этот способ оформления недоступен для бесплатного заказа.</blockquote>
    .call = ❌ Бесплатная оплата запрещена

OrderPaymentRequiredError =
    <b>❌ Требуется оплата</b>

    <blockquote>ℹ️ Для завершения заказа необходимо оплатить его.</blockquote>
    .call = ❌ Требуется оплата

OrderAppliedCouponRequiredError =
    <b>❌ Требуется купон</b>

    <blockquote>ℹ️ Для этого способа оформления необходимо применить купон.</blockquote>
    .call = ❌ Требуется купон
