# check_dell_racadm
开发环境：
	CentOS release 6.5
	Python 2.7.14
	pip 9.0.1 
	DBUtils-1.1
	
	
安装运行环境(仅供参考)：	
	pip install flask
	pip install DBUtils
	pip install request
	pip install requests
	pip install mysql-python
	easy_install jinja2
	
config.py
	请修改为自己的
	
	
#调用脚本
	echo_check_racadm.sh 为访问URL更改、告警使用的脚本
	curl_check_racadm.sh 为从数据库读出IP地址，然后调用echo_check_racadm.sh 来做一些操作用

	
#数据库 文件夹里的 HardwareState.sql 就是备份的库，导入即可
	除了 monitored_ipaddr 其余表应该都不需要主键，monitored_ipaddr的id为个别表的外键
	
	
#运行: python run.py


默认用户：youku
默认密码：123456
	
	
dell远程卡监控
	2019年10月8日 18:00:13
		数据已经全部入库

	2019年9月18日 17:44:42
		1、更新信息脚本已拆分
		2、获取 服务器型号 服务标签 快速服务代码 操作系统 电源状态 网卡 等等信息已入库


模版基于51reboot上课时用的模版
编写中用的物理机器不足，且加上个人能力有限，所以不保证脚本可用性，有问题请自行解决，或自行编写-_-|||


#1、 表字段定义
	check_client_ip						定义允许哪些IP做一些定时调用url，以便来更新数据的接口的白名单
	disk_info							服务器磁盘的所有数据信息(需要的数据字段在 disk_reportsclass 定义)，未做数据格式化前的数据（关联有外键 monitored_ipaddr表的id字段）
	disk_reportsclass					定义需要保留的数据字段
	disk_status_info					服务器磁盘的状态信息（关联有外键 monitored_ipaddr表的id字段）
	disk_status_state					各个英文字段的中文(参考自dell远程管理卡)
	disk_warning_table					定义需要告警的字段，和参考值(warning_change_value 已弃用)
	monitored_ipaddr					定义需要检查的服务器，有远程卡的用户名密码字段，为空则按照remote_card_id里的读取
	remote_card_info					定义远程卡的远程连接参数
	users								用户表(默认123456(4cba3a57c5fa5468032f6ae8c096c40c)),权限管理较弱，权限管理基本没用(请自行开发)
	warning_toolkit_table				定义用来发送报警的接口(暂只支持钉钉)

#2、版本：0.0.1(暂停开发)
	实现钉钉报警
	暂只支持dell服务器，通过racadm来获取更新数据。(需要使用LC 1.7版本以上，iDrac 2.10版本以上，iDrac7及以上)
	可以查看服务器的磁盘的详细数据信息
	可以查看服务器磁盘的状态信息
	可以自定义检查某个服务器的磁盘的状态信息
	
#3、各个接口的释义
	/racadm_disk_change_old				用来变更过时信息的
	/warning_toolkit					用来发送报警的
	/dell_racadm						用来更新某个IP数据的
	/get_dell_racadm_disk_status_page	获取各个服务器磁盘状态信息页
	/get_dell_racadm_info				获取各个服务器磁盘所有信息页


#实现（前面板信息 可有可无）：
	CPU
	内存
	温度
	风扇
	网卡
	硬盘
	主板
如上硬件的详细信息 和 状态信息 和 历史信息，并画图、告警


#告警设想(未经过实际检测)
所有状态判断依据 均需要可以支持多项
	CPU状态： 
		检测状态是否为OK
		状况 是否为 在线
	内存状态：
		状态是否为OK 且  状况不为 Absent
	风扇状态；
		判断状态是否为 Ok
	温度状态：
		判断状态是否为OK
		先判断 灾难级别 是否过大 或者过小 再判断 警告级别
			灾难级别 直接告警忽略警告级别
	电源状态：
		判断状态是否不为 Present
	电池状况：
		判断状态是否为Ok
		

	
	
####暂只实现信息入库，实现了磁盘告警，其余均为实现(因领导要求也因为机器没有了，所以开发停止。其余功能自己写吧)
####第一次发布开源的项目


#运行截图
	请看运行截图文件夹(MD格式的插入图片没搞过)


		