#coding:utf-8
from flask import request,render_template, redirect,session
from . import app
from dbutil import DB
import hashlib
import config
import os
import sys
from collections import OrderedDict
import json
from utils import util
import datetime
import requests
import random
import re

################################ 获取基础信息相关
# 获取dell racadm command
def achieve_dell_cacadm_comman(command_name):
    fields = ['command_body']
    where = { 'command_name':command_name }
    tmp_1=DB().get_one('racadm_command',fields,where)
    if tmp_1:
        return tmp_1['command_body']
    else:
        return 'no'

# 查询获取的字段都是干什么的
def check_dell_racadm_Physical_disk_state(disk_state_name):
    fields = ["disk_state_name"]
    where = {'disk_state_key':disk_state_name}
    tmp_1=DB().get_one('disk_status_state',fields,where)
    if tmp_1:
        return tmp_1['disk_state_name']
    else:
        return disk_state_name

# 获取生成报表所需要的各种字段
def achieve_disk_reportsclass_table_value(reports_submit_name):
    fields = ["get_date_fields"]
    where = {'reports_submit':reports_submit_name}
    tmp_1 = DB().get_one('need_reportsclass',fields,where)
    if tmp_1:
        return tmp_1['get_date_fields']
    else:
        return 'no'

# 获取System info 生成页面所需要的各种字段
def achieve_system_info_state_value(reports_submit_name):
    fields = ["disk_state_name"]
    where = {'disk_state_key':reports_submit_name}
    tmp_1 = DB().get_one('System_AND_Nic_status_state',fields,where)
    if tmp_1:
        return tmp_1['disk_state_name']
    else:
        return 'no'

# 获取Memory info 生成页面所需要的各种字段
def achieve_Memory_info_state_value(reports_submit_name):
    fields = ["disk_state_name"]
    where = {'disk_state_key':reports_submit_name}
    tmp_1 = DB().get_one('Memory_status_state',fields,where)
    if tmp_1:
        return tmp_1['disk_state_name']
    else:
        return 'no'

# 获取 Sensor info 生成页面所需要的各种字段
def achieve_Sensor_status_info_state_value(reports_submit_name):
    fields = ["disk_state_name"]
    where = {'disk_state_key':reports_submit_name}
    tmp_1 = DB().get_one('sensor_status_state',fields,where)
    if tmp_1:
        return tmp_1['disk_state_name']
    else:
        return 'no'


################################ IP相关
# 检查IP是否存在，查询管理卡用户名密码
def check_dell_racadm_ip(client_ip,ip_addr):
    check_ip_fields = ["ip_addr"]
    check_ip_where = {'ip_addr':ip_addr}
    if DB().get_one('monitored_ipaddr',check_ip_fields,check_ip_where):
        return 'yes'
    else:
        util.WriteLog('ip_info').warn("Not allow ip_addr: %s from client_ip: %s"%(ip_addr,client_ip))
        return 'no'

# 返回所有IP地址：
def return_racadm_ip():
    check_ip_fields = ["ip_addr",'id']
    tmp_1=DB().get_list('monitored_ipaddr',check_ip_fields)
    if tmp_1:
        return  tmp_1
    else:
        return 'no'

# 根据id返回IP地址：
def use_id_return_racadm_ip(ip_addr_id):
    check_ip_fields = ["ip_addr"]
    check_ip_where = {'id':ip_addr_id}
    tmp_1=DB().get_one('monitored_ipaddr',check_ip_fields,check_ip_where)
    if tmp_1:
        return tmp_1['ip_addr']
    else:
        return 'no'

# 检测访问IP
def check_client_ip(ip_addr):
    fields = ["ip_user"]
    where = {'ip':ip_addr}
    tmp_1 = DB().get_one('check_client_ip',fields,where)
    if tmp_1:
        return tmp_1["ip_user"]
    else:
        return 'no'

# 检查IP是否存在，查询管理卡用户名密码
def dell_racadm_achieve_ip_info(client_ip,ip_addr):
    ip_fields = ["id","ip_addr","remote_card_id","card_type_name","card_user_name","card_user_passwd"]
    ip_where = {'ip_addr':ip_addr}
    ip_info=DB().get_one('monitored_ipaddr',ip_fields,ip_where)
    if ip_info:
        if ip_info['remote_card_id']:
            achieve_remote_card_info_fields = ["card_type_name",'card_user_name','card_user_passwd']
            achieve_remote_card_info_where = {'id':ip_info['remote_card_id']}
            achieve_remote_card_info = DB().get_one('remote_card_info',achieve_remote_card_info_fields,achieve_remote_card_info_where)
            if achieve_remote_card_info:
                if ip_info['card_type_name'] != '====':
                    achieve_remote_card_info['card_type_name'] = ip_info['card_type_name']
                if ip_info['card_user_name'] != '====':
                    achieve_remote_card_info['card_user_name'] = ip_info['card_user_name']
                if ip_info['card_user_passwd'] != '====':
                    achieve_remote_card_info['card_user_passwd'] = ip_info['card_user_passwd']
                achieve_remote_card_info['id'] = ip_info['id']
                return achieve_remote_card_info
            else:
                util.WriteLog('ip_info').warn("ip_info achieve error.Table remote_card_info remote_card_id  is none . ip_addr: %s from client_ip: %s remote_card_id: %s"%(ip_addr,client_ip,ip_info['remote_card_id']))
                return 'no'
        else:
            util.WriteLog('ip_info').warn("ip_info achieve error remote_card_id is none . ip_addr: %s from client_ip: %s"%(ip_addr,client_ip))
            return 'no'
    else:
        util.WriteLog('ip_info').warn("ip_info achieve error ip_addr: %s from client_ip: %s"%(ip_addr,client_ip))
        return 'no'


################################ 告警相关
# 发送钉钉告警
def send_ding_talk_warning(data):
    tmp_2=achieve_warning_toolkit_value('offline_ding_talk')
    if tmp_2 == 'no':
        return 'no'

    for i in data:
        program={
        "msgtype": "markdown",
        "markdown": {"title":"%s"%(i['title']),
        "text":"%s"%(i['text'])
            },
        "at": {
            "isAtAll": False 
            }
        }
        try:
            tmp_3=random.choice(tmp_2)
            url = '%s%s'%(tmp_3['toolkit_url'],tmp_3['toolkit_key'])
            headers={'Content-Type': 'application/json'}
            f=requests.post(url,data=json.dumps(program),headers=headers)
        except:
            util.WriteLog('send_ding_talk_warning').info("Execute '%s' error: %s" % (i,'False'))
    return 'ok'
    

# 获取告警所需要的key和url
def achieve_warning_toolkit_value(toolkit_name):
    fields = ['toolkit_url','toolkit_key']
    where = {'toolkit_name':toolkit_name}
    tmp_1=DB().get_list_where('warning_toolkit_table',fields,where)
    if tmp_1:
        return tmp_1
    else:
        return 'no'

# 检测告警字段 检测 更改
def disk_achieve_disk_warning_value(warning_field_key):
    fields = ['warning_field_key','warning_value','warning_change_value']
    where = {'warning_field_key':warning_field_key}
    tmp_1=DB().get_one('disk_warning_table',fields,where)
    if tmp_1:
        return tmp_1
    else:
        return 'no'

# 将所有告警规则返回
def disk_achieve_disk_warning_return():
    fields = ['warning_field_key','warning_value']
    tmp_1=DB().get_list('disk_warning_table',fields)
    if tmp_1:
        return tmp_1
    else:
        return 'no'

# 磁盘告警数据
def warning_toolkit_disk_date():
    tmp_fields = ['disk_name','ip_addr_id']
    tmp_where = { 'disk_state_value':'====' }
    tmp_1=DB().get_list_where('disk_status_info',tmp_fields,tmp_where)
    if not tmp_1:
        tmp_1=[]
    tmp_7=disk_achieve_disk_warning_return()
    if tmp_7 != 'no':
        for tmp_8 in tmp_7:
            tmp_fields_1 = ['disk_name','ip_addr_id']
            tmp_where_1= { 'disk_state_key':tmp_8['warning_field_key'] }
            tmp_where_2= { 'disk_state_value':tmp_8['warning_value'] }
            tmp_9=DB().get_list_where_and_not_where('disk_status_info',tmp_fields_1,tmp_where_1,tmp_where_2)
            if tmp_9:
                for tmp_4 in tmp_9:
                    tmp_1.append({'ip_addr_id':tmp_4['ip_addr_id'],'disk_name':tmp_4['disk_name']})
    # 对列表里的字典 去重
    run_function = lambda x, y: x if y in x else x + [y]
    tmp_2=reduce(run_function, [[], ] + tmp_1)
    tmp_5=[]
    for tmp_3 in tmp_2:
        tmp_5.append({'ip_addr':use_id_return_racadm_ip(tmp_3['ip_addr_id']),'disk_name':tmp_3['disk_name']})
    if tmp_5:
        return tmp_5
    else:
        return 'no'


################################ 基础连接相关
# 获取磁盘信息然后用racadm连接来获取信息
def check_dell_racadm_info(ip_addr,connect_user,connect_password,command_body):
    if command_body != 'no':
        result_version=os.popen(("timeout 60 racadm --nocertwarn -r %s -u %s -p %s %s"%(ip_addr,connect_user,connect_password,command_body))).read()
        if result_version:
            return result_version
        else:
            util.WriteLog('racadm_connect').warn("racadm connect error, maybe username or password is error . IP_addr:%s card_user_name:%s card_user_passwd:%s command body:%s"%(ip_addr,connect_user,connect_password,command_body))
    return 'no'


################################ 对信息格式化
# 网卡对传输过来的字段进行格式化输出
def check_dell_racadm_NIC_CARD_format(data,ip_addr,check_time):
    tmp_1=[]
    try:
        for i in data.split('===='):
            if i.startswith('NIC'):
                tmp_3 = OrderedDict()
                tmp_3['ip_addr'] = ip_addr
                tmp_3['check_time'] = check_time
                tmp_2 = i.split()
                tmp_3['NIC_name'],tmp_3['NIC_type'],tmp_3['NIC_MAC'] = tmp_2[0],tmp_2[1],tmp_2[3]
                tmp_1.append(tmp_3)
        if tmp_1:
            return tmp_1
        else:
            return 'no'
    except:
        return 'no'

# 磁盘对传输过来的字段进行格式化输出
def check_dell_racadm_Physical_disk_format(data,ip_addr,check_time):
    tmp_2 = []
    try:
        for i in data.replace("|Disk.", "====Disk.").split('===='):
            tmp_1 = OrderedDict()
            if i.startswith('Disk.'):
                tmp_1['ip_addr'] = ip_addr
                tmp_1['check_time'] = check_time
                for k in i.split('|'):
                    if '=' in k:
                        tmp_3,tmp_4 = k.split('=')[0].strip(),k.split('=')[1].strip()
                        tmp_1[tmp_3] = tmp_4.strip()
                    elif k:
                        tmp_1['disk_name'] = k
                tmp_2.append(tmp_1)
        if tmp_2:
            return tmp_2 
        else:
            return 'no'
    except:
        return 'no'

# System对传输过来的字段进行格式化输出
def check_dell_racadm_System_format(data,ip_addr,check_time,need_state='no'):
    tmp_1=[]
    try:
        if need_state == 'no':
            tmp_3 = OrderedDict()
            tmp_3['ip_addr'] = ip_addr
            tmp_3['check_time'] = check_time
            for k in data.split('===='):
                if '=' in k and not k.startswith('NIC'):
                    tmp_4,tmp_5 = k.split('=')[0].strip().replace(' ','_'),k.split('=')[1].strip()
                    tmp_3[tmp_4] = tmp_5
            tmp_1.append(tmp_3)
    
        else:
            tmp_3 = OrderedDict()
            tmp_3['ip_addr'] = ip_addr
            tmp_3['check_time'] = check_time
            for k in data.split('===='):
                if '=' in k and not k.startswith('NIC'):
                    tmp_4,tmp_5 = k.split('=')[0].strip().replace(' ','_'),k.split('=')[1].strip()
                    if tmp_4 in need_state.split(','):
                        tmp_3[tmp_4] = tmp_5
                        tmp_1.append(tmp_3)
            return tmp_3
    
        if tmp_1:
            return tmp_1
        else:
            return 'no'
    except:
        return 'no'

# 硬件资源 内存 信息 对传输过来的字段进行格式化输出
def check_dell_racadm_memory_info_format(data,ip_addr,check_time,ip_addr_id):
    tmp_3 = []
    try:
        for i in data.split('===='):
            tmp_1 = OrderedDict()
            tmp_1['ip_addr_id'] = ip_addr_id
            tmp_2=i.replace('#','')
            if '=' in i:
                tmp_1['disk_state_key'] = tmp_2.split('=')[0].strip().replace(' ','_')
                tmp_1['disk_state_value'] = tmp_2.split('=')[1].strip()
                tmp_3.append(tmp_1)
        tmp_1 = OrderedDict()
        tmp_1['ip_addr_id'] = ip_addr_id
        tmp_1['disk_state_key'],tmp_1['disk_state_value'] = 'check_time',check_time 
        tmp_3.append(tmp_1)
        if tmp_3:
            return tmp_3
        else:
            return 'no'
    except:
        return 'no'

# 硬件资源 CPU 信息 对传输过来的字段进行格式化输出
def check_dell_racadm_cpu_info_format(data,ip_addr,check_time,ip_addr_id):
    tmp_3 = []
    try:
        for i in data.split('===='):
            tmp_1 = OrderedDict()
            tmp_1['ip_addr_id'] = ip_addr_id
            tmp_2=i.replace('#','')
            if '=' in i:
                tmp_1['disk_state_key'] = tmp_2.split('=')[0].strip().replace(' ','_')
                tmp_1['disk_state_value'] = tmp_2.split('=')[1].strip()
                tmp_3.append(tmp_1)
            
        tmp_1 = OrderedDict()
        tmp_1['ip_addr_id'] = ip_addr_id
        tmp_1['disk_state_key'],tmp_1['disk_state_value'] = 'check_time',check_time 
        tmp_3.append(tmp_1)
        if tmp_3:
            return tmp_3
        else:
            return 'no'
    except:
        return 'no'

# 传感器 内存 信息 对传输过来的字段进行格式化输出
def check_dell_racadm_Sensor_memory_format(data,check_time,ip_addr_id):
    try:
        w1 = 'MEMORY'
        w2= 'BATTERY'
        pat = re.compile(w1+'(.*?)'+w2,re.S)
        result = pat.findall(data)
        tmp_0=[]
        for i in result[0].split('===='):
            tmp_2 = OrderedDict()
            if 'Sensor' not in i and 'DIMM' in i:
                tmp_1=i.strip().split()
                tmp_2['ip_addr_id'] = ip_addr_id
                tmp_2['check_time'] = check_time
                tmp_2['Sensor_Name'] = '%s_%s'%(tmp_1[0],tmp_1[1])
                tmp_2['Sensor_Status'] = tmp_1[2]
                tmp_2['Sensor_State'] = tmp_1[3]
                tmp_2['Sensor_lc'] = tmp_1[4]
                tmp_2['Sensor_uc'] = tmp_1[5]
                tmp_0.append(tmp_2)
        if tmp_0:
            return tmp_0
        else:
            return 'no'
    except:
        return 'no'

# 传感器 风扇 信息 对传输过来的字段进行格式化输出
def check_dell_racadm_Sensor_FAN_format(data,check_time,ip_addr_id):
    try:
        w1 = 'FAN'
        w2= 'VOLTAGE'
        pat = re.compile(w1+'(.*?)'+w2,re.S)
        result = pat.findall(data)
        tmp_0=[]
        for i in result[0].split('===='):
            tmp_2 = OrderedDict()
            if 'Sensor' not in i and 'System Board Fan' in i:
                tmp_1=i.strip().split()
                tmp_2['ip_addr_id'] = ip_addr_id
                tmp_2['check_time'] = check_time
                tmp_2['Sensor_Name'] = "_".join(tmp_1[0:-5])
                tmp_2['Sensor_Status'] = tmp_1[-5]
                tmp_2['Sensor_Reading'] = tmp_1[-4]
                tmp_2['Sensor_lc'] = tmp_1[-3]
                tmp_2['Sensor_uc'] = tmp_1[-2]
                tmp_2['Sensor_PWM'] = tmp_1[-1]
                tmp_0.append(tmp_2)
        if tmp_0:
            return tmp_0
        else:
            return 'no'
    except:
        return 'no'

# 传感器 CPU 信息 对传输过来的字段进行格式化输出
def check_dell_racadm_Sensor_CPU_format(data,check_time,ip_addr_id):
    try:
        w1 = 'PROCESSOR'
        w2= 'MEMORY'
        pat = re.compile(w1+'(.*?)'+w2,re.S)
        result = pat.findall(data)
        tmp_0=[]
        for i in result[0].split('===='):
            tmp_2 = OrderedDict()
            if 'Sensor' not in i and 'Status' in i:
                tmp_1=i.strip().split()
                tmp_2['ip_addr_id'] = ip_addr_id
                tmp_2['check_time'] = check_time
                tmp_2['Sensor_Name'] = tmp_1[0]
                tmp_2['Sensor_Status'] = tmp_1[2]
                tmp_2['Sensor_State'] = tmp_1[3]
                tmp_2['Sensor_lc'] = tmp_1[4]
                tmp_2['Sensor_uc'] = tmp_1[5]
                tmp_0.append(tmp_2)
        if tmp_0:
            return tmp_0
        else:
            return 'no'
    except:
        return 'no'

# 传感器 温度 信息 对传输过来的字段进行格式化输出
def check_dell_racadm_Sensor_TEMPERATURE_format(data,check_time,ip_addr_id):
    try:
        w1 = 'TEMPERATURE'
        w2= 'FAN'
        pat = re.compile(w1+'(.*?)'+w2,re.S)
        result = pat.findall(data)
        tmp_0=[]
        for i in result[0].split('===='):
            tmp_2 = OrderedDict()
            if 'Sensor' not in i and '[Key' not in i and 'Temp' in i:
                tmp_1=i.strip().split()
                tmp_2['ip_addr_id'] = ip_addr_id
                tmp_2['check_time'] = check_time
                tmp_2['Sensor_Name'] = "_".join(tmp_1[0:-8])
                tmp_2['Sensor_Status'] = tmp_1[-8]
                tmp_2['Sensor_Reading'] = tmp_1[-7]
                # 警告温度阈值 最小 最大
                tmp_2['Sensor_lnc'] = tmp_1[-4]
                tmp_2['Sensor_unc'] = tmp_1[-2]
                # 灾难温度阈值 最小 最大
                tmp_2['Sensor_lc'] = tmp_1[-6]
                tmp_2['Sensor_uc'] = tmp_1[-5]
                tmp_0.append(tmp_2)
    
        if tmp_0:
            return tmp_0
        else:
            return 'no'
    except:
        return 'no'

# 传感器 电源 状态信息 对传输过来的字段进行格式化输出
def check_dell_racadm_Sensor_POWER_format(data,check_time,ip_addr_id):
    try:
        w1 = 'POWER'
        w2= 'TEMPERATURE'
        pat = re.compile(w1+'(.*?)'+w2,re.S)
        result = pat.findall(data)
        tmp_0=[]
        for i in result[0].split('===='):
            tmp_2 = OrderedDict()
            if 'Sensor' not in i and 'Status' in i:
                tmp_1=i.strip().split()
                tmp_2['ip_addr_id'] = ip_addr_id
                tmp_2['check_time'] = check_time
                tmp_2['Sensor_Name'] = "_".join(tmp_1[0:-2])
                tmp_2['Sensor_Status'] = tmp_1[-2]
                tmp_2['Sensor_Type'] = tmp_1[-1]
                tmp_0.append(tmp_2)
    
        if tmp_0:
            return tmp_0
        else:
            return 'no'
    except:
        return 'no'

# 传感器 电池 状态信息 对传输过来的字段进行格式化输出
def check_dell_racadm_Sensor_BATTERY_format(data,check_time,ip_addr_id):
    try:
        w1 = 'BATTERY'
        w2= 'PERFORMANCE'
        pat = re.compile(w1+'(.*?)'+w2,re.S)
        result = pat.findall(data)
        tmp_0=[]
        for i in result[0].split('===='):
            tmp_2 = OrderedDict()
            if 'Sensor' not in i and 'Battery' in i:
                tmp_1=i.strip().split()
                tmp_2['ip_addr_id'] = ip_addr_id
                tmp_2['check_time'] = check_time
                tmp_2['Sensor_Name'] = "_".join(tmp_1[0:-4])
                tmp_2['Sensor_Status'] = tmp_1[-4]
                tmp_2['Sensor_Reading'] = tmp_1[-3]
                tmp_2['Sensor_lc'] = tmp_1[-2]
                tmp_2['Sensor_uc'] = tmp_1[-1]
                tmp_0.append(tmp_2)
    
        if tmp_0:
            return tmp_0
        else:
            return 'no'
    except:
        return 'no'

# racadm_sytem_page 输出字段中英转换
def sytem_page_info_format(data,need_state):
    tmp_1 = OrderedDict()
    for tmp_2 in need_state.split(','):
        tmp_3=achieve_system_info_state_value(tmp_2)
        if tmp_3 == 'no':
            tmp_1[tmp_2] = tmp_2
        else:
            tmp_1[tmp_2] = tmp_3
    tmp_2=[]
    for i in data:
        tmp_3 = OrderedDict()
        for tmp_4 in need_state.split(','):
            tmp_3[tmp_1[tmp_4]] = i[tmp_4]
        tmp_2.append(tmp_3)
    if tmp_2:
        return tmp_2
    else:
        return 'no'

# racadm_NIC_info_page 输出字段中英转换
def Nic_page_info_format(data,need_state):
    tmp_1 = OrderedDict()
    for tmp_2 in need_state.split(','):
        tmp_3=achieve_system_info_state_value(tmp_2)
        if tmp_3 == 'no':
            tmp_1[tmp_2] = tmp_2
        else:
            tmp_1[tmp_2] = tmp_3
    tmp_2=[]
    for i in data:
        tmp_3 = OrderedDict()
        for tmp_4 in need_state.split(','):
            tmp_3[tmp_1[tmp_4]] = i[tmp_4]
        tmp_2.append(tmp_3)
    if tmp_2:
        return tmp_2
    else:
        return 'no'

# racadm_Memory_info_page 输出字段中英转换
def Memory_page_info_format(data,need_state):
    tmp_1 = OrderedDict()
    for tmp_2 in need_state.split(','):
        tmp_3=achieve_Memory_info_state_value(tmp_2)
        if tmp_3 == 'no':
            tmp_1[tmp_2] = tmp_2
        else:
            tmp_1[tmp_2] = tmp_3
    tmp_2=[]
    for i in data:
        tmp_3 = OrderedDict()
        for tmp_4 in need_state.split(','):
            tmp_3[tmp_1[tmp_4]] = i[tmp_4]
        tmp_2.append(tmp_3)
    if tmp_2:
        return tmp_2
    else:
        return 'no'

# racadm_Memory_status_info_page 输出字段中英转换
def Memory_status_page_info_format(data,need_state):
    tmp_1 = OrderedDict()
    for tmp_2 in need_state.split(','):
        tmp_3=achieve_Memory_info_state_value(tmp_2)
        if tmp_3 == 'no':
            tmp_1[tmp_2] = tmp_2
        else:
            tmp_1[tmp_2] = tmp_3
    tmp_2=[]
    for i in data:
        tmp_3 = OrderedDict()
        for tmp_4 in need_state.split(','):
            tmp_3[tmp_1[tmp_4]] = i[tmp_4]
        tmp_2.append(tmp_3)
    if tmp_2:
        return tmp_2
    else:
        return 'no'

# racadm_Cpu_info_page 输出字段中英转换
def Cpu_page_info_format(data,need_state):
    tmp_1 = OrderedDict()
    for tmp_2 in need_state.split(','):
        tmp_3=achieve_Memory_info_state_value(tmp_2)
        if tmp_3 == 'no':
            tmp_1[tmp_2] = tmp_2
        else:
            tmp_1[tmp_2] = tmp_3
    tmp_2=[]
    for i in data:
        tmp_3 = OrderedDict()
        for tmp_4 in need_state.split(','):
            tmp_3[tmp_1[tmp_4]] = i[tmp_4]
        tmp_2.append(tmp_3)
    if tmp_2:
        return tmp_2
    else:
        return 'no'

# sensor_status 输出字段中英转换
def sensor_status_page_info_format(data,need_state):
    tmp_1 = OrderedDict()
    for tmp_2 in need_state.split(','):
        tmp_3=achieve_Sensor_status_info_state_value(tmp_2)
        if tmp_3 == 'no':
            tmp_1[tmp_2] = tmp_2
        else:
            tmp_1[tmp_2] = tmp_3
    tmp_2=[]
    for i in data:
        tmp_3 = OrderedDict()
        for tmp_4 in need_state.split(','):
            tmp_3[tmp_1[tmp_4]] = i[tmp_4]
        tmp_2.append(tmp_3)
    if tmp_2:
        return tmp_2
    else:
        return 'no'


################################ 保存信息
#传递参数 ip地址、ip id、info表的数据、status表的数据
def check_dell_racadm_Physical_disk_save(ip_addr,ip_addr_id,check_time,info_data='tianshi',status_data='tianshi',need_state='no'):
    if info_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('disk_info',info_data_where)
        info_insert_data={'ip_addr_id':ip_addr_id,'check_time':check_time,'disk_info':info_data}
        DB().create('disk_info',info_insert_data)

    
    if status_data == 'tianshi':
        return 'no'
    else:
        status_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('disk_status_info',status_data_where)
        if need_state == 'no':
            return 'no'
        else:
            need_state = need_state.split(',')
        for i in status_data:
            for k in need_state:
                status_insert_data = {}
                status_insert_data['ip_addr_id'] = ip_addr_id
                status_insert_data['disk_name'] = i['Name']
                tmp_1=check_dell_racadm_Physical_disk_state(k)
                if tmp_1:
                    status_insert_data['disk_state_key'] = tmp_1
                else:
                    status_insert_data['disk_state_key'] = k
                status_insert_data['disk_state_value'] = i[k]
                DB().create('disk_status_info',status_insert_data)
    return 'ok'

#传递参数 ip地址、ip id、info表的数据、status表的数据
def check_dell_racadm_System_Nic_info_save(ip_addr_id,Nic_data='tianshi',System_data='tianshi'):
    if Nic_data == 'tianshi' or System_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('System_info',info_data_where)
        DB().delete('NIC_info',info_data_where)
        for i in Nic_data:
            i['ip_addr_id']=ip_addr_id
            DB().create('NIC_info',i)
        System_data['ip_addr_id']=ip_addr_id
        DB().create('System_info',System_data)
    return 'ok'

# 硬件资源 内存 信息入库
def check_dell_racadm_memory_info_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('Memory_info',info_data_where)
        for i in Nic_data:
            DB().create('Memory_info',i)
    return 'ok'

# 硬件资源 CPU 信息入库
def check_dell_racadm_CPU_info_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('CPU_info',info_data_where)
        for i in Nic_data:
            DB().create('CPU_info',i)
    return 'ok'

# 硬件资源 内存 状态信息入库
def check_dell_racadm_Sensor_memory_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('Memory_status_info',info_data_where)
        for i in Nic_data:
            DB().create('Memory_status_info',i)
    return 'ok'

# 硬件资源 风扇 状态信息入库
def check_dell_racadm_Sensor_Fan_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('Fan_status_info',info_data_where)
        for i in Nic_data:
            DB().create('Fan_status_info',i)
    return 'ok'

# 硬件资源 CPU 状态信息入库
def check_dell_racadm_Sensor_CPU_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('CPU_status_info',info_data_where)
        for i in Nic_data:
            DB().create('CPU_status_info',i)
    return 'ok'

# 硬件资源 温度 传感器状态信息入库
def check_dell_racadm_Sensor_TEMPERATURE_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('Temp_status_info',info_data_where)
        for i in Nic_data:
            DB().create('Temp_status_info',i)
    return 'ok'

# 硬件资源 电源 传感器状态信息入库
def check_dell_racadm_Sensor_POWER_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('Power_status_info',info_data_where)
        for i in Nic_data:
            DB().create('Power_status_info',i)
    return 'ok'

# 硬件资源 电池 传感器状态信息入库
def check_dell_racadm_Sensor_BATTERY_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        info_data_where = {'ip_addr_id':ip_addr_id}
        DB().delete('Battery_status_info',info_data_where)
        for i in Nic_data:
            DB().create('Battery_status_info',i)
    return 'ok'

# 硬件信息 前面板 信息入库
def check_dell_racadm_System_LCD_CurrentDisplay_save(ip_addr_id,Nic_data='tianshi'):
    if Nic_data == 'tianshi':
        return 'no'
    else:
        
        where = {'ip_addr_id':ip_addr_id}
        fields = {'System_LCD_CurrentDisplay':Nic_data.split('=')[1]}
        DB().update_where('System_info',fields,where)
    return 'ok'


################################ 获取保存的信息
# 获取保存的 system 信息
def achieve_System_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        fields=[]
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('System_info',fields)
        if tmp_1:
            return tmp_1
        else:
            return 'no'

# 获取保存的 NIC 信息
def achieve_NIC_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        fields=[]
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('NIC_info',fields)
        if tmp_1:
            return tmp_1
        else:
            return 'no'

# 获取保存的 Memory 信息
def achieve_Memory_page_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('Memory_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)

        tmp_3=[]
        for i in tmp_2:
            fields = ['disk_state_value']
            tmp_5 = OrderedDict()
            tmp_5['ip_addr'] = use_id_return_racadm_ip(i['ip_addr_id'])
            for x in need_state.split(','):
                where = {'ip_addr_id':i['ip_addr_id'],'disk_state_key':x}
                tmp_6 = DB().get_one('Memory_info',fields,where)
                if tmp_6:
                    tmp_5[x] = tmp_6['disk_state_value']
                else:
                    tmp_5[x] = ''
            tmp_3.append(tmp_5)
        if tmp_3:
            return tmp_3
        else:
            return 'no'

# 获取保存的 Memory_status 信息
def achieve_Memory_status_page_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('Memory_status_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)
        tmp_3={}
        for i in tmp_2:
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_3[tmp_4] = use_id_return_racadm_ip(i['ip_addr_id'])
            
        fields=['ip_addr_id']
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('Memory_status_info',fields)
        tmp_2=[]
        for i in tmp_1:
            tmp_9 = OrderedDict()
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_9['ip_addr'] = tmp_3[tmp_4]
            for tmp_7 in need_state.split(','):
                tmp_9[tmp_7] = i[tmp_7]
            tmp_2.append(tmp_9)
        if tmp_2:
            return tmp_2
        else:
            return 'no'

# 获取保存的 Cpu 信息
def achieve_Cpu_page_info(need_state='tianshi',need_state_1='tianshi'):
    if need_state == 'tianshi' or need_state_1 == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('CPU_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)

        tmp_3=[]
        for i in tmp_2:
            fields = ['disk_state_value']
            tmp_5 = OrderedDict()
            tmp_5['ip_addr'] = use_id_return_racadm_ip(i['ip_addr_id'])
            for x in need_state.split(','):
                if x == 'cpu_info':
                    tmp_8 = 0
                    tmp_status='True'
                    tmp_13 = []
                    while tmp_status == 'True':
                        try:
                            tmp_8 = int(tmp_8)+1
                            tmp_12=[]
                            for y in need_state_1.split(','):
                                tmp_9=y.replace('xxxxx=xxxxx','%s'%(tmp_8))
                                where = {'ip_addr_id':i['ip_addr_id'],'disk_state_key':tmp_9}
                                tmp_11=DB().get_one('CPU_info',fields,where)['disk_state_value']
                                tmp_14=y.split('xxxxx=xxxxx',2)[1]
                                tmp_15=achieve_Memory_info_state_value(tmp_14)
                                if tmp_15 == 'no':
                                    tmp_15=tmp_14
                                tmp_12.append('%s : %s'%(tmp_15,tmp_11))
                            tmp_13.append(" | ".join(tmp_12))
                        except:
                            tmp_status='false'
                    tmp_5[x] = tmp_13
                    continue
                where = {'ip_addr_id':i['ip_addr_id'],'disk_state_key':x}
                tmp_6 = DB().get_one('CPU_info',fields,where)
                if tmp_6:
                    tmp_5[x] = tmp_6['disk_state_value']
                else:
                    tmp_5[x] = ''
            tmp_3.append(tmp_5)
        if tmp_3:
            return tmp_3
        else:
            return 'no'

# 获取保存的 Cpu_status 信息
def achieve_Cpu_status_page_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('CPU_status_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)
        tmp_3={}
        for i in tmp_2:
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_3[tmp_4] = use_id_return_racadm_ip(i['ip_addr_id'])
            
        fields=['ip_addr_id']
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('CPU_status_info',fields)
        tmp_2=[]
        for i in tmp_1:
            tmp_9 = OrderedDict()
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_9['ip_addr'] = tmp_3[tmp_4]
            for tmp_7 in need_state.split(','):
                tmp_9[tmp_7] = i[tmp_7]
            tmp_2.append(tmp_9)
        if tmp_2:
            return tmp_2
        else:
            return 'no'

# 获取保存的 Fan_status 信息
def achieve_Fan_status_page_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('Fan_status_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)
        tmp_3={}
        for i in tmp_2:
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_3[tmp_4] = use_id_return_racadm_ip(i['ip_addr_id'])
            
        fields=['ip_addr_id']
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('Fan_status_info',fields)
        tmp_2=[]
        for i in tmp_1:
            tmp_9 = OrderedDict()
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_9['ip_addr'] = tmp_3[tmp_4]
            for tmp_7 in need_state.split(','):
                tmp_9[tmp_7] = i[tmp_7]
            tmp_2.append(tmp_9)
        if tmp_2:
            return tmp_2
        else:
            return 'no'

# 获取保存的 Temp_status 信息
def achieve_Temp_status_page_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('Temp_status_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)
        tmp_3={}
        for i in tmp_2:
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_3[tmp_4] = use_id_return_racadm_ip(i['ip_addr_id'])
            
        fields=['ip_addr_id']
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('Temp_status_info',fields)
        tmp_2=[]
        for i in tmp_1:
            tmp_9 = OrderedDict()
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_9['ip_addr'] = tmp_3[tmp_4]
            for tmp_7 in need_state.split(','):
                tmp_9[tmp_7] = i[tmp_7]
            tmp_2.append(tmp_9)
        if tmp_2:
            return tmp_2
        else:
            return 'no'

# 获取保存的 Power_status 信息
def achieve_Power_status_page_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('Power_status_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)
        tmp_3={}
        for i in tmp_2:
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_3[tmp_4] = use_id_return_racadm_ip(i['ip_addr_id'])
            
        fields=['ip_addr_id']
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('Power_status_info',fields)
        tmp_2=[]
        for i in tmp_1:
            tmp_9 = OrderedDict()
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_9['ip_addr'] = tmp_3[tmp_4]
            for tmp_7 in need_state.split(','):
                tmp_9[tmp_7] = i[tmp_7]
            tmp_2.append(tmp_9)
        if tmp_2:
            return tmp_2
        else:
            return 'no'

# 获取保存的 Battery_status 信息
def achieve_Battery_status_page_info(need_state='tianshi'):
    if need_state == 'tianshi':
        return 'no'
    else:
        tmp_1=DB().get_list('Battery_status_info',['ip_addr_id'])
        # 对数据进行去重处理
        run_function = lambda x, y: x if y in x else x + [y]
        tmp_2=reduce(run_function, [[], ] + tmp_1)
        tmp_3={}
        for i in tmp_2:
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_3[tmp_4] = use_id_return_racadm_ip(i['ip_addr_id'])
            
        fields=['ip_addr_id']
        for tmp_1 in need_state.split(','):
            fields.append(tmp_1)
        tmp_1=DB().get_list('Battery_status_info',fields)
        tmp_2=[]
        for i in tmp_1:
            tmp_9 = OrderedDict()
            tmp_4='tmp_%s_tmp'%(i['ip_addr_id'])
            tmp_9['ip_addr'] = tmp_3[tmp_4]
            for tmp_7 in need_state.split(','):
                tmp_9[tmp_7] = i[tmp_7]
            tmp_2.append(tmp_9)
        if tmp_2:
            return tmp_2
        else:
            return 'no'






