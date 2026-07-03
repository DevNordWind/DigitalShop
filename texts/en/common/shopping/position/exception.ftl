PositionPermissionDeniedError =
    <b>❌ Insufficient permissions</b>

    <blockquote>ℹ️ You do not have permission to perform this action on the position.</blockquote>
    .call = ❌ Insufficient permissions

PositionMediaNotFoundError =
    <b>❌ Media file not found</b>

    <blockquote>ℹ️ The requested position media file was not found.</blockquote>
    .call = ❌ Media file not found

PositionNotFoundError =
    <b>❌ Position not found</b>

    <blockquote>ℹ️ The requested position does not exist or has been deleted.</blockquote>
    .call = ❌ Position not found

PositionAlreadyArchivedError =
    <b>❌ Position already archived</b>

    <blockquote>ℹ️ This position is already archived.</blockquote>
    .call = ❌ Already archived

PositionNotArchivedError =
    <b>❌ Position is not archived</b>

    <blockquote>ℹ️ This action is available only for archived positions.</blockquote>
    .call = ❌ Not archived

PositionDescriptionEmptyError =
    <b>❌ Description is missing</b>

    <blockquote>ℹ️ The position description has not been provided.</blockquote>
    .call = ❌ Description is missing

PositionNameAlreadyTakenError =
    <b>❌ Name already taken</b>

    <blockquote>ℹ️ The position name for language <b>{ $lang }</b> is already in use.</blockquote>
    .call = ❌ Name already taken

PositionMediaLimitReachedError =
    <b>❌ Media file limit reached</b>

    <blockquote>ℹ️ Maximum number of media files: { $limit }.</blockquote>
    .call = ❌ Media file limit reached

PositionChangingForbiddenError =
    <b>❌ Modification forbidden</b>

    <blockquote>ℹ️ Modifying this position is not allowed.</blockquote>
    .call = ❌ Modification forbidden

PositionArchivedError =
    <b>❌ Position is archived</b>

    <blockquote>ℹ️ This action cannot be performed because the position is archived.</blockquote>
    .call = ❌ Position is archived

PositionDeletionForbiddenError =
    <b>❌ Deletion forbidden</b>

    <blockquote>ℹ️ Only archived positions can be deleted.</blockquote>
    .call = ❌ Only archived positions can be deleted

PositionWarehouseFullError =
    <b>❌ Warehouse is full</b>

    <blockquote>ℹ️ Unable to add the item because the warehouse is full.</blockquote>
    .call = ❌ Warehouse is full

OutOfStockError =
    <b>❌ Insufficient stock</b>

    <blockquote>ℹ️ Only { $available } item(s) available.</blockquote>
    .call = ❌ Insufficient stock

PositionItemNotFoundError =
    <b>❌ Item not found</b>

    <blockquote>ℹ️ The requested position item was not found.</blockquote>
    .call = ❌ Item not found

PositionDescriptionTooShortError =
    <b>❌ Description is too short</b>

    <blockquote>ℹ️ Minimum description length is { $min_length } characters.</blockquote>
    .call = ❌ Description is too short

PositionDescriptionTooLongError =
    <b>❌ Description is too long</b>

    <blockquote>ℹ️ Maximum description length is { $max_length } characters.</blockquote>
    .call = ❌ Description is too long

PositionNameTooShortError =
    <b>❌ Name is too short</b>

    <blockquote>ℹ️ Minimum name length is { $min_length } characters.</blockquote>
    .call = ❌ Name is too short

PositionNameTooLongError =
    <b>❌ Name is too long</b>

    <blockquote>ℹ️ Maximum name length is { $max_length } characters.</blockquote>
    .call = ❌ Name is too long

CurrencyMissingError =
    <b>❌ Price missing for one of the currencies</b>

    <blockquote>ℹ️ No price has been set for <b>{ currency }</b>.</blockquote>
    .call = ❌ Price for { currency } is not set
