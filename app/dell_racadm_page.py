#coding:utf-8
from flask import request,render_template, redirect,session
from . import app
from dbutil import DB
from collections import OrderedDict
import json
import datetime
from dell_racadm import check_client_ip,achieve_disk_reportsclass_table_value

# system_info相关
from dell_racadm import achieve_System_info,achieve_system_info_state_value,sytem_page_info_format,achieve_NIC_info,Nic_page_info_format

# Memory 相关
from dell_racadm import achieve_Memory_page_info,Memory_page_info_format,Memory_status_page_info_format,achieve_Memory_status_page_info

# CPU 相关
from dell_racadm import achieve_Cpu_status_page_info,achieve_Cpu_page_info,Cpu_page_info_format

# 传感器相关
from dell_racadm import sensor_status_page_info_format
# 风扇
from dell_racadm import achieve_Fan_status_page_info
# 温度
from dell_racadm import achieve_Temp_status_page_info
# 电源
from dell_racadm import achieve_Power_status_page_info
# 电池
from dell_racadm import achieve_Battery_status_page_info

# 页面页

# 系统信息
# 展示 服务器型号 服务标签 快速服务代码 操作系统 电源状态 
@app.route('/racadm_sytem_page', methods=["GET"])
def racadm_sytem_page():
    # 默认认为时间相差为一个小时 3600秒
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('System_info_page')
        if need_state != 'no':
            tmp_2=achieve_System_info(need_state)
            if tmp_2 != 'no':
                tmp_3=sytem_page_info_format(tmp_2,need_state)
                if tmp_3 != 'no':
                    return render_template('sytem_page/select_Sytem_info.html',info=session,names=tmp_3)
        tmp_3='Default_space'
        return render_template('sytem_page/select_Sytem_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    else:
        return 'no'

# 展示网卡
@app.route('/racadm_NIC_info_page', methods=["GET"])
def racadm_NIC_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('NIC_state')
        if need_state != 'no':
            tmp_2 = achieve_NIC_info(need_state)
            if tmp_2 != 'no':
                tmp_3=Nic_page_info_format(tmp_2,need_state)
                if tmp_3 != 'no':
                    return render_template('sytem_page/select_Nic_info.html',info=session,names=tmp_3)
        tmp_3='Default_space'
        return render_template('sytem_page/select_Nic_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    else:
        return 'no'

# 内存
# 信息
@app.route('/racadm_Memory_info_page', methods=["GET"])
def racadm_Memory_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Memory_info')
        if need_state != 'no':
            tmp_1 = achieve_Memory_page_info(need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Memory_info_page')
                tmp_3=Memory_page_info_format(tmp_1,need_state)
                if tmp_3 != 'no':
                    return render_template('Memory_page/select_Memory_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('Memory_page/select_Memory_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'

# 状态
@app.route('/racadm_Memory_status_info_page', methods=["GET"])
def racadm_Memory_status_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Memory_staus_info')
        if need_state != 'no':
            tmp_1 = achieve_Memory_status_page_info(need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Memory_status_info_need_ip')
                if need_state != 'no':
                    tmp_3=Memory_page_info_format(tmp_1,need_state)
                    if tmp_3 != 'no':
                        return render_template('Memory_page/select_Memory_status_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('Memory_page/select_Memory_status_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'

# CPU
# 信息
@app.route('/racadm_Cpu_info_page', methods=["GET"])
def racadm_Cpu_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Cpu_change_info')
        need_state_1 = achieve_disk_reportsclass_table_value('Cpu_info')
        if need_state != 'no' and need_state_1 != 'no':
            tmp_1 = achieve_Cpu_page_info(need_state_1,need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Cpu_info_need_ip')
                if need_state != 'no':
                    tmp_3=Cpu_page_info_format(tmp_1,need_state)
                    if tmp_3 != 'no':
                        return render_template('Cpu_page/select_Cpu_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('Cpu_page/select_Cpu_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'

# 状态
@app.route('/racadm_Cpu_status_info_page', methods=["GET"])
def racadm_Cpu_status_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Cpu_status_info')
        if need_state != 'no':
            tmp_1 = achieve_Cpu_status_page_info(need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Cpu_status_info_need_ip')
                if need_state != 'no':
                    tmp_3=Cpu_page_info_format(tmp_1,need_state)
                    if tmp_3 != 'no':
                        return render_template('Cpu_page/select_Cpu_status_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('Cpu_page/select_Cpu_status_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'



# 传感器
# 风扇
@app.route('/racadm_Fan_status_info_page', methods=["GET"])
def racadm_Fan_status_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Fan_status_info')
        if need_state != 'no':
            tmp_1 = achieve_Fan_status_page_info(need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Fan_status_info_need_ip')
                if need_state != 'no':
                    tmp_3=sensor_status_page_info_format(tmp_1,need_state)
                    if tmp_3 != 'no':
                        return render_template('sensor_page/select_Fan_status_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('sensor_page/select_Fan_status_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'

# 温度
@app.route('/racadm_Temp_status_info_page', methods=["GET"])
def racadm_Temp_status_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Temp_status_info')
        if need_state != 'no':
            tmp_1 = achieve_Temp_status_page_info(need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Temp_status_info_need_ip')
                if need_state != 'no':
                    tmp_3=sensor_status_page_info_format(tmp_1,need_state)
                    if tmp_3 != 'no':
                        return render_template('sensor_page/select_Temp_status_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('sensor_page/select_Temp_status_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'

# 电源
@app.route('/racadm_Power_status_info_page', methods=["GET"])
def racadm_Power_status_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Power_status_info')
        if need_state != 'no':
            tmp_1 = achieve_Power_status_page_info(need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Power_status_info_need_ip')
                if need_state != 'no':
                    tmp_3=sensor_status_page_info_format(tmp_1,need_state)
                    if tmp_3 != 'no':
                        return render_template('sensor_page/select_Power_status_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('sensor_page/select_Power_status_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'

# 电池
@app.route('/racadm_Battery_status_info_page', methods=["GET"])
def racadm_Battery_status_info_page():
    if not session.get('username',None):
        return redirect("/login")
    if request.method == "GET":
        need_state = achieve_disk_reportsclass_table_value('Battery_status_info')
        if need_state != 'no':
            tmp_1 = achieve_Battery_status_page_info(need_state)
            if tmp_1 != 'no':
                need_state = achieve_disk_reportsclass_table_value('Battery_status_info_need_ip')
                if need_state != 'no':
                    tmp_3=sensor_status_page_info_format(tmp_1,need_state)
                    if tmp_3 != 'no':
                        return render_template('sensor_page/select_Battery_status_info.html',info=session,names=tmp_3)
            tmp_3='Default_space'
            return render_template('sensor_page/select_Battery_status_info.html',info=session,names=tmp_3,need_state=need_state.split(','))
    return 'ERROR'








