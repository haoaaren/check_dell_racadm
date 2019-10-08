#!/bin/bash
source /etc/profile
mysql_ip_host='192.168.0.119'
mysql_ip_port='3306'
mysql_connect_user='Hardware_read'
mysql_connect_passwd='3DeV4B7nPyE5ngX4'

check_shell_file="/usr/local/sbin/curl_check_racadm/echo_check_racadm.sh"
tmp_file='/tmp/3'
tmp_file_tmp='/tmp/curl_check_racadm_tmp'

[[ -f ${tmp_file_tmp} ]] && echo '重复运行' && exit
touch ${tmp_file_tmp}

date "+%Y年%m月%d日 %H:%M:%S" > ${tmp_file}
echo '=========start=========' >> ${tmp_file}
for i in `/usr/bin/mysql -h${mysql_ip_host} --port=${mysql_ip_port} -u${mysql_connect_user} -p${mysql_connect_passwd} -Bse 'use HardwareState; select ip_addr FROM monitored_ipaddr;'`
do
	nohup /bin/bash ${check_shell_file} ${i} >> /tmp/3 &
done
# 更改过期信息
nohup /bin/bash ${check_shell_file} 998 racadm_disk_change_old >> /tmp/3 &
# 发送告警
# nohup /bin/bash ${check_shell_file} 998 warning_toolkit >> /tmp/3 &
rm -f ${tmp_file_tmp}