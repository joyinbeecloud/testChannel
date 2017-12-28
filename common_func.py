# encoding: utf-8
import requests,urllib,json,hashlib,time


def get_app(app_id):
    tt = int(time.time()) * 1000
    sys_app_id = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    sys_app_secret = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    get_app_sign = sign_md5(sys_app_id + str(tt) + sys_app_secret)
    data1 = {'app_id': sys_app_id, 'timestamp': tt, 'app_sign': get_app_sign, 'id': app_id}
    url_temp = "http://internal.beecloud.cn/data/external/get.apps.php"
    # url_temp = "http://internal.comsunny.com/data/external/get.apps.php"
    resp = requests.get(url_temp, params=data1).content
    print resp
    resp_cut = resp[1:len(resp) - 1]
    resp_dict = json.loads(resp_cut)#字符串转化成字典。dumps字典转换成字符串
    # print(type(resp_dict))
    # resp_dict = eval(resp_cut)
    return resp_dict['apps'][0]


def request_post(url,params):
    # print(url)
    jdata = json.dumps(params)
    # print(jdata)
    #r1 = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
    try:
        r=requests.post(url,json=params)
        #print(r.status_code)
    except requests.exceptions.HTTPError:
        return "httperror"
    # print(r.status_code)
    if r.status_code==200:
         # print('common function200')
         resp=r.json()
         # common_func.print_resp(resp)
         return resp
    else:
        # print('common_func'+str(r.status_code))
        # r=r.json()
        return r
        # return r.status_code
def request_get(url):
    param1={"type":"C"}
    param2=json.dumps(param1)
    param=urllib.parse.quote_plus(param2)
    url=url+'?para='+param
    print(url)
    resp_get = requests.get(url)
    resp = resp_get.json()
    return resp
def request_delete(url,param):
    resp = requests.delete(url,params=param)
    if resp.status_code ==200:
        cancel_resp = resp.json()
        # common_func.print_resp(cancel_subs_resp)
        return cancel_resp
    else:
        return resp
def request_put(url,param):
    resp = requests.put(url,json = param)
    put_resp = resp.json()
    # common_func.print_resp(cancel_subs_resp)
    if resp.status_code ==200:
        put_resp = resp.json()
        # common_func.print_resp(cancel_subs_resp)
        return put_resp
    else:
        return resp

def sign_md5(str1):
    m=hashlib.md5()
    m.update(str1.encode('utf-8'))
    get_md5= m.hexdigest()
    return get_md5

def print_resp(resp):
    dict={'name':'python','english':33,'math':35}
    l=[]
    if type(l) is type(resp):
        for r in resp:
            if type(r) is type(dict):
                for i in r:
                    print("%s:%s"%(i,r[i]))
            else:
                print(resp)
    else:
        if type(resp) is type(dict):
                for i in resp:
                    print("%s:%s"%(i,resp[i]))
        else:
            print(resp)

def url_encode(paramm):
    param1=paramm
    param2=json.dumps(param1)
    param=urllib.parse.quote_plus(param2)
    return param

def attachAppSign(reqPara,bcapp):
    bcapp.app_id

