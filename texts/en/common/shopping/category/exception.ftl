CategoryNotFoundError =
    <b>❌ Category not found</b>

    <blockquote>ℹ️ The requested category does not exist or has been deleted.</blockquote>
    .call = ❌ Category not found

CategoryPermissionDeniedError =
    <b>❌ Insufficient permissions</b>

    <blockquote>ℹ️ You do not have permission to view or modify this category.</blockquote>
    .call = ❌ Insufficient permissions

CategoryAlreadyArchivedError =
    <b>❌ Category already archived</b>

    <blockquote>ℹ️ This category is already archived.</blockquote>
    .call = ❌ Already archived

CategoryAlreadyRecoveredError =
    <b>❌ Category is not archived</b>

    <blockquote>ℹ️ This category is already active and does not need to be recovered.</blockquote>
    .call = ❌ Category is not archived

CategoryNameAlreadyTakenError =
    <b>❌ Name already taken</b>

    <blockquote>ℹ️ The category name for language <b>{ $lang }</b> is already in use.</blockquote>
    .call = ❌ Name already taken

CategoryDescriptionEmptyError =
    <b>❌ Description is missing</b>

    <blockquote>ℹ️ The category description has not been provided.</blockquote>
    .call = ❌ Description is missing

CategoryChangingForbiddenError =
    <b>❌ Modification forbidden</b>

    <blockquote>ℹ️ Modifying this category is not allowed.</blockquote>
    .call = ❌ Modification forbidden

CategoryArchivedError =
    <b>❌ Category is archived</b>

    <blockquote>ℹ️ This action cannot be performed because the category is archived.</blockquote>
    .call = ❌ Category is archived

CategoryDeletionForbiddenError =
    <b>❌ Deletion forbidden</b>

    <blockquote>ℹ️ This category cannot be deleted.</blockquote>
    .call = ❌ Deletion forbidden

CategoryDescriptionTooShortError =
    <b>❌ Description is too short</b>

    <blockquote>ℹ️ Minimum description length is { $min_length } characters.</blockquote>
    .call = ❌ Description is too short

CategoryDescriptionTooLongError =
    <b>❌ Description is too long</b>

    <blockquote>ℹ️ Maximum description length is { $max_length } characters.</blockquote>
    .call = ❌ Description is too long

CategoryNameTooShortError =
    <b>❌ Name is too short</b>

    <blockquote>ℹ️ Minimum name length is { $min_length } characters.</blockquote>
    .call = ❌ Name is too short

CategoryNameTooLongError =
    <b>❌ Name is too long</b>

    <blockquote>ℹ️ Maximum name length is { $max_length } characters.</blockquote>
    .call = ❌ Name is too long
