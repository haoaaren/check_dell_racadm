#coding:utf-8
from flask import request,render_template, redirect,session
from . import app
from dbutil import DB
from collections import OrderedDict
import json
import datetime
from dell_racadm import check_client_ip,achieve_disk_reportsclass_table_value,check_dell_racadm_info,achieve_dell_cacadm_comman,check_dell_racadm_Physical_disk_format,check_dell_racadm_System_format


# 更改各个服务器磁盘旧状态信息
@app.route('/racadm_disk_change_old', methods=["GET"])
def racadm_disk_change_old():
    # 默认认为时间相差为一个小时 3600秒
    difference_time = 3600 
    if request.method == "GET":
        client_ip = request.remote_addr
        if check_client_ip(client_ip) == 'no':
            # IP地址没在白名单 禁止访问
            return '01'
        # 当前时间
        now_time_tmp = datetime.datetime.now()
        tmp_fields = ['disk_name','ip_addr_id','disk_state_key','disk_state_value']
        tmp_where = { 'disk_state_key':'check_time' }
        tmp_1=DB().get_list_where('disk_status_info',tmp_fields,tmp_where)
        for tmp_2 in tmp_1:
            if tmp_2['disk_state_value'] != '====':
                tmp_3=datetime.datetime.strptime(tmp_2['disk_state_value'], '%Y-%m-%d %H:%M:%S')
            else:
                continue
            tmp_4 = now_time_tmp - tmp_3
            if tmp_4.seconds > difference_time:
                need_state = achieve_disk_reportsclass_table_value('save_status_data_need')
                if need_state == 'no':
                    info_data_where = {'ip_addr_id':tmp_2['ip_addr_id'],'disk_name':tmp_2['disk_name']}
                    DB().delete('disk_status_info',info_data_where)
                else:
                    status_insert_data = {}
                    for tmp_5 in need_state.split(','):
                        if tmp_5 == 'check_time':
                            continue
                        if tmp_2['disk_state_value'] == '====':
                            continue
                        status_insert_data['disk_state_value'] = '===='
                    tmp_where_1={'disk_name':tmp_2['disk_name'],'ip_addr_id':tmp_2['ip_addr_id']}
                    DB().update_where('disk_status_info',status_insert_data,tmp_where_1)
                    status_insert_data = {'disk_state_value': tmp_2['disk_state_value'] }
                    tmp_where_1={'disk_name':tmp_2['disk_name'],'ip_addr_id':tmp_2['ip_addr_id'],'disk_state_key':tmp_2['disk_state_key']}
                    DB().update_where('disk_status_info',status_insert_data,tmp_where_1)
        return 'ok'

# 测试远程管理卡----磁盘
@app.route('/get_dell_racadm_disk_test', methods=["GET"])
def get_dell_racadm_disk_test():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        IP_addr=request.args.get("IP_addr")
        IP_user=request.args.get("IP_user")
        IP_password=request.args.get("IP_password")
        if IP_addr and IP_user and IP_password:
            tmp_0 = achieve_dell_cacadm_comman('achieve_disk')
            tmp_1 = check_dell_racadm_info(IP_addr,IP_user,IP_password,tmp_0)
            if tmp_1 == 'no':
                return render_template('check_disk/dell_racadm_disk_test.html',info=session,names='3',IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password)
            check_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tmp_2=check_dell_racadm_Physical_disk_format(tmp_1,IP_addr,check_time)
            if tmp_2 == 'no':
                return render_template('check_disk/dell_racadm_disk_test.html',info=session,names='4',IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password)
            return json.dumps(tmp_2, ensure_ascii=False)
        elif IP_addr is None  and IP_user is None and IP_password is None:
            return render_template('check_disk/dell_racadm_disk_test.html',info=session,IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password,names='')
        else:
            return render_template('check_disk/dell_racadm_disk_test.html',info=session,IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password,names='5')
        return '3'
    return redirect("/")

# 测试远程管理卡----服务器型号 服务标签 快速服务代码 操作系统 电源状态 网卡等等
@app.route('/get_dell_racadm_system_test', methods=["GET"])
def get_dell_racadm_system_test():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        IP_addr=request.args.get("IP_addr")
        IP_user=request.args.get("IP_user")
        IP_password=request.args.get("IP_password")
        if IP_addr and IP_user and IP_password:
            tmp_0 = achieve_dell_cacadm_comman('achieve_NIC_and_System')
            tmp_1 = check_dell_racadm_info(IP_addr,IP_user,IP_password,tmp_0)
            if tmp_1 == 'no':
                return render_template('check_disk/get_dell_racadm_system_test.html',info=session,names='3',IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password)
            check_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tmp_2=check_dell_racadm_System_format(tmp_1,IP_addr,check_time)
            if tmp_2 == 'no':
                return render_template('check_disk/get_dell_racadm_system_test.html',info=session,names='4',IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password)
            return json.dumps(tmp_2, ensure_ascii=False)
        elif IP_addr is None  and IP_user is None and IP_password is None:
            return render_template('check_disk/get_dell_racadm_system_test.html',info=session,IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password,names='')
        else:
            return render_template('check_disk/get_dell_racadm_system_test.html',info=session,IP_addr=IP_addr,IP_user=IP_user,IP_password=IP_password,names='5')
        return '3'
    return redirect("/")

