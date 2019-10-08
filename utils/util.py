#/usr/bin/env python
#coding:utf-8
import logging
import logging.handlers
import config

def WriteLog(log_name):
    log_file = "%s/sql_run.log"%(config.log_dir)
    log_level = logging.DEBUG
    # 定义日志格式
    format = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)2d]-%(funcName)s  %(levelname)s %(message)s')
    handler = logging.handlers.RotatingFileHandler(log_file, mode='a', maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(format)
    # 实例化日志对象
    logger = logging.getLogger(log_name)
    if not logger.handlers:
        logger.addHandler(handler)
        logger.setLevel(log_level)
    return logger
