# encoding: utf-8
from flask import Blueprint
from flask import Flask, request, redirect, render_template,Markup
import json
from common_func import *
from datetime import datetime,date
import MySQLdb,time,traceback

yyt_test_view = Blueprint('yyt_test', __name__)





def deal_with_pay(resp):
    resp_str=json.dumps(resp, encoding='utf-8', ensure_ascii=False)
    if 'html' in resp.keys() and resp['html'] != '':
        print 222222222222
        return render_template('blank.html', content=Markup(resp['html']))

    else:
        return render_template('show_url.html', result=resp_str, err_detail=resp['err_detail'],
                           result_code=resp['result_code'])



@yyt_test_view.route('/yyt_bc_gateway',methods=['POST', 'GET'])
def yinyingtong_bc_gateway():
    bill_no = 'bike' + str(int(time.time()) * 1000)

    url = request.args.get('host')
    # url = 'https://api.beecloud.cn/2'
    print url
    resp = {}
    # print(url)
    # url = 'http://120.26.72.189:8080/2'
    tt = int(time.time()) * 1000
    dat = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print "执行时间" + dat
    # fp.write("\n"+dat)
    # fp.write("  请求地址：%s  "%url)
    app_id = "afae2a33-c9cb-4139-88c9-af5c1df472e1"

    if app_id!=None:
        resp_dict = get_app(app_id)
        app_secret = resp_dict['app_secret']
        sign=sign_md5(app_id+str(tt)+app_secret)

    else:
        return "app_id is none"
    online_bill_values = {
        'app_id': app_id,
        'timestamp': tt,
        'app_sign': sign,
        'channel': "BC_GATEWAY",
        # ali_web,un_web    CP_WEB  BC_WX_WAP  BC_ALI_QRCODE(url里不加offline)  BC_ALI_SCAN和BC_WX_SCAN是线下的（url加offline）_
        'title': 'BeeCloud 渠道测试',  # title过长时不传值到提示信息里
        'total_fee': 10000,  # 2000000000  WX_NATIVE 渠道方错误 invalid total_fee  最大1000w
        'bill_no': bill_no,
        'return_url': 'http://beecloud.cn',
        'notify_url': 'https://mock.beecloud.cn:8001/webhook/verify',
        'bank':'102100099996'
    }
    url_temp = url + "/rest/bill"
    resp = request_post(url_temp, online_bill_values)
    resp['channel'] = "BC_GATEWAY"
    # resp = json.dumps(resp)
    print resp
    # return resp
    return deal_with_pay(resp)

@yyt_test_view.route('/',methods=['POST', 'GET'])
def yyt():
    return render_template('yyt_test.html')


