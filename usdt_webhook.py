# encoding: utf-8
from flask import Blueprint
from flask import Flask, request, redirect, render_template,Markup
import json
from common_func import *
from datetime import datetime,date
import MySQLdb,time,traceback

usdt_webhook_view = Blueprint('usdt_webhook', __name__)

@usdt_webhook_view.route('/verify',methods=['POST'])
def webhook():
    data=request.get_data()
    logger.info('recieve data:%s' % json.dumps(data, encoding='utf-8', ensure_ascii=False))
    return 'success'

