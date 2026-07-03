FixedItemNotFoundError =
    <b>❌ Item not found</b>

    <blockquote>ℹ️ The requested fixed item was not found.</blockquote>
    .call = ❌ Item not found

FixedItemContentReplacingForbiddenError =
    <b>❌ Content replacement forbidden</b>

    <blockquote>ℹ️ Archived items cannot be modified.</blockquote>
    .call = ❌ Archived items cannot be modified

FixedItemDeletionForbiddenError =
    <b>❌ Deletion forbidden</b>

    <blockquote>ℹ️ The item must be archived before it can be deleted.</blockquote>
    .call = ❌ Deletion forbidden

FixedItemArchivationForbiddenError = <b>❌ Archiving forbidden</b>
    .call = ❌ Archiving forbidden

FixedItemRecoverForbiddenError = <b>❌ Recovery forbidden</b>
    .call = ❌ Recovery forbidden

ItemContentTooLongError =
    <b>❌ Item content is too long</b>

    <blockquote>ℹ️ Maximum content length is { $max_length } characters.</blockquote>
    .call = ❌ Item content is too long

ItemContentTooShortError =
    <b>❌ Item content is too short</b>

    <blockquote>ℹ️ Minimum content length is { $min_length } characters.</blockquote>
    .call = ❌ Item content is too short

NegativeItemsAmountForbiddenError =
    <b>❌ Invalid quantity</b>

    <blockquote>ℹ️ The item quantity cannot be negative.</blockquote>
    .call = ❌ Invalid quantity

StockItemNotFoundError =
    <b>❌ Item not found</b>

    <blockquote>ℹ️ The requested item was not found.</blockquote>
    .call = ❌ Item not found

StockItemArchivationForbiddenError = { FixedItemArchivationForbiddenError }
    .call = { FixedItemArchivationForbiddenError.call }

StockItemContentReplacingForbiddenError = { FixedItemContentReplacingForbiddenError }
    .call = { FixedItemContentReplacingForbiddenError.call }

StockItemRecoverForbiddenError = { FixedItemRecoverForbiddenError }
    .call = { FixedItemRecoverForbiddenError.call }

StockItemReservationForbiddenError =
    <b>❌ Reservation forbidden</b>

    <blockquote>ℹ️ Reservation is not available at this stage.</blockquote>
    .call = ❌ Reservation is not available at this stage

StockItemSellForbiddenError =
    <b>❌ Sale forbidden</b>

    <blockquote>ℹ️ Selling is not available at this stage.</blockquote>
    .call = ❌ Selling is not available at this stage

StockItemReleaseForbiddenError =
    <b>❌ Reservation release forbidden</b>

    <blockquote>ℹ️ The reservation cannot be released for this stock item at this stage.</blockquote>
    .call = ❌ Reservation release forbidden

StockItemDeletionForbiddenError = { FixedItemDeletionForbiddenError }
    .call = { FixedItemDeletionForbiddenError.call }
