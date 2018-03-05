# encoding: utf-8
import time
from logging import NullHandler
from common_func import *
import requests
import uuid
import json
from flask import Flask, request, redirect, render_template,Markup,g,session
from haohuihua import haohuihua_view
from button import jsbutton_view
from channelTable import channelTable_view
from webhook import webhook_view
import webbrowser
from flask_login import (LoginManager,login_required,login_user,logout_user,UserMixin,current_user)


app=Flask(__name__)

# file_name = "E:\python learning\\api-test\log\\restbill_log.txt"
# fp = open(file_name,'a+')
app.register_blueprint(haohuihua_view, url_prefix='/user_info_3h')
app.register_blueprint(jsbutton_view, url_prefix='/jsbutton')
app.register_blueprint(channelTable_view, url_prefix='/channelTable')
app.register_blueprint(webhook_view,url_prefix='/webhook')
logger = log()

app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.session_protection = 'strong' #设置为strong的时候需要在登陆时候设置session.permanent = True.也可以选择设置为basic
login_manager.login_view = 'login'
login_manager.init_app(app)
login_manager.login_message = u"请登录！"
login_manager.login_message_category = "info"


hosts={
    'api':'https://api.beecloud.cn/2',
    '82.71':'http://123.56.82.71:8080/2',
    '75.44':'http://121.40.75.44:8080/2',
    '40.236':'http://115.28.40.236:8080/2',
    '66.169':'http://182.92.66.169:8080/2',
    '82.220':'http://47.93.82.220:8080/2',
    '120.98':'http://121.41.120.98:8080/2',
    '222.220':'http://120.24.222.220:8080/2',
    '3.98':'http://182.92.3.98:8080/2',
    'apitest98':'https://apitest98.beecloud.cn/2',
    'apitestsq':'https://apitestsq.beecloud.cn/2',
    '42.22':'http://123.56.42.22:8080/2',
    'apitest22':'https://apitest22.beecloud.cn/2',
    'api8271':'https://api8271.beecloud.cn/2',
    '191.185':'http://182.92.191.185:8080/2',
    'apitest185':'https://apitest185.beecloud.cn/2'
    }
users=[{'username':'beecloud','password':'beecloud617','user_id':'1qaz'},{'username':'bee','password':'bee','user_id':'2wsx'}]

class User(UserMixin):
    pass
def query_user(username):
    for user in users:
        if user['username']==username:
            return user
    return None
@login_manager.user_loader
def load_user(username):
    # return User.get(username)
    ##原来的代码
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id=username
        return curr_user
@app.before_request
def before_request():
    g.user=current_user




@app.route('/login',methods=['GET','POST'])
def login():
    if g.user.is_authenticated == True:
        return redirect('/channelTable')
    session.permanent = True
    if request.method == 'POST':
        # session['username']=request.form['username']
        # session['password']=request.form['password']
        username = request.form['username']
        password = request.form['password']

        user=query_user(username)
        if user == None:
            return render_template('login.html',error=u'用户名不存在')
        if str(password) == user['password']:

            curr_user = User()
            curr_user.id = username
            login_user(curr_user)
            print("auth:%r"%current_user.is_authenticated)
            return redirect('/channelTable')
        else:
            return render_template('login.html',error=u'密码错误')

    return render_template('login.html')
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    print(current_user.id)
    logout_user()
    # session.pop('username',None)
    # session.pop('password',None)

    return redirect('/login')

@app.route('/')
def hello_index():
    return app.send_static_file('index.html')

@app.route('/get_app')
def get_app_email():
    email = request.args.get('email').strip()
    tt = int(time.time()) * 1000
    sys_app_id = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    sys_app_secret = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    get_app_sign = sign_md5(sys_app_id + str(tt) + sys_app_secret)
    data1 = {'app_id': sys_app_id, 'timestamp': tt, 'app_sign': get_app_sign, 'email': email}
    url_temp = "http://internal.beecloud.cn/data/external/get.apps.php"
    # url_temp = "http://internal.comsunny.com/data/external/get.apps.php"
    resp = requests.get(url_temp, params=data1).content
    print resp
    resp_cut = resp[1:len(resp) - 1]
    resp_dict = json.loads(resp_cut)  # 字符串转化成字典。dumps字典转换成字符串
    # print(resp_dict)
    # resp_dict = eval(resp_cut)
    return render_template('new_index.html',email=email,apps=resp_dict)
    # return resp_dict['apps'][0]





@app.route('/bill',methods=['POST', 'GET'])
def bill():
    # bill_no = str(uuid.uuid1()).replace('-', '')
    bill_no = 'bike'+str(int(time.time())*1000)
    url = 'https://api.beecloud.cn/2'
    # url = 'http://120.26.72.189:8080/2'
    tt = int(time.time()) * 1000
    dat=str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    print "执行时间"+dat
    # fp.write("\n"+dat)
    # fp.write("  请求地址：%s  "%url)
    app_id = request.form['app_id']
    if app_id!=None:
        app_secret = get_app(app_id)['app_secret']
    else:
        return "app_id is empty"

    # app_secret = request.form['app_secret']
    channel = request.form['channel']
    if request.form['total_fee']!='':
        total_fee = int(request.form['total_fee'])
    else:
        total_fee = None
    coupon_id = request.form['coupon_id']
    if coupon_id=='':
        coupon_id=None
    auth_code = request.form['auth_code']
    card_no = request.form['card_no']
    #AFS T0的必传参数
    # bank_name = request.form['bank_name']
    # #print("bank_name:%s"%bank_name)
    # bank_num = request.form['bank_num']
    # idcard = request.form['idcard']
    # name = request.form['name']
    bank = request.form['gatewayBank']
    if bank=='':
        bank=None
    buyer_id = request.form['buyer_id']
    if buyer_id=='':
        buyer_id=None
    store_id = request.form['store_id']
    if store_id=='':
        store_id=None
    partition_id = request.form['partition_id']
    if partition_id=='':
        partition_id=None
    opt = request.form['optional']
    ana = request.form['analysis']
    pay_ip = request.remote_addr
    analysis={}
    # print pay_ip
    analysis['ip'] = pay_ip
    if ana != '':
        try:
            analysis.update(json.loads(ana))
        except ValueError:
            return "analysis must be json"
    else:
        analysis={"ip":pay_ip}
    if opt != '':
        try:
            optional = json.loads(opt)

        except ValueError:
            return "optional must be json"
    else:
        optional={"aa":"bb"}
    # optional['bank_name'] = bank_name
    # optional['bank_num'] = bank_num
    # optional['idcard'] = idcard
    # optional['name'] = name
    noti = request.form['notify_url']
    if noti == '':
        notify_url = 'http://mock.beecloud.cn:8001/webhook/verify'
    else:
        notify_url = noti

    host=request.form['host']
    if host!='':
        if host=='other':
            inputHost = request.form['inputHost']
            if inputHost != '':
                url='http://'+inputHost+':8080/2'
            else:
                url=hosts['api']
        else:
            url=hosts[host]
        # url=hosts[host]

    agent = request.form.get('agent1',default='1')
    sign = sign_md5(app_id+str(tt)+app_secret)
    online_bill_values={
        'app_id':app_id,
        'timestamp' : tt,
        'app_sign':sign,
        'channel':channel,#ali_web,un_web    CP_WEB  BC_WX_WAP  BC_ALI_QRCODE(url里不加offline)  BC_ALI_SCAN和BC_WX_SCAN是线下的（url加offline）_
        'title':'BeeCloud 渠道测试',#title过长时不传值到提示信息里
        'total_fee': total_fee, #2000000000  WX_NATIVE 渠道方错误 invalid total_fee  最大1000w
        'coupon_id':coupon_id,
        'bill_no': bill_no,
        'auth_code':auth_code,
        'card_no':card_no,
        'return_url':'http://mock.beecloud.cn:8001/test_return_url',
        'optional':optional,
        'notify_url':notify_url,
        'bank':bank,
        'buyer_id':buyer_id,
        'analysis':analysis,
        'store_id':store_id,
        'partition_id':partition_id
        }
    # print '传入参数：%r'%online_bill_values
    if agent == 'true':
        url_temp = url+"/rest/offline/agent/bill"
    else:
        if channel == 'BC_ALI_SCAN' or channel == 'BC_WX_SCAN' or channel == 'WX_SCAN' or channel == 'ALI_SCAN' or channel == 'ALI_OFFLINE_QRCODE':
            url_temp = url+"/rest/offline/bill"
        else:
            url_temp = url+"/rest/bill"
    # print url_temp
    logger.info(online_bill_values)
    logger.info('%s: %s'%(bill_no,url_temp))
    # resp=requests.post(url_temp,json=online_bill_values)
    resp = request_post(url_temp,online_bill_values)
    # fp.write("返回结果%s"%resp)
    # print resp
    # print_resp(resp)
    logger.info('%s: %r'%(bill_no,resp))
    return deal_with_pay(channel,resp,total_fee)


@app.route('/pay_bill',methods=['POST', 'GET'])
def pay_bill():
    # bill_no = str(uuid.uuid1()).replace('-', '')
    bill_no = 'bike' + str(int(time.time()) * 1000)
    url = 'https://api.beecloud.cn/2'
    resp={}
    # print(url)
    # url = 'http://120.26.72.189:8080/2'
    tt = int(time.time()) * 1000
    dat = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print "执行时间" + dat
    # fp.write("\n"+dat)
    # fp.write("  请求地址：%s  "%url)
    app_id = request.args.get('app_id')
    channel = request.args.get('channel')
    total_fee = request.args.get('total_fee')
    if total_fee!=None and total_fee !='':
        total_fee = int(float(total_fee) * 100)
    # print total_fee
    else:
        resp["result_code"] = 1
        resp["errMsg"] = "金额不能为空"
        resp=json.dumps(resp)
        return resp
    auth_code = request.args.get('auth_code')
    card_no = request.args.get('card_no')
    # AFS T0的必传参数
    # bank_name = request.form['bank_name']
    # print("bank_name:%s"%bank_name)
    # bank_num = request.form['bank_num']
    # idcard = request.form['idcard']
    # name = request.form['name']
    ##积分通道必传参数
    user_fee = request.args.get('user_fee')#用户的手续费
    fc_card_no = request.args.get('fc_card_no')#出款卡
    user_name = request.args.get('user_name')#姓名
    user_cert_no = request.args.get('user_cert_no')#身份证号
    user_mobile = request.args.get('user_mobile')#付款卡手机号
    ##shenfu通道必传参数，user_name,user_cert_no,user_fee与积分通道重复
    pay_bank_expiry_date=request.args.get('pay_bank_expiry_date')
    pay_bank_cvv2=request.args.get('pay_bank_cvv2')
    payee_card_no=request.args.get('payee_card_no')
    mobile_no=request.args.get('mobile_no')
    payee_mobile_no=request.args.get('payee_mobile_no')
    ##齐商京东必传参数  user_mobile积分通道已取
    id_no = request.args.get('id_no')
    id_holder = request.args.get('id_holder')
    bank=request.args.get('bank')
    card_exp = request.args.get('card_exp')
    card_cvv2 = request.args.get('card_cvv2')
    card_type = request.args.get('card_type')
    # print card_no
    optional = {"aa": "bb"}
    optional['user_fee'] = user_fee
    optional['fc_card_no'] = fc_card_no
    optional['user_name'] = user_name
    optional['user_cert_no'] = user_cert_no
    optional['user_mobile'] = user_mobile
    #shenfu通道补充的参数
    optional['pay_bank_expiry_date'] = pay_bank_expiry_date
    optional['pay_bank_cvv2'] = pay_bank_cvv2
    optional['payee_card_no'] = payee_card_no
    optional['mobile_no'] = mobile_no
    optional['payee_mobile_no'] = payee_mobile_no

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
        'channel': channel,
        # ali_web,un_web    CP_WEB  BC_WX_WAP  BC_ALI_QRCODE(url里不加offline)  BC_ALI_SCAN和BC_WX_SCAN是线下的（url加offline）_
        'title': 'BeeCloud 渠道测试',  # title过长时不传值到提示信息里
        'total_fee': total_fee,  # 2000000000  WX_NATIVE 渠道方错误 invalid total_fee  最大1000w
        'bill_no': bill_no,
        'auth_code': auth_code,
        'card_no': card_no,
        'return_url': 'http://beecloud.cn',
        'optional': optional,
        'notify_url': 'https://mock.beecloud.cn:8001/webhook/verify',
        'id_holder':id_holder,
        'id_no':id_no,
        'bank':bank,
        'card_type':card_type

    }
    # print '传入参数：%r' % online_bill_values
    if channel == 'BC_ALI_SCAN' or channel == 'BC_WX_SCAN' or channel == 'WX_SCAN' or channel == 'ALI_SCAN' or channel == 'ALI_OFFLINE_QRCODE':
        url_temp = url + "/rest/offline/bill"
    else:
        url_temp = url + "/rest/bill"
    # print url_temp
    logger.info(online_bill_values)
    logger.info(url_temp)
    # resp=requests.post(url_temp,json=online_bill_values)
    resp = request_post(url_temp, online_bill_values)
    # fp.write("返回结果%s"%resp)
    # print resp
    # print_resp(resp)
    logger.info('%s: %r'%(online_bill_values['bill_no'],resp))
    resp['channel']=channel
    resp=json.dumps(resp)
    return resp


def deal_with_pay(channel,resp,total_fee):
    resp_str=json.dumps(resp, encoding='utf-8', ensure_ascii=False)
    if channel == 'BC_WX_WAP' or channel == 'WX_WAP':
        if 'url' in resp.keys():
            # word = u'微信wap的返回数据，把以下的url在手机端的非微信浏览器打开即可支付'
            # return render_template('show_url.html', word = word,result=resp,url=resp['url'],id=resp['id'],err_detail=resp['err_detail'].encode('utf-8'))
            return render_template('wx_wap.html',content=resp['url'])
        else:
            return render_template('show_url.html', result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])

    elif channel == 'BC_NATIVE' or channel == 'BC_ALI_QRCODE' or channel == 'ALI_OFFLINE_QRCODE' or channel == 'WX_NATIVE' or channel=='BC_QQ_NATIVE':
        if 'code_url' in resp.keys():
            if resp['code_url'] !='' and resp['result_code'] == 0:
                print resp['code_url']
                return render_template('qrcode.html', raw_content=resp['code_url'], total_fee=total_fee,channel = channel)
            else:
                return render_template('show_url.html', result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])
        else:
            return render_template('show_url.html', result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])
    elif channel=='BC_ALI_APP':#考虑包的bc_ali_app
        if resp['result_code'] == 0:
            if 'code_url' in resp.keys():
                if resp['code_url'] != '':
                # print resp['code_url']
                    return render_template('qrcode.html', raw_content=resp['code_url'], total_fee=total_fee,channel = channel)
            else:
                return render_template('show_url.html', result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])
        else:
            return render_template('show_url.html', result=resp_str, err_detail=resp['err_detail'],
                                   result_code=resp['result_code'])
    elif channel == 'ALI_WEB' or channel == 'ALI_WAP' or channel =='ALI_QRCODE' or channel == 'BC_ALI_WEB':
        if 'url' in resp.keys():
            if resp['url'] != '' and resp['result_code'] == 0:
                return redirect(resp['url'])
            else:
                return render_template('show_url.html', result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])
        else:
            return render_template('show_url.html', result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])
    elif channel == 'BC_WX_SCAN' or channel == 'BC_ALI_SCAN' or channel == 'ALI_SCAN' or channel == 'WX_SCAN':
        if resp['result_code']==0 and resp['pay_result']==True:
            return app.send_static_file('success.html')
        else:
            return render_template('show_url.html',result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])
    elif channel == 'BC_EXPRESS' or channel == 'UN_WEB' or channel == 'UN_WAP' or channel == 'BC_GATEWAY' or channel == 'JD_WEB' or channel =='JD_WAP':
        if resp['result_code'] == 0:
            # if 'url' in resp.keys() and resp['url']!='':
            #     print resp['url']

                # return redirect(resp['url'])
            if 'html' in resp.keys() and resp['html'] != '':
                print 222222222222
                return render_template('blank.html',content=Markup(resp['html']))
            else:
                return render_template('show_url.html', result=resp_str, err_detail=resp['err_detail'],
                                       result_code=resp['result_code'])
        else:
            return render_template('show_url.html',result=resp_str,err_detail=resp['err_detail'],result_code=resp['result_code'])
    elif channel == 'BC_ALI_WAP':
        if 'code_url' in resp.keys():
            if resp['code_url'] !='' and resp['result_code'] == 0:
                return render_template('qrcode.html', raw_content=resp['code_url'], total_fee=total_fee)
            else:
                return render_template('show_url.html',result=resp_str, err_detail=resp['err_detail'],result_code=resp['result_code'])
        elif 'url' in resp.keys():
            if resp['url'] != '' and resp['result_code'] == 0:
                return redirect(resp['url'])
            else:
                return render_template('show_url.html',result=resp_str, err_detail=resp['err_detail'],
                                       result_code=resp['result_code'])
        else:
            return render_template('show_url.html',result=resp_str, err_detail=resp['err_detail'],
                                   result_code=resp['result_code'])
    elif channel =='WX_APP' or channel == 'ALI_APP' or channel == 'BC_WX_APP':
        return render_template('show_url.html',result=resp_str)
    # elif channel =='BC_ALI_QRCODE':
    #     return render_template('newjs.html',code_url=resp['code_url'])
    else:
        return render_template('show_url.html',result=resp_str, err_detail=resp['err_detail'],
                                   result_code=resp['result_code'])



@app.route('/pay_test',methods=['POST','GET'])
def pay_test():
    app_id = request.args.get('app_id')#从url里获取app_id
    sub_channel = request.args.get('sub_channel')#从url里获取sub_channel
    if app_id!=None:
        resp_dict = get_app(app_id)
        app_secret = resp_dict['app_secret']
        bc_express_channel_type = resp_dict['bc_express_channel_type']
        master_secret = resp_dict['master_secret']
        # print bc_express_channel_type
        # print app_secret
        # sign=sign_md5(app_id+str(tt)+app_secret)
        return render_template('pay_test.html',app_id=app_id,channel=sub_channel,app_secret=app_secret,bc_express_channel_type=bc_express_channel_type)
    else:
        return 'app_id is None'

@app.route('/jinjian',methods=['POST','GET'])
def jinjian():
    url = 'https://api.beecloud.cn/2/rest/merchantsettled'
    # url = 'http://192.168.1.100:8080/2/rest/merchantsettled'
    tt = int(time.time()) * 1000
    resp={}
    app_id = request.args.get('app_id')#从url里获取app_id
    id_no = request.args.get('jinjian_id_no')
    contact = request.args.get('jinjian_contact')
    card_no = request.args.get('jinjian_card_no')
    id_holder = request.args.get('jinjian_id_holder')
    if app_id!=None:
        resp_dict = get_app(app_id)
        app_secret = resp_dict['app_secret']
        sign=sign_md5(app_id+str(tt)+app_secret)
        jinjian_value={'app_id':app_id,
                       'app_sign':sign,
                       'timestamp':tt,
                       'id_no': id_no,
                       'contact': contact,
                       'card_no': card_no,
                       'id_holder': id_holder
                       }
        resq=json.dumps(jinjian_value, encoding='utf-8', ensure_ascii=False)
        logger.info('jinjian_request:%s' %resq)
        resp=request_post(url,jinjian_value)
        resp=json.dumps(resp)
        logger.info('jinjian_result:%s' %json.dumps(resp,encoding='utf-8', ensure_ascii=False))

        return resp
    else:
        resp['result_code']=1
        resp['errMsg']='app_id is None'
        resp=json.dumps(resp)
        return resp
@app.route('/SFConfirm',methods=['GET'])
def SFConfirm():
    url = 'https://api.beecloud.cn/2/rest/bill/confirm'
    # url = 'http://192.168.1.100:8080/2/rest/merchantsettled'
    tt = int(time.time()) * 1000
    resp = {}
    confirm_para={}
    app_id = request.args.get('app_id')
    token = request.args.get('token')
    bc_bill_id = request.args.get('bc_bill_id')
    verify_code = request.args.get('verify_code')
    if app_id != None:
        resp_dict = get_app(app_id)
        app_secret = resp_dict['app_secret']
        sign = sign_md5(app_id + str(tt) + app_secret)
        confirm_para={ 'app_id':app_id,
                        'timestamp' : tt,
                        'app_sign':sign,
                        'token':token,
                        'bc_bill_id':bc_bill_id,
                        'verify_code':verify_code
                     }
        req = json.dumps(confirm_para, encoding='utf-8', ensure_ascii=False)
        logger.info('SFConfirm_request:%s' % req)
        resp = request_post(url, confirm_para)
        resp = json.dumps(resp)
        logger.info('SFConfirm_result:%s' % resp)
        return resp
@app.route('/webhook',methods=['POST'])
def webhook():
    ip = request.remote_addr
    print 'webhook from:' + ip
    json_data = request.get_json()
    print json_data
    logger.info('recieve webhook:%s' % json.dumps(json_data, encoding='utf-8', ensure_ascii=False))
    if str(ip) =='123.57.146.46' or str(ip) == '182.92.114.175' or str(ip) == '123.57.81.91':
        # 第一步：验证数字签名
        # 从beecloud传回的sign
        bc_sign = json_data['signature']
        app_id = json_data['app_id']
        bill_no = json_data['transaction_id']
        transaction_fee = json_data['transaction_fee']
        transaction_type = json_data['transaction_type']
        channel_type = json_data['channel_type']

        if app_id!=None:
            resp_dict = get_app(app_id)
            app_master_secret = resp_dict['master_secret']
            signature = sign_md5(app_id + bill_no + transaction_type + channel_type + str(
                transaction_fee) + app_master_secret)
            # 判断两个sign是否一致
            if bc_sign != signature:
                logger.info("%s signature cannot match"%bill_no)
                return "signature cannot match"
            else:
                logger.info('%s webhook success' % bill_no)
                return 'success'
        else:
            logger.info("%s app_id is None" % bill_no)
            return "app_id is None"
    else:
        # print 'ip is not from beecloud,ip is:' + ip
        logger.info('ip is not from beecloud,ip is:' + ip)
        return 'ip is not from beecloud,ip is:' + ip



@app.route('/test_return_url',methods=['GET','POST'])
def test_return_url():

    print request.values
    aa=str(request.values)
    return aa

# fp.close()
if __name__ == '__main__':
    app.debug = True
    # app.run(host='pythondemo.beecloud.cn', port=80)
    # app.run(host='192.168.2.119',port=5000)
    app.run(host='0.0.0.0',port=5000)
    # app.run()
