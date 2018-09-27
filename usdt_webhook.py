# encoding: utf-8
from flask import Blueprint
from flask import Flask, request, redirect, render_template,Markup
import json
from common_func import *
from datetime import datetime,date
import MySQLdb,time,traceback

usdt_webhook_view = Blueprint('usdt_webhook', __name__)
apps={'a35dac4b-00c4-4930-9271-aed06810dd0c':'2034607c-1afc-47c5-bd66-6dfa00b1c524',
      '0a5e78a3-ca29-4b63-906b-eb66dedf08a0':'e7247996-6e3d-47c7-8d75-944b8b29467f',
      'dc767edf-5123-483a-a166-9632f1bd4657':'cdb1252a-1ff7-4e31-9d7f-27826a3768b6',
      '8741ef83-db4f-4bd7-ac97-049064bda5f5':'3c367b6a-faa0-48fb-b5d7-a1c6f3951b44'}

@usdt_webhook_view.route('/verify',methods=['POST'])
def webhook():
    try:
        data=request.get_json()
        logger.info('USDT_webhook data:%s' % json.dumps(data, encoding='utf-8', ensure_ascii=False))
        recieve_appSign=data['appSign']
        app_id=data['appId']
        app_secret=apps[app_id]
        if 'appSign' in data:
            data.pop('appSign')
        appSign=dict_sorted_and_sign(data,app_secret)
        if appSign==recieve_appSign:
            logger.info('hashcode:%s,success'%data['hashcode'])
            return 'success'
        else:
            logger.info('hashcode:%s,recieved appSign:%s,calculate appSign:%s'%(data['hashcode'],recieve_appSign,appSign))
            return 'appSign not match'
    except Exception, e:
        logger.info(traceback.print_exc(e))
        data = request.get_data()
        logger.info('USDT_exception data:%s' % json.dumps(data, encoding='utf-8', ensure_ascii=False))
        return 'except success'

