#!/bin/bash
source /etc/profile
ip_addr=$1
server_ip='192.168.0.48'
server_port=9094
operate_value=$2



if [[ ${ip_addr} == '' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 参数传递失败,为空"
fi
if [[ ${operate_value} == 'racadm_disk_change_old' ]]
then
	tianshi=`curl -s "http://${server_ip}:${server_port}/racadm_disk_change_old"`
elif [[ ${operate_value} == 'warning_toolkit' ]]
then
	tianshi=`curl -s "http://${server_ip}:${server_port}/warning_toolkit"`
else
	tianshi=`curl -s "http://${server_ip}:${server_port}/dell_racadm?IP_addr=${ip_addr}"`
fi

if [[ ${tianshi} == 'ok' ]]
then
	if [[ ${operate_value} == '' ]]
	then
		echo "`date +'%Y-%-m-%d %H:%M:%S'` 传入IP: ${ip_addr} 执行完毕"
	elif [[ ${operate_value} == 'racadm_disk_change_old' ]]
	then
		echo "`date +'%Y-%-m-%d %H:%M:%S'` 磁盘旧状态更改完毕"
	elif [[ ${operate_value} == 'warning_toolkit' ]]
	then
		echo "`date +'%Y-%-m-%d %H:%M:%S'` 告警已发送"
	fi
elif [[ ${tianshi} == '01' ]]
then
	echo '请将本机IP加入白名单'
elif [[ ${tianshi} == '1' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 传入IP: ${ip_addr} 地址不在记录中"
elif [[ ${tianshi} == '2' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 信息 获取错误"
elif [[ ${tianshi} == '3' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 无法获取测试用 racadm 命令"
elif [[ ${tianshi} == '4' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} racadm 连接异常"
elif [[ ${tianshi} == '5' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 获取 服务器型号 服务标签 快速服务代码 操作系统 电源状态 网卡 等等信息失败"
elif [[ ${tianshi} == '6' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 硬件资源 内存 信息格式化失败"
elif [[ ${tianshi} == '7' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 硬件资源 内存 信息入库失败"
elif [[ ${tianshi} == '8' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 硬件资源 CPU 信息格式化失败"
elif [[ ${tianshi} == '9' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 硬件资源 CPU 信息入库失败"
elif [[ ${tianshi} == '10' ]]
then
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} cpu 内存 温度 风扇 硬盘 主板等等信息(传感器) 获取失败"
elif [[ ${tianshi} == 'good' ]]
then
	if [[ ${operate_value} == 'warning_toolkit' ]]
	then
		echo "`date +'%Y-%-m-%d %H:%M:%S'` 所有状态都很好"
	fi
else
	echo "`date +'%Y-%-m-%d %H:%M:%S'` 此IP: ${ip_addr} 未知错误:${tianshi}  请知悉"
fi