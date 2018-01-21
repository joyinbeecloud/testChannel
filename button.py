# encoding: utf-8
import json
import hashlib
import time
import json
import requests,logging,random
from flask import Flask, request, redirect, render_template, Markup,jsonify
from flask import Blueprint
from common_func import *

jsbutton_view = Blueprint('button', __name__)
app=Flask(__name__)
logger = logging.getLogger('jsButtonTest')
logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('/jsButtonTest.log')
fh.setLevel(logging.DEBUG)
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)



# def sign_md5(need_md5_str):
#     print(need_md5_str)
#     m=hashlib.md5()
#     m.update(need_md5_str.encode('utf-8'))
#     get_md5= m.hexdigest()
#     return get_md5

#获取时间戳
tt=time.time()
tt=int(tt)*1000
timeStamp= str(tt)


title="CMFJSButtonTest"
return_url = 'https://beecloud.cn'
debug=True
optional={"aa":"bbb"}
card_no='6217906101007446144'
hosts={
    'api':'https://api.beecloud.cn',
    '82.71':'http://123.56.82.71:8080',
    '75.44':'http://121.40.75.44:8080',
    '40.236':'http://115.28.40.236:8080',
    '66.169':'http://182.92.66.169:8080',
    '82.220':'http://47.93.82.220:8080',
    '120.98':'http://121.41.120.98:8080',
    '222.220':'http://120.24.222.220:8080',
    '3.98':'http://182.92.3.98:8080',
    'apitest98':'https://apitest98.beecloud.cn',
    'apitest22':'https://apitest22.beecloud.cn',
    'api8271':'https://api8271.beecloud.cn',
    '42.22':'http://123.56.42.22:8080',
    '191.185':'http://182.92.191.185:8080',
    'apitest185':'https://apitest185.beecloud.cn'
    }



@jsbutton_view.route('')
def hello_index():
    return app.send_static_file('js_email.html')

@jsbutton_view.route('/get_app')
def get_app_email():
    email = request.args.get('email').strip()
    print(email)
    tt = int(time.time()) * 1000
    sys_app_id = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    sys_app_secret = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    get_app_sign = sign_md5(sys_app_id + str(tt) + sys_app_secret)
    data1 = {'app_id': sys_app_id, 'timestamp': tt, 'app_sign': get_app_sign, 'email': email}
    url_temp = "http://internal.beecloud.cn/data/external/get.apps.php"
    # url_temp = "http://internal.comsunny.com/data/external/get.apps.php"
    resp = requests.get(url_temp, params=data1).content
    resp_str=resp.decode()#python3 上面这条返回的是bytes，所以要解码成str，就可以了
    resp_cut = resp_str[1:len(resp_str) - 1]
    # print(resp_cut)
    resp_dict = json.loads(resp_cut)  # 字符串转化成字典。dumps字典转换成字符串
    print(resp_dict)
    return jsonify(resp_dict)
    # return render_template('new_index.html',email=email,apps=resp_dict)




@jsbutton_view.route('/button',methods=['GET'])
def button():
    out_trade_no = "cmfjs" + str(int(time.time())) + str(random.randint(1,100))
    app_id=request.args.get('app_id')
    app_secret = request.args.get('app_secret')
    amount=request.args.get('total_fee')
    card_no=request.args.get('card_no')
    print(out_trade_no)
    str1 = str(app_id) + str(title) + str(amount) + str(out_trade_no) + str(app_secret)
    sign = sign_md5(str1)
    print(sign)
    host = request.args.get('host')
    if host != '':
        url = hosts[host]
    else:
        url = hosts['api']
    print(url)
    return render_template("spay-button.html", title=title, amount=amount, out_trade_no=out_trade_no, sign=sign,
                               debug=debug, optional=optional, card_no=card_no,app_id=app_id,url=url)


    # user_agent = request.headers.get('User-Agent')
    # if "MicroMessenger" in user_agent:
    #     open_id = request.args.get('openid')
    #     if not open_id:
    #         url = "http://wxactivity.beecloud.cn/activity/get.openid.php?callbackurl=" + "http://192.168.1.117:9887/" + "&app_id=" + app_id
    #         print(url)
    #         return redirect(url)
    #     else:
    #         print(open_id)
    #         return render_template("spay-button.html", title=title, amount=amount, out_trade_no=out_trade_no,sign=sign, debug=debug, optional=optional,card_no=card_no,open_id=open_id,app_id=app_id,url=url)
    # else:
    #     return render_template("spay-button.html", title=title, amount=amount, out_trade_no=out_trade_no, sign=sign,
    #                            debug=debug, optional=optional, card_no=card_no,app_id=app_id,url=url)
#
#
# if __name__=='__main__':
#     app.run('0.0.0.0', port='9887')


