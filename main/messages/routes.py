from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, jsonify
from flask_login import login_required, current_user
from main.messages.forms import MessageForm
from main.models import Message, db, User, Notification

messages = Blueprint('messages', __name__)


# Slouzi pro privatni komunikaci uzivatelu, kde "recipient" je libovolnym uzivatelem z DB, krome aktualniho.
# A take slouzi pro ukladani zprav do sqlite DB. Vztahuje se na stranku "about.html" (pak zmenim nazev na logicky),
# kde je seznam vsech registrovanych uzivatelu systemu.
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


# Mozna schopnost odpovedet' pri kliknuti na jmeno autora zpravy, ale jeste nefunguje tak, jak treba, to musim upravit.
@messages.route('/send_message/<post>/<author>', methods=['GET', 'POST'])
@login_required
def send_message_to(author):
    user = User.query.filter_by(username=author).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('primary.about', username=author))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=author)


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
