#coding:utf-8
from flask import request,render_template, redirect,session
from . import app
from dbutil import DB
from collections import OrderedDict
import json
import datetime
from dell_racadm import check_client_ip,warning_toolkit_disk_date,check_client_ip,send_ding_talk_warning



# 发送告警
@app.route('/warning_toolkit', methods=["GET"])
def warning_toolkit():
    if request.method == "GET":
        client_ip = request.remote_addr
        if check_client_ip(client_ip) == 'no':
            # IP地址没在白名单 禁止访问
            return '01'

        #读取磁盘告警
        tmp_status='999'
        tmp_1=warning_toolkit_disk_date()
        if tmp_1 == 'no':
      #      tmp_2=[{'title':'Run well','text':'All Run IS Good!'}]
      #      send_ding_talk_warning(tmp_2)
            return 'good'
        else:
            # 发送告警
            # 1、发送钉钉告警
            # 只管传递，不管对错
            tmp_status='0'
            tmp_2=[]
            for i in tmp_1:
              #  print i
                tmp_3= []
              #  tmp_3['title'] = 'DELL server : %s disk : %s warning'%(i['ip_addr'],i['disk_name'])
              #  tmp_3['text'] = '#### %s-%s Disk Warning\n>IP：%s\n\n>Disk_name：%s\n\n>Status：Bad'%(i['ip_addr'],i['disk_name'],i['ip_addr'],i['disk_name'])
                
                tmp_2.append(tmp_3)

            #send_ding_talk_warning(tmp_2)
    
    print tmp_2
    print tmp_status
    return 'ok'
      


  
