PositionPermissionDeniedError =
    <b>❌ Insufficient Permissions</b>

    <blockquote>ℹ️ You do not have permission to perform this action on this position.</blockquote>
    .call = ❌ Insufficient Permissions

PositionMediaNotFoundError =
    <b>❌ Media File Not Found</b>

    <blockquote>ℹ️ The requested position media file was not found.</blockquote>
    .call = ❌ Media File Not Found

PositionNotFoundError =
    <b>❌ Position Not Found</b>

    <blockquote>ℹ️ The requested position does not exist or has been deleted.</blockquote>
    .call = ❌ Position Not Found

PositionAlreadyArchivedError =
    <b>❌ Position Already Archived</b>

    <blockquote>ℹ️ The position is already in the archive.</blockquote>
    .call = ❌ Already Archived

PositionNotArchivedError =
    <b>❌ Position Not Archived</b>

    <blockquote>ℹ️ This action is only available for archived positions.</blockquote>
    .call = ❌ Not Archived

PositionDescriptionEmptyError =
    <b>❌ Description Missing</b>

    <blockquote>ℹ️ The position description is not filled in.</blockquote>
    .call = ❌ Description Missing

PositionNameAlreadyTakenError =
    <b>❌ Name Already Taken</b>

    <blockquote>ℹ️ The position name for language <b>{ $lang }</b> is already in use.</blockquote>
    .call = ❌ Name Taken

PositionMediaLimitReachedError =
    <b>❌ Media Limit Reached</b>

    <blockquote>ℹ️ Maximum number of media files: { $limit }.</blockquote>
    .call = ❌ Media Limit Reached

PositionChangingForbiddenError =
    <b>❌ Modification Forbidden</b>

    <blockquote>ℹ️ Modifying this position is forbidden.</blockquote>
    .call = ❌ Modification Forbidden

PositionArchivedError =
    <b>❌ Position Archived</b>

    <blockquote>ℹ️ Action cannot be performed because the position is in the archive.</blockquote>
    .call = ❌ Position Archived

PositionDeletionForbiddenError =
    <b>❌ Deletion Forbidden</b>

    <blockquote>ℹ️ Only archived positions can be deleted.</blockquote>
    .call = ❌ Only archived positions can be deleted.

PositionWarehouseFullError =
    <b>❌ Warehouse Full</b>

    <blockquote>ℹ️ Cannot add items because the warehouse is full.</blockquote>
    .call = ❌ Warehouse Full

PositionItemNotFoundError =
    <b>❌ Item Not Found</b>

    <blockquote>ℹ️ The requested position item was not found.</blockquote>
    .call = ❌ Item Not Found

PositionDescriptionTooShortError =
    <b>❌ Description Too Short</b>

    <blockquote>ℹ️ Minimum description length is { $min_length } characters.</blockquote>
    .call = ❌ Description Too Short

PositionDescriptionTooLongError =
    <b>❌ Description Too Long</b>

    <blockquote>ℹ️ Maximum description length is { $max_length } characters.</blockquote>
    .call = ❌ Description Too Long

PositionNameTooShortError =
    <b>❌ Name Too Short</b>

    <blockquote>ℹ️ Minimum name length is { $min_length } characters.</blockquote>
    .call = ❌ Name Too Short

PositionNameTooLongError =
    <b>❌ Name Too Long</b>

    <blockquote>ℹ️ Maximum name length is { $max_length } characters.</blockquote>
    .call = ❌ Name Too Long

CurrencyMissingError =
    <b>❌ Price Missing for One of the Currencies</b>

    <blockquote>ℹ️ No price set for currency <b>{ currency }</b>.</blockquote>
    .call = ❌ Price for { currency } is not set

OutOfStockError =
    <b>❌ Insufficient Stock</b>

    <blockquote>ℹ️ Only { $available } pcs. available.</blockquote>
    .call = ❌ Insufficient Stock
