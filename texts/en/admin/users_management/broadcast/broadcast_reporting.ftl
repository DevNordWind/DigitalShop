broadcast-started = <b>📢 Broadcast started!</b>

    <blockquote>ℹ️ Will send <code>{ $total }</code> messages</blockquote>

broadcast-in-progress = <b>📢 Broadcast in progress...</b>

    <b>{ -current } Sent:</b> <code>{ $current }/{ $total }</code> messages
    ├ Success: { $success }
    ├ Blocked: { $not_active }
    └ Errors: { $error }

broadcast-ended = <b>📢 Broadcast completed!</b>

    <b>{ -current } Total sent:</b> <code>{ $total }</code>
    ├ Success: { $success }
    ├ Blocked: { $not_active }
    └ Errors: { $error }