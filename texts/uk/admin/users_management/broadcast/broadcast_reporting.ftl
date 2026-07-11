broadcast-started = <b>📢 Розсилку розпочато!</b>

    <blockquote>ℹ️ Буде надіслано <code>{ $total }</code> повідомлень</blockquote>

broadcast-in-progress = <b>📢 Розсилка триває...</b>

    <b>{ -current } Надіслано:</b> <code>{ $current }/{ $total }</code> повідомлень
    ├ Успішно: { $success }
    ├ Заблокували: { $not_active }
    └ З помилкою: { $error }

broadcast-ended = <b>📢 Розсилку завершено!</b>

    <b>{ -current } Всього надіслано:</b> <code>{ $total }</code>
    ├ Успішно: { $success }
    ├ Заблокували: { $not_active }
    └ З помилкою: { $error }
