# encoding: utf-8
import requests,urllib,json,hashlib,time,logging
import MySQLdb
import traceback

def get_app(app_id):
    tt = int(time.time()) * 1000
    sys_app_id = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    sys_app_secret = 'c37d661d-7e61-49ea-96a5-68c34e83db3a'
    get_app_sign = sign_md5(sys_app_id + str(tt) + sys_app_secret)
    data1 = {'app_id': sys_app_id, 'timestamp': tt, 'app_sign': get_app_sign, 'id': app_id}
    url_temp = "http://internal.beecloud.cn/data/external/get.apps.php"
    # url_temp = "http://internal.comsunny.com/data/external/get.apps.php"
    resp = requests.get(url_temp, params=data1).content
    # print resp
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


def log():
    logger = logging.getLogger('Test_channel')
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('/test201710311202.log')
    fh.setLevel(logging.DEBUG)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def connect_db():
    db = MySQLdb.connect("123.56.111.169", "beecloud", "beecloud617", "beetest", charset='utf8')
    cursor = db.cursor()
    return {"db":db,"cursor":cursor}

def modify_data(modify_sql):
    db_resp = connect_db()
    db = db_resp['db']
    cursor = db_resp['cursor']
    try:
        cursor.execute(modify_sql)
        db.commit()
        return 1
    except():
        db.rollback()
        # print ()
        print("modify_db_fail")
        return 0

def query_data(query_sql):
    db_resp = connect_db()
    db = db_resp['db']
    cursor = db_resp['cursor']
    # query_sql = "select * from "+table
    cursor.execute(query_sql)
    channels = cursor.fetchall()
    db.commit()
    db.close()
    return channels

# apps=get_app('afae2a33-c9cb-4139-88c9-af5c1df472e1')
# print apps
# json_map={"aa":11,"bb":22}
# try:
#     for key in json_map:
#         print json_map['www']
# except Exception,e:
#     print repr(e)

# optional={"aa":{"bb":"EXCEPTION"}}
# optional1={"aa":{"bb":"EXCEPTION"}}
# if optional==optional1:
#     print 'match'
# else:
#     print 'not match'
