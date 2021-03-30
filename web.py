import os
import json
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from database import clients
from tbot import telegram_post
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from forms import TelegramMessage
from update import rescan

app = Flask(__name__, template_folder='templates')

TOP_LEVEL_DIR = os.path.abspath(os.curdir)
engine = create_engine('sqlite:///' + TOP_LEVEL_DIR + '/db/sqlite.db', echo=False, connect_args={"check_same_thread": False}) #, echo=True
Session = sessionmaker(bind=engine)
session = Session()

app.config.update(dict(SECRET_KEY="powerful secretkey", WTF_CSRF_SECRET_KEY="a csrf secret key"))


@app.route('/')
def index():
    if request.args.get('telegram_msg'):
        tg_msg = True
    else:
        tg_msg = False
    if request.args.get('network_rescan'):
        n_rescan = True
    else:
        n_rescan = False
    data = session.query(clients).all()
    list = []
    for d in data:
        j = {}
        j['id'] = d.id
        j['mac'] = d.mac
        j['data'] = json.loads(d.data)
        list.append(j)
    tgmsg_form = TelegramMessage(request.form)
    return render_template('index.html',
        data=list,
        settings=settings,
        tgmsg_form=tgmsg_form,
        tg_msg=tg_msg,
        n_rescan=n_rescan
    )

@app.route('/telegram/message', methods=('GET','POST'))
def telegram_msg():
    if settings['telegram']['test_msg_enable']:
        form = TelegramMessage(request.form)
        if request.method == 'POST' and form.validate():
            telegram_post(form.tgmsg.data)
            return redirect(url_for('index',
                telegram_msg='true')
            )
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/client/delete/<clientid>')
def create(clientid):
    if id:
        session.query(clients).filter_by(id=clientid).delete()
        session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/network/rescan')
def network_rescan():
    rescan()
    return redirect(url_for('index', network_rescan='true'))

if __name__ == '__main__':
   app.run(
    debug = True,
    host = '0.0.0.0'
   )
