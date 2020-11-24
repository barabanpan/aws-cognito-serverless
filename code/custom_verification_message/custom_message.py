def handler(event, context):
    if not event["triggerSource"] == "CustomMessage_SignUp":
        return event

    event["request"]["linkParameter"] = event["request"]["linkParameter"].replace("Click Here", "Verify email.")

    email = event["request"]["userAttributes"]["email"]
    email_lines = [
        "<b>Almost done!</b>",
        "",
        "<b>To complete your signup, we just need you</b>",
        "<b>to verify your email address: {0}</b>.".format(email),
        "",
        "<b>{0}</b>".format(event["request"]["linkParameter"]),
        "",
        "<b>Thank you!</b>",
        "",
        "",
        "You’re receiving this email because you recently created a new account.",
        "If this wasn’t you, please ignore this email.",
    ]

    event["response"]["emailSubject"] = "Please verify your email address."
    event["response"]["emailMessage"] = "<br>".join(email_lines)

    return event
