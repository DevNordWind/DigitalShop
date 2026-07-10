admin-broadcast = <b>📢 Розсилка</b>

    <blockquote>ℹ️ Повідомлення отримають лише ті користувачі, чия мова є в текстах розсилки</blockquote>
    .preview-btn = 🖼 Попередній перегляд
    .buttons-btn = Кнопки
    .texts-btn = Тексти
    .media-btn = { -media-emoji } Медіа
    .start-btn = ✅ Розпочати

admin-broadcast-preview-select-lang = <b>🖼 Попередній перегляд</b>

    <blockquote>ℹ️ Вибери мову для попереднього перегляду</blockquote>
    .show-language-btn = Показати на:
    .lang-btn = { lang.emoji } { lang.ins }

admin-broadcast-preview =
    { $text ->
        [None] <blockquote>⚠️ Повідомлення не будуть надіслані цією мовою</blockquote>
        *[other] { $text }
    }

admin-broadcast-buttons = <b>Кнопки</b>

    <blockquote>ℹ️ Додані кнопки будуть у повідомленні розсилки</blockquote>
    .close-button-btn = Кнопка закриття { $with_close_button ->
        [True] ✅
        *[False] ❌
    }
    .url-buttons-btn = URL-кнопки

admin-broadcast-buttons-url = <b>URL-кнопки</b>
    .btn = { $button_text }

admin-broadcast-buttons-url-create = <b>Створення URL-кнопки</b>

    <blockquote>⚠️ Переконайся, що мови назв кнопки збігаються з мовами текстів розсилки.
    <i>Створена кнопка буде відображатися зверху під текстом поточного повідомлення</i></blockquote>
    .show-language-btn = Показати на:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .names-btn = Назви
    .url-btn = URL

admin-broadcast-buttons-url-text = <b>✏️ Введи назву кнопки</b>

    { -current } Поточна назва: { $name ->
        [None] { unknown.emoji } Не вказано
        *[other] <code>{ $name }</code>
    }
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-broadcast-buttons-url-url = <b>✏️ Введи URL кнопки</b>

    { -current } Поточний URL: { $url ->
        [None] { unknown.emoji } Не вказано
        *[other] { $url }
    }
    .invalid = <b>❌ Невірний формат URL</b>

admin-broadcast-texts = <b>✏️ Введи текст розсилки</b>

    { -current } Поточний текст: { $text ->
        [None] { unknown.emoji } Не вказано
        *[other] { $text }
    }

    <blockquote>ℹ️ Підтримується HTML форматування</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-broadcast-media = <b>{ -media-emoji } Додавання медіа</b>

    <blockquote>ℹ️ Надішли фото, відео або GIF</blockquote>
