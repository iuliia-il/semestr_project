from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, jsonify, session, g
from flask_login import login_required, current_user
from sqlalchemy.testing.pickleable import Foo

from main.messages.forms import MessageForm, SearchForm
from main.models import Message, db, User, Notification

messages = Blueprint('messages', __name__)


# Slouzi pro privatni komunikaci uzivatelu, kde "recipient" je libovolnym uzivatelem z DB, krome aktualniho.
# A take slouzi pro ukladani zprav do sqlite DB. Vztahuje se na stranku "users.html" kde je seznam vsech registrovanych
# uzivatelu systemu. Mozna schopnost odpovedet' pri kliknuti na jmeno autora zpravy.
@messages.route('/send_message', methods=['GET', 'POST'])
@messages.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('primary.about', username=recipient))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)


# slouzi pro zobrazeni prijatych zprav podle datuma (nove se nachazi nahore), a take moznost prepinat mezi strankami
# se zpravy (15 zprav na strance).
@messages.route('/messages')
@login_required
def msg():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages.msg', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages.msg', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


# upozorneni o nove zprave
@messages.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@messages.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))  # or what you want
    return render_template('search.html', form=form)


@messages.route('/search_results/<query>')
@login_required
def search_results(query):
  results = User.query.whoosh_search(query).all()
  return render_template('search_results.html', query=query, results=results)

