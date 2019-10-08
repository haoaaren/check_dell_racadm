/*
Navicat MySQL Data Transfer

Source Server         : 192.168.24.98
Source Server Version : 50725
Source Host           : 127.0.0.1:3306
Source Database       : HardwareState

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-10-08 14:18:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `Battery_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `Battery_status_info`;
CREATE TABLE `Battery_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `check_time` varchar(50) NOT NULL,
  `Sensor_Name` varchar(50) NOT NULL,
  `Sensor_Status` varchar(20) NOT NULL,
  `Sensor_Reading` varchar(20) NOT NULL,
  `Sensor_lc` varchar(20) NOT NULL,
  `Sensor_uc` varchar(20) NOT NULL,
  KEY `Temp_status_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `Battery_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 温度 传感器信息';

-- ----------------------------
-- Records of Battery_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `check_client_ip`
-- ----------------------------
DROP TABLE IF EXISTS `check_client_ip`;
CREATE TABLE `check_client_ip` (
  `ip` varchar(50) NOT NULL,
  `ip_user` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用途用来检测 client_ip 的，只有在列表里的才可以访问';

-- ----------------------------
-- Records of check_client_ip
-- ----------------------------
INSERT INTO `check_client_ip` VALUES ('192.168.0.50', '定时调用IP');

-- ----------------------------
-- Table structure for `CPU_info`
-- ----------------------------
DROP TABLE IF EXISTS `CPU_info`;
CREATE TABLE `CPU_info` (
  `ip_addr_id` int(100) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  `disk_state_value` varchar(100) NOT NULL,
  UNIQUE KEY `ip_addr_id_2` (`ip_addr_id`,`disk_state_key`) USING BTREE,
  KEY `ip_addr_id` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `CPU_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 CPU信息';

-- ----------------------------
-- Records of CPU_info
-- ----------------------------

-- ----------------------------
-- Table structure for `CPU_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `CPU_status_info`;
CREATE TABLE `CPU_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `check_time` varchar(50) NOT NULL,
  `Sensor_Name` varchar(20) NOT NULL,
  `Sensor_Status` varchar(20) NOT NULL,
  `Sensor_State` varchar(50) NOT NULL,
  `Sensor_lc` varchar(20) DEFAULT 'NA',
  `Sensor_uc` varchar(20) DEFAULT 'NA',
  KEY `Memory_status_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `CPU_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 内存信息';

-- ----------------------------
-- Records of CPU_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `disk_info`
-- ----------------------------
DROP TABLE IF EXISTS `disk_info`;
CREATE TABLE `disk_info` (
  `ip_addr_id` int(100) NOT NULL,
  `check_time` varchar(50) NOT NULL DEFAULT '',
  `disk_info` text NOT NULL,
  KEY `disk_name` (`disk_info`(255)) USING BTREE,
  KEY `disk_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `disk_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录磁盘详细信息';

-- ----------------------------
-- Records of disk_info
-- ----------------------------

-- ----------------------------
-- Table structure for `disk_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `disk_status_info`;
CREATE TABLE `disk_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `disk_name` varchar(100) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  `disk_state_value` varchar(100) NOT NULL,
  UNIQUE KEY `ip_addr_id_2` (`ip_addr_id`,`disk_state_key`,`disk_name`) USING BTREE,
  KEY `disk_name` (`disk_name`) USING BTREE,
  KEY `ip_addr_id` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `disk_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录磁盘状态信息';

-- ----------------------------
-- Records of disk_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `disk_status_state`
-- ----------------------------
DROP TABLE IF EXISTS `disk_status_state`;
CREATE TABLE `disk_status_state` (
  `disk_state_name` varchar(20) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  PRIMARY KEY (`disk_state_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用来解释 racadm 获取的字段是用来做什么的';

-- ----------------------------
-- Records of disk_status_state
-- ----------------------------
INSERT INTO `disk_status_state` VALUES ('可用 RAID 磁盘空间', 'AvailableRaidDiskSpace');
INSERT INTO `disk_status_state` VALUES ('块大小', 'BlockSizeInBytes');
INSERT INTO `disk_status_state` VALUES ('总线协议', 'BusProtocol');
INSERT INTO `disk_status_state` VALUES ('设备说明', 'DeviceDescription');
INSERT INTO `disk_status_state` VALUES ('预测到故障', 'FailurePredicted');
INSERT INTO `disk_status_state` VALUES ('外型', 'FormFactor');
INSERT INTO `disk_status_state` VALUES ('热备用', 'Hotspare');
INSERT INTO `disk_status_state` VALUES ('制造日', 'ManufacturedDay');
INSERT INTO `disk_status_state` VALUES ('制造周', 'ManufacturedWeek');
INSERT INTO `disk_status_state` VALUES ('制造年', 'ManufacturedYear');
INSERT INTO `disk_status_state` VALUES ('制造者', 'Manufacturer');
INSERT INTO `disk_status_state` VALUES ('支持的速度', 'MaxCapableSpeed');
INSERT INTO `disk_status_state` VALUES ('介质类型', 'MediaType');
INSERT INTO `disk_status_state` VALUES ('协商速度', 'NegotiatedSpeed');
INSERT INTO `disk_status_state` VALUES ('操作状态', 'OperationState');
INSERT INTO `disk_status_state` VALUES ('部件号', 'PartNumber');
INSERT INTO `disk_status_state` VALUES ('电源状态', 'PowerStatus');
INSERT INTO `disk_status_state` VALUES ('产品 ID', 'ProductId');
INSERT INTO `disk_status_state` VALUES ('转速', 'RaidNominalMediumRotationRate');
INSERT INTO `disk_status_state` VALUES ('剩余额定写入耐久性', 'RemainingRatedWriteEndurance');
INSERT INTO `disk_status_state` VALUES ('汇总状态', 'RollupStatus');
INSERT INTO `disk_status_state` VALUES ('安全状态', 'SecurityStatus');
INSERT INTO `disk_status_state` VALUES ('序列号', 'SerialNumber');
INSERT INTO `disk_status_state` VALUES ('T10 PI 功能', 'T10PICapability');
INSERT INTO `disk_status_state` VALUES ('已用 RAID 磁盘空间', 'UsedRaidDiskSpace');

-- ----------------------------
-- Table structure for `disk_warning_table`
-- ----------------------------
DROP TABLE IF EXISTS `disk_warning_table`;
CREATE TABLE `disk_warning_table` (
  `warning_field_key` varchar(50) NOT NULL COMMENT '要告警检测的字段',
  `warning_value` varchar(50) NOT NULL COMMENT '正常值',
  `warning_change_value` varchar(50) NOT NULL COMMENT '不是正常值要更改为的值',
  PRIMARY KEY (`warning_field_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of disk_warning_table
-- ----------------------------
INSERT INTO `disk_warning_table` VALUES ('汇总状态', 'Ok', 'Bad');
INSERT INTO `disk_warning_table` VALUES ('电源状态', 'Spun-Up', 'Bad');

-- ----------------------------
-- Table structure for `Fan_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `Fan_status_info`;
CREATE TABLE `Fan_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `check_time` varchar(50) NOT NULL,
  `Sensor_Name` varchar(20) NOT NULL,
  `Sensor_Status` varchar(20) NOT NULL,
  `Sensor_Reading` varchar(50) NOT NULL,
  `Sensor_lc` varchar(20) NOT NULL DEFAULT '',
  `Sensor_uc` varchar(20) NOT NULL DEFAULT '',
  `Sensor_PWM` varchar(20) NOT NULL,
  KEY `Memory_status_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `Fan_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 内存信息';

-- ----------------------------
-- Records of Fan_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `Memory_info`
-- ----------------------------
DROP TABLE IF EXISTS `Memory_info`;
CREATE TABLE `Memory_info` (
  `ip_addr_id` int(100) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  `disk_state_value` varchar(100) NOT NULL,
  UNIQUE KEY `ip_addr_id_2` (`ip_addr_id`,`disk_state_key`) USING BTREE,
  CONSTRAINT `Memory_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 内存信息';

-- ----------------------------
-- Records of Memory_info
-- ----------------------------

-- ----------------------------
-- Table structure for `Memory_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `Memory_status_info`;
CREATE TABLE `Memory_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `check_time` varchar(50) NOT NULL,
  `Sensor_Name` varchar(20) NOT NULL,
  `Sensor_Status` varchar(20) NOT NULL,
  `Sensor_State` varchar(50) NOT NULL,
  `Sensor_lc` varchar(20) DEFAULT 'NA',
  `Sensor_uc` varchar(20) DEFAULT 'NA',
  KEY `Memory_status_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `Memory_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 内存信息';

-- ----------------------------
-- Records of Memory_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `Memory_status_state`
-- ----------------------------
DROP TABLE IF EXISTS `Memory_status_state`;
CREATE TABLE `Memory_status_state` (
  `disk_state_name` varchar(20) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  PRIMARY KEY (`disk_state_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用来解释 racadm 获取的字段是用来做什么的';

-- ----------------------------
-- Records of Memory_status_state
-- ----------------------------
INSERT INTO `Memory_status_state` VALUES ('CPU名', 'Brand');
INSERT INTO `Memory_status_state` VALUES ('更改时间', 'check_time');
INSERT INTO `Memory_status_state` VALUES ('纠正ECC SMI', 'CorrEccSmi');
INSERT INTO `Memory_status_state` VALUES ('IP地址', 'ip_addr');
INSERT INTO `Memory_status_state` VALUES ('二级缓存', 'L2Cache');
INSERT INTO `Memory_status_state` VALUES ('三级缓存', 'L3Cache');
INSERT INTO `Memory_status_state` VALUES ('内存操作模式', 'MemOpMode');
INSERT INTO `Memory_status_state` VALUES ('扩展内存测试', 'MemTest');
INSERT INTO `Memory_status_state` VALUES ('节点交织', 'NodeInterleave');
INSERT INTO `Memory_status_state` VALUES ('核心数', 'NumCores');
INSERT INTO `Memory_status_state` VALUES ('LC', 'Sensor_lc');
INSERT INTO `Memory_status_state` VALUES ('名称', 'Sensor_Name');
INSERT INTO `Memory_status_state` VALUES ('状况', 'Sensor_State');
INSERT INTO `Memory_status_state` VALUES ('状态', 'Sensor_Status');
INSERT INTO `Memory_status_state` VALUES ('UC', 'Sensor_uc');
INSERT INTO `Memory_status_state` VALUES ('内存大小', 'SysMemSize');
INSERT INTO `Memory_status_state` VALUES ('内存频率', 'SysMemSpeed');
INSERT INTO `Memory_status_state` VALUES ('内存类型', 'SysMemType');
INSERT INTO `Memory_status_state` VALUES ('内存电压', 'SysMemVolt');
INSERT INTO `Memory_status_state` VALUES ('可用的视频内存总量', 'VideoMem');

-- ----------------------------
-- Table structure for `monitored_ipaddr`
-- ----------------------------
DROP TABLE IF EXISTS `monitored_ipaddr`;
CREATE TABLE `monitored_ipaddr` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `ip_addr` varchar(50) NOT NULL,
  `remote_card_id` varchar(10) NOT NULL DEFAULT '====' COMMENT '远程管理卡id',
  `card_type_name` varchar(20) NOT NULL DEFAULT '====' COMMENT '远程管理卡品牌类型',
  `card_user_name` varchar(20) NOT NULL DEFAULT '====' COMMENT '远程管理卡用户名',
  `card_user_passwd` varchar(100) NOT NULL DEFAULT '====' COMMENT '远程管理卡密码',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_addr` (`ip_addr`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='本表记录受监控的IP地址，如果此记录有记录远程管理卡用户名密码则优先使用';

-- ----------------------------
-- Records of monitored_ipaddr
-- ----------------------------
INSERT INTO `monitored_ipaddr` VALUES ('5', '192.168.25.205', '1', '====', '====', '====');

-- ----------------------------
-- Table structure for `need_reportsclass`
-- ----------------------------
DROP TABLE IF EXISTS `need_reportsclass`;
CREATE TABLE `need_reportsclass` (
  `reports_submit` varchar(50) NOT NULL COMMENT '报表的字段名称',
  `get_date_fields` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用来记录报表所需要的出表单的各个字段';

-- ----------------------------
-- Records of need_reportsclass
-- ----------------------------
INSERT INTO `need_reportsclass` VALUES ('get_dell_racadm_info', 'ip_addr,check_time,disk_name,Status,DeviceDescription,RollupStatus,Name,State,OperationState,PowerStatus,Size,FailurePredicted,RemainingRatedWriteEndurance,SecurityStatus,BusProtocol,MediaType,UsedRaidDiskSpace,AvailableRaidDiskSpace,Hotspare,Manufacturer,ProductId,Revision,SerialNumber,PartNumber,NegotiatedSpeed,ManufacturedDay,ManufacturedWeek,ManufacturedYear,SasAddress,FormFactor,RaidNominalMediumRotationRate,T10PICapability,BlockSizeInBytes,MaxCapableSpeed');
INSERT INTO `need_reportsclass` VALUES ('save_status_data_need', 'check_time,State,RollupStatus,PowerStatus,Size,AvailableRaidDiskSpace');
INSERT INTO `need_reportsclass` VALUES ('System_Information', 'System_Model,System_Revision,System_BIOS_Version,Service_Tag,Express_Svc_Code,Host_Name,OS_Name,OS_Version,Power_Status,Fresh_Air_Capable');
INSERT INTO `need_reportsclass` VALUES ('NIC_state', 'ip_addr,check_time,NIC_name,NIC_type,NIC_MAC');
INSERT INTO `need_reportsclass` VALUES ('System_info_page', 'ip_addr,check_time,System_Model,System_Revision,System_BIOS_Version,Service_Tag,Express_Svc_Code,Host_Name,OS_Name,OS_Version,Power_Status,Fresh_Air_Capable,System_LCD_CurrentDisplay');
INSERT INTO `need_reportsclass` VALUES ('Memory_info', 'check_time,CorrEccSmi,MemOpMode,MemTest,NodeInterleave,SysMemSize,SysMemSpeed,SysMemType,SysMemVolt,VideoMem');
INSERT INTO `need_reportsclass` VALUES ('Memory_staus_info', 'check_time,Sensor_Name,Sensor_Status,Sensor_State,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Memory_status_info_need_ip', 'ip_addr,check_time,Sensor_Name,Sensor_Status,Sensor_State,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Cpu_status_info', 'check_time,Sensor_Name,Sensor_Status,Sensor_State,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Cpu_status_info_need_ip', 'ip_addr,check_time,Sensor_Name,Sensor_Status,Sensor_State,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Cpu_change_info', 'Procxxxxx=xxxxxBrand,Procxxxxx=xxxxxId,Procxxxxx=xxxxxL2Cache,Procxxxxx=xxxxxL3Cache,Procxxxxx=xxxxxNumCores');
INSERT INTO `need_reportsclass` VALUES ('Cpu_info', 'check_time,cpu_info,ControlledTurbo,DcuIpPrefetcher,DcuStreamerPrefetcher,DynamicCoreAllocation,LogicalProc,Proc64bit,ProcAdjCacheLine,ProcBusSpeed,ProcConfigTdp,ProcCores,ProcCoreSpeed,ProcExecuteDisable,ProcHwPrefetcher,ProcVirtualization,ProcX2Apic,QpiSpeed,RtidSetting');
INSERT INTO `need_reportsclass` VALUES ('Cpu_info_need_ip', 'ip_addr,check_time,cpu_info,ControlledTurbo,DcuIpPrefetcher,DcuStreamerPrefetcher,DynamicCoreAllocation,LogicalProc,Proc64bit,ProcAdjCacheLine,ProcBusSpeed,ProcConfigTdp,ProcCores,ProcCoreSpeed,ProcExecuteDisable,ProcHwPrefetcher,ProcVirtualization,ProcX2Apic,QpiSpeed,RtidSetting');
INSERT INTO `need_reportsclass` VALUES ('Fan_status_info', 'check_time,Sensor_Name,Sensor_Status,Sensor_Reading,Sensor_lc,Sensor_uc,Sensor_PWM');
INSERT INTO `need_reportsclass` VALUES ('Fan_status_info_need_ip', 'ip_addr,check_time,Sensor_Name,Sensor_Status,Sensor_Reading,Sensor_lc,Sensor_uc,Sensor_PWM');
INSERT INTO `need_reportsclass` VALUES ('Temp_status_info', 'check_time,Sensor_Name,Sensor_Status,Sensor_Reading,Sensor_lnc,Sensor_unc,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Temp_status_info_need_ip', 'ip_addr,check_time,Sensor_Name,Sensor_Status,Sensor_Reading,Sensor_lnc,Sensor_unc,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Power_status_info', 'check_time,Sensor_Name,Sensor_Status,Sensor_Type');
INSERT INTO `need_reportsclass` VALUES ('Power_status_info_need_ip', 'ip_addr,check_time,Sensor_Name,Sensor_Status,Sensor_Type');
INSERT INTO `need_reportsclass` VALUES ('Battery_status_info', 'check_time,Sensor_Name,Sensor_Status,Sensor_Reading,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Battery_status_info_need_ip', 'ip_addr,check_time,Sensor_Name,Sensor_Status,Sensor_Reading,Sensor_lc,Sensor_uc');
INSERT INTO `need_reportsclass` VALUES ('Memory_info_page', 'ip_addr,check_time,CorrEccSmi,MemOpMode,MemTest,NodeInterleave,SysMemSize,SysMemSpeed,SysMemType,SysMemVolt,VideoMem');

-- ----------------------------
-- Table structure for `NIC_info`
-- ----------------------------
DROP TABLE IF EXISTS `NIC_info`;
CREATE TABLE `NIC_info` (
  `ip_addr_id` int(100) NOT NULL,
  `ip_addr` varchar(50) NOT NULL,
  `check_time` varchar(50) NOT NULL DEFAULT '',
  `NIC_name` varchar(50) DEFAULT 'N/A',
  `NIC_type` varchar(20) DEFAULT 'N/A',
  `NIC_MAC` varchar(50) DEFAULT 'N/A',
  KEY `NIC_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `NIC_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 System Information 信息';

-- ----------------------------
-- Records of NIC_info
-- ----------------------------

-- ----------------------------
-- Table structure for `NIC_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `NIC_status_info`;
CREATE TABLE `NIC_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `disk_name` varchar(100) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  `disk_state_value` varchar(100) NOT NULL,
  UNIQUE KEY `ip_addr_id_2` (`ip_addr_id`,`disk_state_key`,`disk_name`) USING BTREE,
  KEY `disk_name` (`disk_name`) USING BTREE,
  KEY `ip_addr_id` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `NIC_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录网卡状态信息';

-- ----------------------------
-- Records of NIC_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `Power_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `Power_status_info`;
CREATE TABLE `Power_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `check_time` varchar(50) NOT NULL,
  `Sensor_Name` varchar(20) NOT NULL,
  `Sensor_Status` varchar(20) NOT NULL,
  `Sensor_Type` varchar(50) NOT NULL,
  KEY `Temp_status_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `Power_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 温度 传感器信息';

-- ----------------------------
-- Records of Power_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `racadm_command`
-- ----------------------------
DROP TABLE IF EXISTS `racadm_command`;
CREATE TABLE `racadm_command` (
  `command_name` varchar(50) NOT NULL,
  `command_body` text NOT NULL,
  `remarks` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`command_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='racadm 命令记录表';

-- ----------------------------
-- Records of racadm_command
-- ----------------------------
INSERT INTO `racadm_command` VALUES ('achieve_CPU_info', 'get BIOS.ProcSettings | grep -v \'\\[Key=\' | sed \'s/]//g\' | sed \'s/\\[//g\' | sed \'s/^#//g\' | sed \'s/^/====/g\' | sed \'s/$/====/g\'', '获取CPU信息命令');
INSERT INTO `racadm_command` VALUES ('achieve_disk', 'storage get pdisks -o | sed \'0,/Disk./s//====Disk./\' | sed \'s/====/\\n/g\' | grep \'^Disk\' -A320 | tr \'\\n\' \'|\' | sed \'s/^/|/g\'', '获取磁盘信息命令');
INSERT INTO `racadm_command` VALUES ('achieve_Memory_info', 'get BIOS.memSettings | grep -v \'\\[Key=\' | sed \'s/]//g\' | sed \'s/\\[//g\' | sed \'s/^#//g\' | sed \'s/^/====/g\' | sed \'s/$/====/g\'', '获取内存信息命令');
INSERT INTO `racadm_command` VALUES ('achieve_NIC_and_System', 'getsysinfo -s | sed \'s/^/====/g\' | sed \'s/$/====/g\'', '获取 服务器型号 服务标签 快速服务代码 操作系统 电源状态 网卡等等命令');
INSERT INTO `racadm_command` VALUES ('achieve_sensorinfo', 'getsensorinfo | sed \'s/^/====/g\' | sed \'s/$/====/g\'', '获取传感器信息(包含：cpu 内存 温度 风扇 硬盘 主板等等)');
INSERT INTO `racadm_command` VALUES ('achieve_System_LCD', 'get System.LCD | grep \'#CurrentDisplay\' |sed \'s/^#//g\'', '获取前面板信息命令');
INSERT INTO `racadm_command` VALUES ('test_connect', 'get BIOS.SysInformation.SystemServiceTag | grep -w SystemServiceTag', '测试链接是否可用');

-- ----------------------------
-- Table structure for `remote_card_info`
-- ----------------------------
DROP TABLE IF EXISTS `remote_card_info`;
CREATE TABLE `remote_card_info` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '远程管理卡id',
  `card_type_name` varchar(20) NOT NULL COMMENT '远程管理卡品牌类型',
  `card_user_name` varchar(20) NOT NULL COMMENT '远程管理卡用户名',
  `card_user_passwd` varchar(100) NOT NULL COMMENT '远程管理卡密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='本表记录远程管理卡的型号 远程用户名 密码';

-- ----------------------------
-- Records of remote_card_info
-- ----------------------------
INSERT INTO `remote_card_info` VALUES ('1', 'DELL', 'root', 'calvin');

-- ----------------------------
-- Table structure for `sensor_status_state`
-- ----------------------------
DROP TABLE IF EXISTS `sensor_status_state`;
CREATE TABLE `sensor_status_state` (
  `disk_state_name` varchar(20) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  PRIMARY KEY (`disk_state_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用来解释 racadm 获取的字段是用来做什么的';

-- ----------------------------
-- Records of sensor_status_state
-- ----------------------------
INSERT INTO `sensor_status_state` VALUES ('更改时间', 'check_time');
INSERT INTO `sensor_status_state` VALUES ('IP地址', 'ip_addr');
INSERT INTO `sensor_status_state` VALUES ('灾难级别最小阈值', 'Sensor_lc');
INSERT INTO `sensor_status_state` VALUES ('警告级别最小阈值', 'Sensor_lnc');
INSERT INTO `sensor_status_state` VALUES ('名称', 'Sensor_Name');
INSERT INTO `sensor_status_state` VALUES ('PWM', 'Sensor_PWM');
INSERT INTO `sensor_status_state` VALUES ('当前值', 'Sensor_Reading');
INSERT INTO `sensor_status_state` VALUES ('状况', 'Sensor_State');
INSERT INTO `sensor_status_state` VALUES ('状态', 'Sensor_Status');
INSERT INTO `sensor_status_state` VALUES ('类型', 'Sensor_Type');
INSERT INTO `sensor_status_state` VALUES ('灾难级别最大阈值', 'Sensor_uc');
INSERT INTO `sensor_status_state` VALUES ('警告级别最大阈值', 'Sensor_unc');

-- ----------------------------
-- Table structure for `System_AND_Nic_status_state`
-- ----------------------------
DROP TABLE IF EXISTS `System_AND_Nic_status_state`;
CREATE TABLE `System_AND_Nic_status_state` (
  `disk_state_name` varchar(20) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  PRIMARY KEY (`disk_state_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用来解释 racadm 获取的字段是用来做什么的';

-- ----------------------------
-- Records of System_AND_Nic_status_state
-- ----------------------------
INSERT INTO `System_AND_Nic_status_state` VALUES ('更改时间', 'check_time');
INSERT INTO `System_AND_Nic_status_state` VALUES ('快速服务代码', 'Express_Svc_Code');
INSERT INTO `System_AND_Nic_status_state` VALUES ('新鲜空气能力', 'Fresh_Air_Capable');
INSERT INTO `System_AND_Nic_status_state` VALUES ('系统主机名', 'Host_Name');
INSERT INTO `System_AND_Nic_status_state` VALUES ('IP地址', 'ip_addr');
INSERT INTO `System_AND_Nic_status_state` VALUES ('网卡MAC地址', 'NIC_MAC');
INSERT INTO `System_AND_Nic_status_state` VALUES ('网卡名称', 'NIC_name');
INSERT INTO `System_AND_Nic_status_state` VALUES ('网卡类型', 'NIC_type');
INSERT INTO `System_AND_Nic_status_state` VALUES ('操作系统', 'OS_Name');
INSERT INTO `System_AND_Nic_status_state` VALUES ('操作系统版本', 'OS_Version');
INSERT INTO `System_AND_Nic_status_state` VALUES ('电源状态', 'Power_Status');
INSERT INTO `System_AND_Nic_status_state` VALUES ('服务标签', 'Service_Tag');
INSERT INTO `System_AND_Nic_status_state` VALUES ('BIOS 版本', 'System_BIOS_Version');
INSERT INTO `System_AND_Nic_status_state` VALUES ('前面板LED', 'System_LCD_CurrentDisplay');
INSERT INTO `System_AND_Nic_status_state` VALUES ('系统型号', 'System_Model');
INSERT INTO `System_AND_Nic_status_state` VALUES ('系统修订', 'System_Revision');

-- ----------------------------
-- Table structure for `System_info`
-- ----------------------------
DROP TABLE IF EXISTS `System_info`;
CREATE TABLE `System_info` (
  `ip_addr_id` int(100) NOT NULL,
  `ip_addr` varchar(50) NOT NULL,
  `check_time` varchar(50) NOT NULL DEFAULT '',
  `System_Model` varchar(50) DEFAULT 'N/A',
  `System_Revision` varchar(50) DEFAULT 'N/A',
  `System_BIOS_Version` varchar(50) DEFAULT 'N/A',
  `Service_Tag` varchar(50) DEFAULT 'N/A',
  `Express_Svc_Code` varchar(50) DEFAULT 'N/A',
  `Host_Name` varchar(50) DEFAULT 'N/A',
  `OS_Name` varchar(50) DEFAULT 'N/A',
  `OS_Version` varchar(50) DEFAULT 'N/A',
  `Power_Status` varchar(50) DEFAULT 'N/A',
  `Fresh_Air_Capable` varchar(50) DEFAULT 'N/A',
  `System_LCD_CurrentDisplay` varchar(1000) DEFAULT '无法获取',
  KEY `disk_name` (`System_Model`) USING BTREE,
  KEY `ip_addr_id` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `System_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 System Information 信息';

-- ----------------------------
-- Records of System_info
-- ----------------------------

-- ----------------------------
-- Table structure for `System_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `System_status_info`;
CREATE TABLE `System_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `disk_name` varchar(100) NOT NULL,
  `disk_state_key` varchar(100) NOT NULL,
  `disk_state_value` varchar(100) NOT NULL,
  UNIQUE KEY `ip_addr_id_2` (`ip_addr_id`,`disk_state_key`,`disk_name`) USING BTREE,
  KEY `disk_name` (`disk_name`) USING BTREE,
  KEY `ip_addr_id` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `System_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录网卡状态信息';

-- ----------------------------
-- Records of System_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `Temp_status_info`
-- ----------------------------
DROP TABLE IF EXISTS `Temp_status_info`;
CREATE TABLE `Temp_status_info` (
  `ip_addr_id` int(100) NOT NULL,
  `check_time` varchar(50) NOT NULL,
  `Sensor_Name` varchar(50) NOT NULL,
  `Sensor_Status` varchar(20) NOT NULL,
  `Sensor_Reading` varchar(50) NOT NULL,
  `Sensor_lnc` varchar(20) NOT NULL DEFAULT '',
  `Sensor_unc` varchar(20) NOT NULL DEFAULT '',
  `Sensor_lc` varchar(20) NOT NULL,
  `Sensor_uc` varchar(20) NOT NULL,
  KEY `Temp_status_info_ibfk_1` (`ip_addr_id`) USING BTREE,
  CONSTRAINT `Temp_status_info_ibfk_1` FOREIGN KEY (`ip_addr_id`) REFERENCES `monitored_ipaddr` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='本表记录 温度 传感器信息';

-- ----------------------------
-- Records of Temp_status_info
-- ----------------------------

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL COMMENT 'ç”¨æˆ·å',
  `name_cn` varchar(50) NOT NULL COMMENT 'ä¸­æ–‡å',
  `password` varchar(50) NOT NULL COMMENT 'ç”¨æˆ·å¯†ç ',
  `email` varchar(50) DEFAULT NULL COMMENT 'ç”µå­é‚®ä»¶',
  `mobile` varchar(11) NOT NULL COMMENT 'æ‰‹æœºå·ç ',
  `role` varchar(10) NOT NULL COMMENT '1:sa;2:php;3:ios;4:test',
  `status` tinyint(4) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL COMMENT 'åˆ›å»ºæ—¶é—´',
  `last_time` datetime DEFAULT NULL COMMENT 'æœ€åŽç™»å½•æ—¶é—´',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=latin1 COMMENT='ç”¨æˆ·è¡¨';

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('67', 'youku', 'youku', '4cba3a57c5fa5468032f6ae8c096c40c', 'aiqiyi@huiselantian.com', '13813859138', 'admin', '0', null, null);

-- ----------------------------
-- Table structure for `warning_toolkit_table`
-- ----------------------------
DROP TABLE IF EXISTS `warning_toolkit_table`;
CREATE TABLE `warning_toolkit_table` (
  `toolkit_name` varchar(50) NOT NULL COMMENT '接口名称',
  `toolkit_url` varchar(200) NOT NULL COMMENT '接口url',
  `toolkit_key` varchar(100) NOT NULL COMMENT '接口key',
  `remarks` text COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用来发送报警的接口\r\n\r\n因钉钉机器人调用频率的限制问题，取消主键。\r\n改为按照toolkit_name取出所有，然后随机选择一个';

-- ----------------------------
-- Records of warning_toolkit_table
-- ----------------------------
INSERT INTO `warning_toolkit_table` VALUES ('offline_ding_talk', 'https://oapi.dingtalk.com/robot/send?access_token=', '998996995994', '线下服务器_钉钉机器人');

-- ----------------------------
-- Table structure for `warning_use_tmp_table`
-- ----------------------------
DROP TABLE IF EXISTS `warning_use_tmp_table`;
CREATE TABLE `warning_use_tmp_table` (
  `ip_addr` varchar(50) NOT NULL COMMENT '要告警检测的字段',
  `warning_key` varchar(100) NOT NULL COMMENT '正常值',
  `warning_value` varchar(200) NOT NULL COMMENT '不是正常值要更改为的值'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of warning_use_tmp_table
-- ----------------------------
