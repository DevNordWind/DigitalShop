broadcast-started = <b>📢 Рассылка запущена!</b>

    <blockquote>ℹ️ Будет отправлено <code>{ $total }</code> сообщений</blockquote>

broadcast-in-progress = <b>📢 Рассылка в процессе...</b>

    <b>{ -current } Отправлено:</b> <code>{ $current }/{ $total }</code> сообщений
    ├ Успешно: { $success }
    ├ Заблокировали: { $not_active }
    └ С ошибкой: { $error }

broadcast-ended = <b>📢 Рассылка завершена!</b>

    <b>{ -current } Всего отправлено:</b> <code>{ $total }</code>
    ├ Успешно: { $success }
    ├ Заблокировали: { $not_active }
    └ С ошибкой: { $error }
