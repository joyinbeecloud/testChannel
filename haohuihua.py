# encoding: utf-8
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template,session
import json
from common_func import sign_md5,get_app
haohuihua_view = Blueprint('haohuihua', __name__)




@haohuihua_view.route('')
def user_info():
    user_id = request.args.get('user_id')

    app_id = request.args.get('app_id')
    timestamp = request.args.get('timestamp')
    mch_account = request.args.get('mch_account')
    app_sign = request.args.get('app_sign')
    #get app_secret from bc
    if app_id!=None:
        app_info = get_app(app_id)
        app_secret = app_info['app_secret']
        sign=sign_md5(app_id+str(timestamp)+app_secret)



    users={'cmf1':{'user_id':'cmf1',
                   'id_no':'111',
                   'name':'ccc',
                   'mobile':'123',
                   'card_no':'111',
                   'bank_name':u'中国银行',
                   'bank_branch_name':u'独墅湖支行',
                   'bank_no':'222',
                   'credit_score':6,
                   'register_time':1497254157000,
                   'province':u'江苏省',
                   'city':u'苏州市',
                   'address':'aaaa'
                   },
           'cmf2':{'user_id':'cmf2',
                   'id_no':'111',
                   'name':'ccc',
                   'mobile':'123',
                   'card_no':'111',
                   'bank_name':u'中国银行',
                   'bank_branch_name':u'独墅湖支行',
                   'bank_no':'222',
                   'credit_score':5,
                   'register_time':1497254157000,
                   'province':u'江苏省',
                   'city':u'苏州市',
                   'address':'aaaa'
                  },
           'lzw':{'user_id':'lzw',
                   'id_no':'500224198604064619',
                   'name':u'李志伟',
                   'mobile':'18094705373',
                   'card_no':'6214855710163144',
                   'bank_name':u'招商银行',
                   'bank_branch_name':u'招商银行杭州庆春支行',
                   'bank_no':'222',
                   'credit_score':1,
                   'register_time':1497254157000,
                   'province':u'江苏省',
                   'city':u'苏州市',
                   'address':u'国家大学纳米科技园'

           },
           'cmf':{
               'user_id': 'cmf',
               'id_no': '330682198904063427',
               'name': u'陈梦飞',
               'mobile': '13575765971',
               'card_no': '6222600170004441589',
               'bank_name': u'交通银行',
               'bank_branch_name': u'交通银行',
               'bank_no': '222',
               'credit_score': 10,
               'register_time': 1497254157000,
               'province': u'江苏省',
               'city': u'苏州市',
               'address': u'国家大学纳米科技园'
           },
           'gjf':{
               'user_id': 'gjf',
               'id_no': '230826198601240832',
               'name': u'高健峰',
               'mobile': '18136950721',
               'card_no': '6217856101009660486',
               'bank_name': u'中国银行',
               'bank_branch_name': u'交通银行',
               'bank_no': '222',
               'credit_score': 1,
               'register_time': 1507254157000,
               'province': u'江苏省',
               'city': u'苏州市',
               'address': u'国家大学纳米科技园'
           },
           'hjx': {
               'user_id': 'hjx',
               'id_no': '420281198606113434',
               'name': u'黄君贤',
               'mobile': '18501501060',
               'card_no': '6217856101012201385',
               'bank_name': u'中国银行',
               'bank_branch_name': u'中国银行独墅湖支行',
               'bank_no': '222',
               'credit_score': 6,
               'register_time': 1477254157000,
               'province': u'湖北省',
               'city': u'黄石',
               'address': u'黄石中学旁'
           },
           'qzh': {
               'user_id': 'qzh',
               'id_no': '320525199007133018',
               'name': u'钱志浩',
               'mobile': '18652420434',
               'card_no': '370285001914760',
               'bank_name': u'招商银行',
               'bank_branch_name': u'招商银行独墅湖支行',
               'bank_no': '222',
               'credit_score': 9,
               'register_time': 1497254157000,
               'province': u'江苏省',
               'city': u'苏州市',
               'address': u'吴江'
           },
           'yy': {
               'user_id': 'yy',
               'id_no': '321323198803100228',
               'name': u'俞艳',
               'mobile': '18550047310',
               'card_no': '6217906101008246428',
               'bank_name': u'中国银行',
               'bank_branch_name': u'招商银行独墅湖支行',
               'bank_no': '222',
               'credit_score': 9,
               'register_time': 1497254157000,
               'province': u'江苏省',
               'city': u'苏州市',
               'address': u'吴江'
           },
           }
    res={
        'result_code':'1',
        'err_detail':'user not exist',
        'result_msg':'user not exist',
        'user_info':''
    }
    # json.dumps(query_bill_para, encoding='utf-8',
    #            ensure_ascii=False)

    if users.has_key(user_id):
        res['result_code']='0'
        res['err_detail']='OK'
        res['result_msg']='0'
        res['user_info']=users[user_id]
        print res
        return json.dumps(res,encoding='utf-8',ensure_ascii=False)
    else:
        return json.dumps(res)
    # return render_template('show_url.html', result=users[user_id])
@haohuihua_view.route('/trade')
def trade():
    user_id = request.args.get('user_id')

    trades={'cmf1':[{'trade_no':'1111',
                     'trade_type':0,
                     'trade_fee':1,
                     'trade_time':1497254157000,
                     'success_time':1497254167000,
                     'bc_trade_no':'1111',
                     'trade_result':-1,
                     'card_no':'11111'
                     },
                    {'trade_no': '1122',
                     'trade_type': 0,
                     'trade_fee': 1,
                     'trade_time': 1497254167000,
                     'success_time': 1497254177000,
                     'bc_trade_no': '1122',
                     'trade_result': 1,
                     'card_no': '111113'
                     },
                    ],
            'yy': [{'trade_no': '1111',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254157000,
                      'success_time': 1497254167000,
                      'bc_trade_no': '1111',
                      'trade_result': -1,
                      'card_no': '11111'
                      },
                     {'trade_no': '1122',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254167000,
                      'success_time': 1497254177000,
                      'bc_trade_no': '1122',
                      'trade_result': 1,
                      'card_no': '111113'
                      },
                     ],
            'gjf': [{'trade_no': '1111',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254157000,
                      'success_time': 1497254167000,
                      'bc_trade_no': '1111',
                      'trade_result': -1,
                      'card_no': '11111'
                      },
                     {'trade_no': '1122',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254167000,
                      'success_time': 1497254177000,
                      'bc_trade_no': '1122',
                      'trade_result': 1,
                      'card_no': '111113'
                      },
                     ],
            'cmf': [{'trade_no': '1111',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254157000,
                      'success_time': 1497254167000,
                      'bc_trade_no': '1111',
                      'trade_result': -1,
                      'card_no': '11111'
                      },
                     {'trade_no': '1122',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254167000,
                      'success_time': 1497254177000,
                      'bc_trade_no': '1122',
                      'trade_result': 1,
                      'card_no': '111113'
                      },
                     ],
            'cmf2':[{'trade_no':'1134',
                     'trade_type':0,
                     'trade_fee':1,
                     'trade_time':1497254187000,
                     'success_time':1497254267000,
                     'bc_trade_no':'1114',
                     'trade_result':1,
                     'card_no':'111344'
                     }],
            'lzw':[{'trade_no':'1134345',
                     'trade_type':0,
                     'trade_fee':1,
                     'trade_time':1497254189000,
                     'success_time':1497254297000,
                     'bc_trade_no':'1114',
                     'trade_result':1,
                     'card_no':'1113443333'
            }],
            'hjx': [{'trade_no': '1134345',
                     'trade_type': 0,
                     'trade_fee': 1,
                     'trade_time': 1497254189000,
                     'success_time': 1497254297000,
                     'bc_trade_no': '1114',
                     'trade_result': 1,
                     'card_no': '1113443333'
                     }],
            'qzh': [{'trade_no': '1111',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254157000,
                      'success_time': 1497254167000,
                      'bc_trade_no': '1111',
                      'trade_result': -1,
                      'card_no': '11111'
                      },
                     {'trade_no': '1122',
                      'trade_type': 0,
                      'trade_fee': 1,
                      'trade_time': 1497254167000,
                      'success_time': 1497254177000,
                      'bc_trade_no': '1122',
                      'trade_result': 1,
                      'card_no': '111113'
                      }],
            }

    res_trade = {
        'result_code': '1',
        'err_detail': 'user not exist',
        'result_msg': 'user not exist',
        'trade': ''
    }
    if trades.has_key(user_id):
        trade={}

        res_trade['result_code'] = '0'
        res_trade['err_detail'] = 'OK'
        res_trade['result_msg'] = '0'
        res_trade['trade'] = trades[user_id]

        return json.dumps(res_trade,encoding='utf-8',ensure_ascii=False)
    else:
        return json.dumps(res_trade)




