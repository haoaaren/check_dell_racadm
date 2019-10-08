#coding:utf-8
from flask import request,render_template, redirect,session
from . import app
from dbutil import DB
from collections import OrderedDict
import json
import datetime

# 基础
from dell_racadm import check_client_ip,check_dell_racadm_ip,dell_racadm_achieve_ip_info,achieve_dell_cacadm_comman,check_dell_racadm_info


# 数据信息
# 硬盘信息
from dell_racadm import check_dell_racadm_Physical_disk_format,achieve_disk_reportsclass_table_value,check_dell_racadm_Physical_disk_save

# 系统信息格式化 + 信息/网卡信息入库
from dell_racadm import check_dell_racadm_System_format,check_dell_racadm_System_Nic_info_save
# NIC网卡信息格式化
from dell_racadm import check_dell_racadm_NIC_CARD_format


# CPU信息
from dell_racadm import check_dell_racadm_cpu_info_format,check_dell_racadm_CPU_info_save

# 内存信息
from dell_racadm import check_dell_racadm_memory_info_format,check_dell_racadm_memory_info_save

# 前面板信息
from dell_racadm import check_dell_racadm_System_LCD_CurrentDisplay_save

# 传感器 状态 信息
# 传感器-内存
from dell_racadm import check_dell_racadm_Sensor_memory_format,check_dell_racadm_Sensor_memory_save

# 传感器-风扇
from dell_racadm import check_dell_racadm_Sensor_FAN_format,check_dell_racadm_Sensor_Fan_save

# 传感器-CPU
from dell_racadm import check_dell_racadm_Sensor_CPU_format,check_dell_racadm_Sensor_CPU_save

# 传感器-温度
from dell_racadm import check_dell_racadm_Sensor_TEMPERATURE_format,check_dell_racadm_Sensor_TEMPERATURE_save

# 传感器-电源
from dell_racadm import check_dell_racadm_Sensor_POWER_format,check_dell_racadm_Sensor_POWER_save

# 传感器-电池
from dell_racadm import check_dell_racadm_Sensor_BATTERY_format,check_dell_racadm_Sensor_BATTERY_save

# 此为用来传入IP以检查 并入库。暂未做限制；
# 经测试，应限制在300，警戒500的范围。
# 限制可以在调用此接口的那端限制
@app.route('/dell_racadm', methods=["GET"])
def dell_racadm():
    if request.method == "GET":
        client_ip = request.remote_addr
        if check_client_ip(client_ip) == 'no':
            # IP地址没在白名单 禁止访问
            return '01'
        IP_addr=request.args.get("IP_addr")
        check_ip_Result=check_dell_racadm_ip(client_ip,IP_addr)
        if check_ip_Result == 'no':
            # 返回1 IP地址不在记录中
            return '1'
        achieve_ip_Result=dell_racadm_achieve_ip_info(client_ip,IP_addr)
        if achieve_ip_Result == 'no':
            # 返回 2 IP地址信息 获取错误
            return '2'
        
        check_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 先检测 racadm 是否可用
        tmp_0 = achieve_dell_cacadm_comman('test_connect')
        if tmp_0 == 'no':
            # 返回 3 代表 无法获取测试用 racadm 命令
            return '3'
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 == 'no' :
            # 返回 4 代表 racadm 连接异常
            return '4'

        # 获取 磁盘信息 入库
        tmp_0 = achieve_dell_cacadm_comman('achieve_disk')
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 != 'no':
            tmp_2=check_dell_racadm_Physical_disk_format(tmp_1,IP_addr,check_time)
            if tmp_2 != 'no':
                need_state = achieve_disk_reportsclass_table_value('save_status_data_need')
                tmp_3=check_dell_racadm_Physical_disk_save(IP_addr,achieve_ip_Result['id'],check_time,tmp_1,tmp_2,need_state)
        # 获取 服务器型号 服务标签 快速服务代码 操作系统 电源状态 网卡 等等信息入库
        tmp_0 = achieve_dell_cacadm_comman('achieve_NIC_and_System')
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 == 'no':
            return '5'
        # 获取 服务器型号 服务标签 快速服务代码 操作系统 电源状态 网卡 等等信息入库
        # 服务器型号 服务标签 快速服务代码 操作系统 电源状态 格式化
        need_state = achieve_disk_reportsclass_table_value('System_Information')
        tmp_3=check_dell_racadm_System_format(tmp_1,IP_addr,check_time,need_state)
        # 网卡信息格式化
        tmp_4=check_dell_racadm_NIC_CARD_format(tmp_1,IP_addr,check_time)
        # 入库操作
        tmp_5=check_dell_racadm_System_Nic_info_save(achieve_ip_Result['id'],System_data=tmp_3,Nic_data=tmp_4)
                
        # 硬件资源 内存 信息入库
        tmp_0 = achieve_dell_cacadm_comman('achieve_Memory_info')
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 == 'no':
            return '6'
        tmp_2=check_dell_racadm_memory_info_format(tmp_1,IP_addr,check_time,achieve_ip_Result['id'])
        if tmp_2 == 'no':
            return '7'
        tmp_3=check_dell_racadm_memory_info_save(achieve_ip_Result['id'],tmp_2)

        # 硬件资源 CPU 信息入库
        tmp_0 = achieve_dell_cacadm_comman('achieve_CPU_info')
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 == 'no':
            return '8'
        tmp_2 = check_dell_racadm_cpu_info_format(tmp_1,IP_addr,check_time,achieve_ip_Result['id'])
        if tmp_2 == 'no':
            return '9'
        tmp_3 = check_dell_racadm_CPU_info_save(achieve_ip_Result['id'],tmp_2)

        # 硬件信息 前面板信息获取
        tmp_0 = achieve_dell_cacadm_comman('achieve_System_LCD')
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 != 'no':
            check_dell_racadm_System_LCD_CurrentDisplay_save(achieve_ip_Result['id'],tmp_1)
        
        # cpu 内存 温度 风扇 硬盘 主板等等信息(传感器)
        tmp_0 = achieve_dell_cacadm_comman('achieve_sensorinfo')
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 == 'no':
            return '10'
        # 内存传感器信息格式化并入库
        tmp_2=check_dell_racadm_Sensor_memory_format(tmp_1,check_time,achieve_ip_Result['id'])
        if tmp_2 != 'no':
            check_dell_racadm_Sensor_memory_save(achieve_ip_Result['id'],tmp_2)
        # 风扇传感器信息格式化并入库
        tmp_2=check_dell_racadm_Sensor_FAN_format(tmp_1,check_time,achieve_ip_Result['id'])
        if tmp_2 != 'no':
            check_dell_racadm_Sensor_Fan_save(achieve_ip_Result['id'],tmp_2)
        # CPU传感器信息格式化并入库
        tmp_2=check_dell_racadm_Sensor_CPU_format(tmp_1,check_time,achieve_ip_Result['id'])
        if tmp_2 != 'no':
            check_dell_racadm_Sensor_CPU_save(achieve_ip_Result['id'],tmp_2)
        # 温度传感器信息格式化并入库
        tmp_2=check_dell_racadm_Sensor_TEMPERATURE_format(tmp_1,check_time,achieve_ip_Result['id'])
        if tmp_2 != 'no':
            check_dell_racadm_Sensor_TEMPERATURE_save(achieve_ip_Result['id'],tmp_2)
        # 电源传感器信息格式化并入库
        tmp_2=check_dell_racadm_Sensor_POWER_format(tmp_1,check_time,achieve_ip_Result['id'])
        if tmp_2 != 'no':
            check_dell_racadm_Sensor_POWER_save(achieve_ip_Result['id'],tmp_2)
        # 电池传感器信息格式化并入库
        tmp_2=check_dell_racadm_Sensor_BATTERY_format(tmp_1,check_time,achieve_ip_Result['id'])
        if tmp_2 != 'no':
            check_dell_racadm_Sensor_BATTERY_save(achieve_ip_Result['id'],tmp_2)



                

        return 'ok'
    #    return json.dumps(tmp_2, ensure_ascii=False)
    else:
        return redirect('/')


# cpu 内存 温度 风扇 硬盘 主板等等信息入库
@app.route('/save_cpu', methods=["GET"])
def save_cpu():
    if request.method == "GET":
        client_ip = request.remote_addr
        if check_client_ip(client_ip) == 'no':
            # IP地址没在白名单 禁止访问
            return '01'
        IP_addr=request.args.get("IP_addr")
        check_ip_Result=check_dell_racadm_ip(client_ip,IP_addr)
        if check_ip_Result == 'no':
            # 返回1 IP地址不在记录中
            return '1'
        achieve_ip_Result=dell_racadm_achieve_ip_info(client_ip,IP_addr)
        if achieve_ip_Result == 'no':
            # 返回 2 IP地址信息 获取错误
            return '2'

        # 更新网卡
        tmp_0 = achieve_dell_cacadm_comman('achieve_NIC_and_System')
        if tmp_0 == 'no':
            return '3'
        tmp_1 = check_dell_racadm_info(IP_addr,achieve_ip_Result['card_user_name'],achieve_ip_Result['card_user_passwd'],tmp_0)
        if tmp_1 == 'no':
            # 返回 3 代表 racadm 连接异常
            return '3'
        check_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        need_state = achieve_disk_reportsclass_table_value('System_Information')
        tmp_2=check_dell_racadm_System_format(tmp_1,IP_addr,check_time,need_state)
        return json.dumps(tmp_2, ensure_ascii=False)
        tmp_2 = check_dell_racadm_NIC_CARD_format(tmp_1,IP_addr,check_time)
        if tmp_2 == 'no':
            # 返回 4 代表 数据格式化失败,规则不匹配
            return '4' 
        else:
            return json.dumps(tmp_2, ensure_ascii=False)
            return tmp_2
    return '33'
