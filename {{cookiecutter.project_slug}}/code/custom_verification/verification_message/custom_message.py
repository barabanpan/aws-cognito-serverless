import urllib
import os


def handler(event, context):
    if not event["triggerSource"] in ["CustomMessage_SignUp", "CustomMessage_ResendCode"]:
        return event

    email = event["request"]["userAttributes"]["email"]
    code = event["request"]["codeParameter"]

    my_url = os.environ.get("URL_TO_LAMBDA_FOR_REDIRECT")

    link = '<a href="{0}?code={1}&email={2}" target="_blank">Click here to verify</a>'.format(  # noqa
        my_url, code, urllib.parse.quote(email)
    )

    email_lines = [
        "<b>Almost done!</b>",
        "",
        "<b>To complete your signup, we just need you</b>",
        "<b>to verify your email address: {0}</b>.".format(email),
        "",
        "<b>{0}</b>".format(link),
        "",
        "<b>Thank you!</b>",
        "",
        "",
        "You’re receiving this email because you recently created a new {{cookiecutter.project_name}} account.",
        "If this wasn’t you, please ignore this email.",
    ]

    event["response"]["emailSubject"] = "[{{cookiecutter.project_name}}] Please verify your email address."
    event["response"]["emailMessage"] = "<br>".join(email_lines)

    return event
