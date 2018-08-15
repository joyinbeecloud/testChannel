# encoding: utf-8
from flask import Blueprint
from flask import Flask, request, redirect, render_template,Markup
import json
from common_func import *
from datetime import datetime,date
import MySQLdb,time,traceback

private_webhook_view = Blueprint('private_webhook', __name__)


def get_app_info(app_id):
    query_sql = "select * from app WHERE app_id='%s'" % app_id
    app_infos = private_query_data(query_sql)
    apps={}
    if app_infos !=():
        for app_info in app_infos:
            apps={'app_id':app_info[0],'user_id':app_info[1],'app_avatar':app_info[2],
                  'app_secret':app_info[3],'master_secret':app_info[5],'app_name':app_info[6],
                  }
        return apps
    else:
        logger.info("查询的app_id是:%r,查询结果是%r" % (app_id, app_infos))
        return apps

##支付订单，bill_id传bill_id;退款订单，bill_id传refund_id
def get_bill_info(bill_id,trasaction_type='PAY'):
    if trasaction_type=='PAY':
        query_sql = "select total_fee,bill_no,channel,optional,sub_channel from bill WHERE bill_id='%s'" % bill_id
    elif trasaction_type =='REFUND':
        query_sql = "select refund_fee,refund_no,channel,optional,sub_channel from bill WHERE bill_id='%s'" % bill_id

    bill_infos = private_query_data(query_sql)
    bill_param={}
    if bill_infos != ():
        for bill_info in bill_infos:
            bill_param={"transaction_fee": bill_info[0], 'bill_no':bill_info[1],
                        "channel_type": bill_info[2],"optional": bill_info[3],
                        "sub_channel_type": bill_info[4]}
        return bill_param
    else:
        logger.info("查询的bill_id是:%r,查询结果是%r"%(bill_id, bill_infos))
        return bill_param



# get_bill_info(11945332130393702)

# get_app_info('beacfdf5-badd-4a11-9b23-9ef3801732d4')



@private_webhook_view.route('/verify',methods=['POST'])
def private_webhook():
    # app_info = get_app_info()
    data = request.get_data()
    # logger.info('private recieve data:%s' % json.dumps(data, encoding='utf-8', ensure_ascii=False))
    bill_query_param = {}
    webhook_param = {}
    bill_param = {}
    bill_webhook_verify = 0
    signature = '0'
    bc_sign = '1'
    Is_bill_id_match = 0
    tt = int(time.time()) * 1000
    ip = request.remote_addr
    refund_bill_no = ''
    createdAt = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    webhook_data = request.get_json()
    try:
        json_data = request.get_json()
        logger.info('private recieve webhook:%s' % json.dumps(json_data, encoding='utf-8', ensure_ascii=False))
        webhook_signature = json_data['signature']
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
        webhook_param = {"transaction_fee": transaction_fee, "channel_type": channel_type,
                         'bill_no':transaction_id,
                         "optional": optional, "sub_channel_type": sub_channel_type,
                         }

    except Exception, e:
        logger.info(traceback.print_exc(e))
        return '获取webhook内容异常'
    if trade_success!=True:
        logger.info(transaction_id+':trade_success is not true,trade_success is '+trade_success)
        return 'trade_success is not true,trade_success is '+trade_success
    aa={}
    if type(message_detail)!=type(aa):
        logger.info(transaction_id+':message_detail is not a dict,message_detail is %r' %message_detail)
        return transaction_id+':message_detail is not a dict'

    if app_id != None:
        resp_dict = get_app_info(app_id)
        if resp_dict=={}:
            result_msg=' query app info is empty'
            logger.info(app_id+result_msg)
            return app_id+result_msg
        app_master_secret = resp_dict['master_secret']
        app_secret = resp_dict['app_secret']
        signature = sign_md5(app_id + transaction_id + transaction_type + channel_type + str(
            transaction_fee) + app_master_secret)
    else:
        logger.info("%s app_id is None" % transaction_id)
        return "app_id is None"

    if webhook_bill_id != None:

        bill_content=get_bill_info(webhook_bill_id,transaction_type)
        bill_param=bill_content
        if bill_param == {}:
            result_msg = ', bill query is empty'
            logger.info('bill_id is:'+str(webhook_bill_id)+result_msg)
            return 'bill_id is:'+str(webhook_bill_id) + result_msg
    else:
        logger.info('webhook_bill_id is none')
        return 'webhook_bill_id is none'

    # 订单表内容和webhook内容做比较
    for key in bill_param:
        if key in webhook_param:
            if key == 'optional':
                # print bill_param[key]
                if bill_param[key]=='':
                    bill_param[key]='{}'
                bill_optional1 = json.loads(bill_param[key])

                IS_optional_match = cmp(bill_optional1, webhook_param[key])
                if IS_optional_match == 0:
                    pass
                else:
                    result_msg = key + ' not match'
                    logger.info(transaction_id + ':' + result_msg)
                    return transaction_id + ':' + result_msg
            else:
                if bill_param[key] == webhook_param[key]:
                    pass
                else:
                    result_msg = key + ' not match'
                    logger.info(transaction_id + ':' + result_msg)
                    return transaction_id + ':' + result_msg
        else:
            result_msg = key + ' not in webhook'
            logger.info(transaction_id + ':' + result_msg)
            return transaction_id + ':' + result_msg
    if bc_sign == signature:
        logger.info('%s webhook success,send_host:%s' % (transaction_id,str(ip)))
        result_msg = "success"
        return result_msg
    else:
        logger.info("%s signature not match" % transaction_id)
        result_msg = "signature not match"
        return result_msg










