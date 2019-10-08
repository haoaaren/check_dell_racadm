#coding:utf-8
from flask import request,render_template, redirect,session
from . import app
from dbutil import DB
from collections import OrderedDict
import json
import datetime
from dell_racadm import check_client_ip,check_dell_racadm_Physical_disk_format,achieve_disk_reportsclass_table_value,check_dell_racadm_Physical_disk_state,disk_achieve_disk_warning_value


# 获取各个服务器磁盘详细信息
@app.route('/get_dell_racadm_info', methods=["GET"])
def get_dell_racadm_info():
    if not session.get('username',None):
        return redirect("/login")
    info_fields = [ 'id','ip_addr' ]
    tmp_1 = DB().get_list('monitored_ipaddr',info_fields)
    if tmp_1:
        tmp_2 = []
        for i in tmp_1:
            tmp_fields = ['disk_info','check_time']
            tmp_where = { 'ip_addr_id':i['id'] }
            tmp_3=DB().get_one('disk_info',tmp_fields,tmp_where)
            if tmp_3:
                tmp_4=check_dell_racadm_Physical_disk_format(tmp_3['disk_info'],i['ip_addr'],tmp_3['check_time'])
                if tmp_4:
                    # tmp_5 = []
                    tmp_6 = achieve_disk_reportsclass_table_value('get_dell_racadm_info')
                    if tmp_6 != 'no':
                        for tmp_7 in tmp_4:
                            tmp_8 = OrderedDict()
                            for tmp_9 in tmp_6.split(','):
                                tmp_10 = check_dell_racadm_Physical_disk_state(tmp_9)
                                try:
                                    tmp_8[tmp_10] = tmp_7[tmp_9]
                                except:
                                    tmp_8[tmp_10] = ''
                            tmp_2.append(tmp_8)
                           # tmp_5.append(tmp_8)
                   #  tmp_2.append(tmp_5)
        #return json.dumps(tmp_2, ensure_ascii=False)
        return render_template('check_disk/select_dell_racadm_disk_info.html',info=session,names=tmp_2)
    return '1'

# 获取各个服务器磁盘状态信息
@app.route('/get_dell_racadm_disk_status_page')
def get_dell_racadm_disk_status_page():
    if not session.get('username',None):
        return redirect("/login")
    info_fields = [ 'id','ip_addr' ]
    tmp_1 = DB().get_list('monitored_ipaddr',info_fields)
    if tmp_1:
        tmp_2 = []
        for i in tmp_1:
            tmp_fields = ['disk_name','ip_addr_id']
            tmp_where = { 'ip_addr_id':i['id'] }
            tmp_3=DB().get_list_where('disk_status_info',tmp_fields,tmp_where)
            if tmp_3:
                # 对列表里的字典 去重
                run_function = lambda x, y: x if y in x else x + [y]
                for x in reduce(run_function, [[], ] + tmp_3):
                    tmp_4=OrderedDict()
                    tmp_1_fields = ['disk_state_key','disk_state_value']
                    tmp_5 = DB().get_list_where('disk_status_info',tmp_1_fields,x)
                    tmp_4['ip_addr'] = i['ip_addr']
                    tmp_4['disk_name'] = x['disk_name']
                    for tmp_6 in tmp_5:
                        tmp_7=disk_achieve_disk_warning_value(tmp_6['disk_state_key'])
                        if tmp_7 == 'no':
                            tmp_4[tmp_6['disk_state_key']] = tmp_6['disk_state_value']
                        else:
                            if tmp_7['warning_value'] == tmp_6['disk_state_value']:
                                tmp_4[tmp_6['disk_state_key']] = tmp_6['disk_state_value']
                            else:
                                tmp_4[tmp_6['disk_state_key']] = '===='
                            
                    tmp_2.append(tmp_4)
        return render_template('check_disk/select_dell_racadm_disk_status_page.html',info=session,names=tmp_2)
    return '33'





