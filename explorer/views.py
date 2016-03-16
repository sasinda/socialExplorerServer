__author__ = 'sasinda'


import logging
from flask import Blueprint, current_app, render_template, Flask, request, abort
from flask_babel import gettext as _
from flask_security.utils import do_flash
import auth.models as models
import tw_hot_topic as tw
import insta as insta

app = Blueprint("explorer", __name__, template_folder="templates")

@app.route("/dashboard")
def dashboard():
    users=models.list_social_users()
    return render_template('/dashboard.html', social_users=users)

@app.route("/analyse")
def analyse():
    analType= request.args['analysis']
    provider= request.args['provider']
    profile_id1= request.args['profile_id_1']
    profile_id2= request.args['profile_id_1']

    user1=models.load_social_by_profile_id(profile_id1).first()
    user2=None
    if profile_id2!=None or profile_id2!='' :
        user2=models.load_social_by_profile_id(profile_id1).first()

    #Analysis switch
    if provider=='Facebook':
        template='/facebook.html'
        return render_template(template)
    elif provider=='Instagram':
        return render_template('/instagram.html', score=0.44)
    else:
        return renderTwitter(user1)


def renderTwitter(user):
    jason=None
    error=None
    template='/twitter.html'
    if(user.provider!='Twitter'):
         error="Use a Twitter users profile id not "+ user.provider
         do_flash(_(error), "error")
    else:
        token=user.access_token.encode('ascii','ignore')
        secret=user.secret.encode('ascii','ignore')
        jason=tw.json_for_twitter(token, secret)
    return render_template(template, data=jason, error=error)


def renderInstagram(user1, user2):
    score=None
    error=None
    template='/instagram.html'
    if(user1.provider!='Instagram' or user2.provider!='Instagram'):
         error="Use  profile ids of Instagram users not %s %s" % (user1.provider , user2.provider )
         do_flash(_(error), "error")
    else:
        token1=user1.access_token.encode('ascii','ignore')
        token2=user2.secret.encode('ascii','ignore')
        # score=insta.similarity(token1, token2)
        score=0.5
    return render_template(template, score=score, error=error)