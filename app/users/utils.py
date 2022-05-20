from flask import url_for
from flask_mail import Message
from PIL import Image
import os, secrets
#==============================================================================
from app import app, mail

# NOTE: Make sure two way authentication of your `MAIL_USERNAME` is turned off. 
# Google is going to make `Two Way Authentication` mandatory from May-31, 2022. 
# So in order to have this application working properly, refactor is needed 
# after the date.
def _send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def _save_piture(form_pic):
    random_hex = secrets.token_hex(8)
    _, extention = os.path.splitext(form_pic.filename)
    pic_file_name = random_hex+extention
    path = os.path.join(app.root_path, 'static/profile_pics', pic_file_name)

    resize_to = (125,125)
    with Image.open(form_pic) as img:
        img.thumbnail(resize_to)
        img.save(path)

    return pic_file_name
