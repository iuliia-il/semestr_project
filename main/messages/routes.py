from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from main.models import Message
from main.messages.forms import AddMessageForm

messages = Blueprint('messages', __name__)

@messages.route("/chat_form")
def chat():
    return render_template('chat_form.html')
