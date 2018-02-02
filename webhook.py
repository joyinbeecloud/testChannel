# encoding: utf-8
from flask import Blueprint
from flask import Flask, request, redirect, render_template,Markup
import json
from common_func import *
from datetime import datetime,date
import MySQLdb,time,traceback

webhook_view = Blueprint('webhook', __name__)
logger=log()

def query_bill(query_param):
    query_param_str = json.dumps(query_param)
    en_param = urllib.quote_plus(query_param_str.encode('utf-8'))
    url_temp = 'https://api.beecloud.cn/2/rest/bills?para=' + en_param
    # print("/rest/bills接口请求参数%s"%query_param_str)
    query_bill_resp = requests.get(url_temp).json()
    if 'bills' in query_bill_resp:
        # print ('/rest/bills接口响应内容%r'%query_bill_resp['bills'])
        return query_bill_resp['bills']
    else:
        # print ('/rest/bills接口响应内容%r'%query_bill_resp)
        return 0
def query_refund(query_param):
    query_param_str = json.dumps(query_param)
    en_param = urllib.quote_plus(query_param_str.encode('utf-8'))
    url_temp = 'https://api.beecloud.cn/2/rest/refunds?para=' + en_param
    # print("/rest/bills接口请求参数%s"%query_param_str)
    query_bill_resp = requests.get(url_temp).json()
    if 'refunds' in query_bill_resp:
        # print ('/rest/bills接口响应内容%r'%query_bill_resp['refunds'])
        return query_bill_resp['refunds']
    else:
        # print ('/rest/bills接口响应内容%r'%query_bill_resp)
        return 0


def create_insert_sql(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type):
    insert_sql="INSERT INTO webhook_results(bill_no,bill_id,webhook_result,ip,createdAt,refund_no,transaction_type) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type)
    return insert_sql



@webhook_view.route('/verify',methods=['POST'])
def webhook():

    bill_query_param={}
    webhook_param = {}
    bill_param = {}
    bill_webhook_verify=0
    signature='0'
    bc_sign='1'
    Is_bill_id_match=0
    tt = int(time.time())*1000
    ip = request.remote_addr
    refund_no=''
    createdAt = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    #从webhook里拿信息
    try:
        json_data = request.get_json()
        logger.info('recieve webhook:%s' % json.dumps(json_data, encoding='utf-8', ensure_ascii=False))
        bc_sign = json_data['signature']
        app_id = json_data['app_id']
        transaction_id = json_data['transaction_id']
        transaction_fee = json_data['transaction_fee']
        transaction_type = json_data['transaction_type']
        channel_type = json_data['channel_type']
        webhook_bill_id = json_data['id']
        trade_success = json_data['trade_success']
        message_detail = json_data['message_detail']
        optional = json_data['optional']
        sub_channel_type = json_data['sub_channel_type']
        if transaction_type=='PAY':
            bill_fee = json_data['bill_fee']
            discount = json_data['discount']
            coupon_id = json_data['coupon_id']
            webhook_param = {"transaction_fee": transaction_fee, "channel_type": channel_type,
                             "bill_id": webhook_bill_id,
                             "optional": optional, "sub_channel_type": sub_channel_type, "bill_fee": bill_fee,
                             "discount": discount, "coupon_id": coupon_id}
        else:
            webhook_param = {"transaction_fee": transaction_fee, "channel_type": channel_type,
                             "bill_id": webhook_bill_id,
                             "optional": optional, "sub_channel_type": sub_channel_type}
    except Exception,e:
        logger.info(traceback.print_exc(e))
        return '获取webhook内容异常'
    #根据app_id查询app_secret并生成sign
    if app_id != None:
        resp_dict = get_app(app_id)
        app_master_secret = resp_dict['master_secret']
        app_secret = resp_dict['app_secret']
        signature = sign_md5(app_id + transaction_id + transaction_type + channel_type + str(
            transaction_fee) + app_master_secret)
        sign = sign_md5(app_id+str(tt)+app_secret)
    else:
        logger.info("%s app_id is None" % transaction_id)
        return "app_id is None"

    bill_query_param["app_id"]=app_id
    bill_query_param["app_sign"] = sign
    bill_query_param["timestamp"] = tt

    if transaction_type=='PAY':
        bill_query_param["bill_no"] = transaction_id
        query_transaction_resp = query_bill(bill_query_param)
    elif transaction_type=='REFUND':
        print 'refund'
        bill_query_param["refund_no"] = transaction_id
        query_transaction_resp = query_refund(bill_query_param)

    #从bills/refunds查询取内容
    if query_transaction_resp!=0 and query_transaction_resp!=[]:
        for transaction in query_transaction_resp:
            bill_id=transaction['id']#支付订单或者退款订单的id
            if bill_id == webhook_bill_id:#由于存在订单号重复的可能性，故只取id一样的订单做比较
                Is_bill_id_match = 1
                bill_channel_type = transaction['channel']
                bill_sub_channel_type = transaction['sub_channel']
                bill_optional = transaction['optional']
                if transaction_type=='PAY':
                    bill_transaction_fee = transaction['total_fee']
                    bill_bill_fee = transaction['bill_fee']
                    bill_discount = transaction['discount']
                    bill_coupon_id = transaction['coupon_id']
                    bill_param = {"transaction_fee": bill_transaction_fee, "channel_type": bill_channel_type,
                                  "bill_id": bill_id,
                                  "optional": bill_optional, "sub_channel_type": bill_sub_channel_type,
                                  "bill_fee": bill_bill_fee,
                                  "discount": bill_discount, "coupon_id": bill_coupon_id}
                else:
                    bill_transaction_fee = transaction['refund_fee']
                    refund_no = transaction_id
                    transaction_id = transaction['bill_no']
                    bill_param={"transaction_fee":bill_transaction_fee,"channel_type":bill_channel_type,"bill_id":bill_id,
                      "optional":bill_optional,"sub_channel_type":bill_sub_channel_type}
        if Is_bill_id_match == 1:
            pass
        else:
            logger.info('/rest/bills接口查询内容与webhook内容对比，bill_id not match')
            return '/rest/bills接口查询内容与webhook内容对比，bill_id not match'
    else:
        logger.info('/rest/bills接口查询结果为空')
        return '/rest/bills接口查询结果为空'


    #bills接口查询出来的内容与收到的webhook内容做比较
    for key in bill_param:
        if key in webhook_param:
            if key=='optional':
                bill_optional1=json.loads(bill_param[key])
                IS_optional_match = cmp(bill_optional1,webhook_param[key])
                if IS_optional_match==0:
                    pass
                else:
                    result_msg = key + ' not match'
                    logger.info(transaction_id + ':' + result_msg)
                    modify_data(create_insert_sql(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type))
                    return transaction_id + ':' + result_msg
            else:
                if bill_param[key]==webhook_param[key]:
                    pass
                else:
                    result_msg = key+' not match'
                    logger.info(transaction_id + ':' + result_msg)
                    modify_data(create_insert_sql(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type))
                    return transaction_id+':'+result_msg
        else:
            result_msg = key + ' not in webhook'
            logger.info(transaction_id + ':' + result_msg)
            modify_data(create_insert_sql(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type))
            return transaction_id+':'+result_msg

    if str(ip) == '123.57.146.46' or str(ip) == '182.92.114.175' or str(
            ip) == '123.57.81.91':
        # 判断两个sign是否一致
        if bc_sign == signature:
            logger.info('%s webhook success' % transaction_id)
            result_msg = "success"
            modify_data(create_insert_sql(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type))
            return result_msg
        else:
            logger.info("%s signature not match" % transaction_id)
            result_msg = "signature not match"
            modify_data(create_insert_sql(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type))
            return result_msg
    else:
        result_msg = 'ip is not from beecloud,ip is:' + ip
        logger.info(transaction_id + ':' + result_msg)
        print ("transaction_id:%s"%transaction_id)
        print ("bill_id:%s"%bill_id)
        print ("result_msg:%s"%result_msg)
        # print ('insert_sql:%s'%insert_sql)
        modify_data(create_insert_sql(transaction_id,bill_id,result_msg,ip,createdAt,refund_no,transaction_type))
        return result_msg

#
#
# app_id = 'afae2a33-c9cb-4139-88c9-af5c1df472e1'
# app_secret = 'fc8865bb-9dca-454e-ba8e-0d8ed6cc83a2'
# tt=int(time.time())*1000
# sign = sign_md5(app_id+str(tt)+app_secret)
# bill_param = {
#     'app_id': app_id,
#     'timestamp': tt,
#     'app_sign':sign,
#     'bill_no':'bike1517276394000'
#    }
# resp = query_bill(bill_param)
# print resp