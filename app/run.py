#/usr/bin/env python
#coding=utf8

ip_list='192.168.0.20'
ip_addr_list=['192.168.25.200','192.168.25.200','192.168.25.200','192.168.25.200']

import os
import sys
import MySQLdb
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask,request,render_template,redirect
from collections import OrderedDict

app=Flask(__name__)

#获取数据库的连接对象
#def Mysqlconnect(select_type='select',IP_addr='None',tomcat_name='None',tomcat_port='None',tomcat_Xms='None',tomcat_Xmx='None',tomcat_Xss='None',tomcat_old_version='None',tomcat_new_version='None',change_date_time='None',last_change_date_time='None',select_sql='None'):
def Mysqlconnect(select_type='select',IP_addr='None',ACL_type='None',logrotate_start_time='None',logrotate_end_time='None',logrotate_end_file_numbe='None',logrotate_end_name='None',logrotate_server_logrotate_name='None',logrotate_server_logrotate_file_numbe='None',logrotate_start_rsync_time='None',logrotate_end_rsync_time='None',Manual_synchronization_rsync_time='None',select_sql='None',table_field='None',table_field_value='None'):
    use_table='debug'
    con = MySQLdb.connect(host='192.168.0.119',user='check_log_backup',passwd='NR5CpeEnTD',db='check_log_backup',charset='utf8');

    if select_type == 'select':
        with con:
            cur=con.cursor()
            if IP_addr is None or select_sql == 'None':
                sql="SELECT * from %s;"%(use_table)
            else:
                sql="SELECT * from %s where %s;"%(use_table,select_sql)
            cur.execute(sql)
            rows=cur.fetchall()
            if len(rows):
                return rows 
            else:
                return 'None'
            con.close
    elif select_type == 'update':
        with con:
            cur=con.cursor()
            sql="SELECT * from %s where IP_addr='%s' and ACL_type='%s';"%(use_table,IP_addr,ACL_type)
            cur.execute(sql)
            rows=cur.fetchall()
            if not rows:
                sql="INSERT INTO %s(IP_addr,ACL_type,logrotate_start_time) VALUE('%s','%s','%s');"%(use_table,IP_addr,ACL_type,table_field_value)
                cur.execute(sql)
                con.close
                return 'OK'
            else:
                if table_field == 'logrotate_start_time':
                    sql="update %s set %s='%s',logrotate_end_time=null,logrotate_start_rsync_time=null,logrotate_end_rsync_time=null where IP_addr='%s' and ACL_type='%s';"%(use_table,table_field,table_field_value,IP_addr,ACL_type)
                    #print sql
                else:
                    sql="update %s set %s='%s' where IP_addr='%s' and ACL_type='%s';"%(use_table,table_field,table_field_value,IP_addr,ACL_type)
                try:
                    cur.execute(sql)
                except:
                    con.close
                    return 'ERROR'
                else:
                    con.close
                    return 'OK'
    elif select_type == 'update_server':
        with con:
            cur=con.cursor()
            sql="SELECT * from %s where IP_addr='%s' and ACL_type='%s';"%(use_table,IP_addr,ACL_type)
            cur.execute(sql)
            rows=cur.fetchall()
            if not rows:
                sql="INSERT INTO %s(IP_addr,ACL_type,logrotate_server_logrotate_name) VALUE('%s','%s','%s');"%(use_table,IP_addr,ACL_type,table_field_value)
                print sql
                cur.execute(sql)
                con.close
                return 'OK'
            else:
                if table_field == 'logrotate_server_logrotate_name':
                    sql="update %s set %s='%s',logrotate_server_logrotate_file_numbe=null where IP_addr='%s' and ACL_type='%s';"%(use_table,table_field,table_field_value,IP_addr,ACL_type)
                else:
                    sql="update %s set %s='%s' where IP_addr='%s' and ACL_type='%s';"%(use_table,table_field,table_field_value,IP_addr,ACL_type)
                try:
                    cur.execute(sql)
                except:
                    con.close
                    return 'ERROR'
                else:
                    con.close
                    return 'OK'

 
def MMysql_log(select_type='select',client_ip='None',table_field='None',table_field_value='None',select_sql='None',IP_addr='None',ACL_type='None'):
    use_table='log'
    con = MySQLdb.connect(host='192.168.0.119',user='check_log_backup',passwd='NR5CpeEnTD',db='check_log_backup',charset='utf8');
    
    if select_type == 'select':
        with con:
            cur=con.cursor()
            if select_sql == '' or select_sql == 'None':
                sql="SELECT * from %s order by `id` desc limit 10000;"%(use_table)
            else:
                sql="SELECT * from %s where %s order by `id` desc limit 10000;"%(use_table,select_sql)
            print sql
            cur.execute(sql)
            rows=cur.fetchall()
            con.close
            if len(rows):
                return rows 
            else:
                return 'None'
        
    elif select_type == 'insert':
        with con:
            cur=con.cursor()
            sql="INSERT INTO %s(client_ip,IP_addr,ACL_type,field_name,field_value) VALUE('%s','%s','%s','%s','%s');"%(use_table,client_ip,IP_addr,ACL_type,table_field,table_field_value)
            cur.execute(sql)
            con.close
        

@app.route('/update',methods = ['GET', 'POST'])
def add_ip():
    IP_addr = request.args.get('IP_addr')
    ACL_type = request.args.get('ACL_type')
    table_field = request.args.get('table_field')
    table_field_value = request.args.get('table_field_value')
    client_ip=request.remote_addr

    MMysql_log(select_type='insert',table_field=table_field,table_field_value=table_field_value,client_ip=client_ip,IP_addr=IP_addr,ACL_type=ACL_type)

    if IP_addr == 'None' or IP_addr == '' or ACL_type == 'None' or ACL_type == '':
        return redirect('/')
    if table_field == 'logrotate_start_time' or table_field == 'logrotate_end_time' or table_field == 'logrotate_server_logrotate_name' or table_field == 'logrotate_start_rsync_time' or table_field == 'logrotate_end_rsync_time':
        if table_field_value == '1':
            table_field_value = datetime.datetime.now().strftime("%Y年%m月%d日 %H时%M分%S秒")

    #if not IP_addr.find(client_ip):
    #    return redirect('/')
    Mysqlconnect(select_type='update',IP_addr=IP_addr,ACL_type=ACL_type,table_field=table_field,table_field_value=table_field_value)

    return redirect('/')

@app.route('/update_server',methods = ['GET', 'POST'])
def check_server_log():
    IP_addr = request.args.get('IP_addr')
    ACL_type = request.args.get('ACL_type')
    table_field = request.args.get('table_field')
    table_field_value = request.args.get('table_field_value')

    if IP_addr == 'None' or IP_addr == '' or ACL_type == 'None' or ACL_type == '' or table_field == 'None' or table_field == '' or table_field_value == '' or table_field_value == 'None':
        return redirect('/')

    Mysqlconnect(select_type='update_server',IP_addr=IP_addr,ACL_type=ACL_type,table_field=table_field,table_field_value=table_field_value)

    return redirect('/')


@app.errorhandler(404) 
def page_not_found(error): 
    return redirect('/') 

@app.route('/select_log',methods = ['GET', 'POST'])
def select_log():
    IP_addr=request.form.get('IP_addr','')
    ACL_type=request.form.get('ACL_type','')
    client_ip=request.form.get('client_ip','')

    if IP_addr is None or IP_addr == '':
        if ACL_type is None or ACL_type == '':
            if client_ip is None or client_ip == '':
                select_sql='None'
            else:
                select_sql="client_ip='%s'"%(client_ip)
        else:
            if client_ip is None or client_ip == '':
                select_sql="ACL_type='%s'"%(ACL_type)
            else:
                select_sql="client_ip='%s' and ACL_type='%s'"%(client_ip,ACL_type)
    else:
        if ACL_type is None or ACL_type == '':
            if client_ip is None or client_ip == '':
                select_sql="IP_addr='%s'"%(IP_addr)
            else:
                select_sql="IP_addr='%s' and client_ip='%s'"%(IP_addr,client_ip)
        else:
            if client_ip is None or client_ip == '':
                select_sql="IP_addr='%s' and ACL_type='%s'"%(IP_addr,ACL_type)
            else:
                select_sql="IP_addr='%s' and ACL_type='%s' ACL_type='%s'"%(IP_addr,ACL_type,client_ip)

    if select_sql == '' or select_sql == 'None':
        names=MMysql_log(select_type='select')
    else:
        names=MMysql_log(select_type='select',select_sql=select_sql)
    return render_template('select_log.html',names=names,IP_addr=IP_addr,ACL_type=ACL_type,client_ip=client_ip)

@app.route('/')
def index():
    client_ip=request.remote_addr
    tmp_1=[]
    for ip_addr in  ip_addr_list:
        print ip_addr
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        result_version = os.popen(("racadm -r %s -uroot -p calvin storage get pdisks -o | sed 's#Disk.Bay#\\nDisk.Bay#g' | grep '^Disk' -A320 | tr '\n' '|' | sed 's/ //g' "%(ip_addr))).read()
        info_is_need_use_hava = 'yes'
        if info_is_need_use_hava == 'yes' :
            for i in result_version.replace("|Disk.", " Disk.").split(' '):
                tmp_2 = OrderedDict()
                tmp_6=[]
                if i.startswith('Disk.'):
                    for k in i.split('|'):
                        if '=' in k:
                            tmp_3,tmp_4 = k.split('=')[0],k.split('=')[1]
                            tmp_2[tmp_3] = tmp_4
                        elif k:
                            tmp_2['disk_name'] = k
                tmp_2['ip_addr'] = ip_addr
                tmp_1.append(tmp_2)

    #print tmp_1
    return render_template('test5.html',client_ip=client_ip,names=tmp_1,IP_addr=ip_addr)

if __name__=='__main__':
    #app.run(host='0.0.0.0',port=9094,threaded=True,debug=False)
    #app.run(host='0.0.0.0',port=9094,threaded=False,debug=True)
    app.run(host='0.0.0.0',port=9094,threaded=True,debug=True)
