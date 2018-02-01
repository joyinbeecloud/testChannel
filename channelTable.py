# encoding: utf-8
from flask import Blueprint
from flask import Flask, request, redirect, render_template,Markup
import json
from common_func import *
from datetime import datetime,date
import time

channelTable_view = Blueprint('channelTable', __name__)

def query_data():
    db_resp = connect_db()
    db=db_resp['db']
    cursor = db_resp['cursor']
    query_sql="select * from channelsInfo"
    cursor.execute(query_sql)
    channels = cursor.fetchall()
    db.commit()
    db.close()
    return channels


def change_str_to_Bool(v):
    if v=="true":
        return 1
    else:
        return 0

@channelTable_view.route('')
def table_show():
    table_content = []
    table_dict = {}
    channels = query_data()
    # for channel in channels:
    #     print channel
    for channel in channels:
        table_dict = {'isBill': channel[0], 'id': channel[2],
                      'channel': channel[4], 'isTransfer': channel[5],
                      'channelSourceNumber': channel[6],
                      'channelSourceName': channel[7],'developer': channel[8],
                      'isLive': channel[9],'limit_amount':channel[10],
                      'jsbutton': channel[11],'isVerify':channel[12],
                      'cost': channel[13],'isRefund': channel[14],
                      'note': channel[15],
                       }
        table_content.append(table_dict)
    print table_content
    return render_template('channelTable.html', table=table_content)

@channelTable_view.route('/modify_channels_Info')
def save_channels_info():
    id=request.args.get('id')
    channel=request.args.get('channel')
    channelSourceName=request.args.get('channelSourceName')
    channelSourceNumber=request.args.get('channelSourceNumber')
    cost=request.args.get('cost')
    developer=request.args.get('developer')
    isBill=change_str_to_Bool(request.args.get('isBill'))
    isLive=change_str_to_Bool(request.args.get('isLive'))
    print isLive
    isRefund=change_str_to_Bool(request.args.get('isRefund'))
    isTransfer=change_str_to_Bool(request.args.get('isTransfer'))
    isVerify=change_str_to_Bool(request.args.get('isVerify'))
    jsbutton=change_str_to_Bool(request.args.get('jsbutton'))
    note=request.args.get('note')
    updatedAt = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    modify_sql = "UPDATE channelsInfo SET channel='%s',channelSourceName='%s',channelSourceNumber='%s'," \
                 "cost='%s',developer='%s',isBill='%s',isLive='%s',isRefund='%s',isTransfer='%s'," \
                 "isVerify='%s',jsbutton='%s',note='%s',updatedAt = '%s' WHERE id = '%s'"\
                 % (channel,channelSourceName,channelSourceNumber,cost,developer,isBill,isLive,isRefund,
                    isTransfer,isVerify,jsbutton,note,updatedAt,id)
    modify_result=modify_data(modify_sql)
    if modify_result==1:
        resp={'result_code':0,'msg':'修改成功'}
    # return 1
    else:
        resp = {'result_code': 1, 'msg': '修改失败'}
    return json.dumps(resp)

@channelTable_view.route('/create_channel')
def create_channel():
    limit_amount = request.args.get('limit_amount')
    channel = request.args.get('channel')
    channelSourceName = request.args.get('channelSourceName')
    channelSourceNumber = request.args.get('channelSourceNumber')
    cost = request.args.get('cost')
    developer = request.args.get('developer')
    isBill = change_str_to_Bool(request.args.get('isBill'))
    isLive = change_str_to_Bool(request.args.get('isLive'))
    print isLive
    isRefund = change_str_to_Bool(request.args.get('isRefund'))
    isTransfer = change_str_to_Bool(request.args.get('isTransfer'))
    isVerify = change_str_to_Bool(request.args.get('isVerify'))
    jsbutton = change_str_to_Bool(request.args.get('jsbutton'))
    note = request.args.get('note')
    updatedAt=str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    finishTime = request.args.get('datetimepicker')
    createdAt = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    insert_sql = "INSERT INTO channelsInfo(limit_amount,isBill,jsbutton,channelSourceNumber,isVerify,channelSourceName,isLive,cost,channel,isRefund,note,isTransfer,finishTime,developer,updatedAt,createdAt) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
    limit_amount, isBill, jsbutton, channelSourceNumber, isVerify, channelSourceName, isLive, cost, channel, isRefund, note,
    isTransfer, finishTime, developer, updatedAt, createdAt)
    modify_result = modify_data(insert_sql)
    if modify_result == 1:
        resp = {'result_code': 0, 'msg': '创建成功'}
    else:
        resp = {'result_code': 1, 'msg': '修改失败'}
    # return 1
    return json.dumps(resp)


