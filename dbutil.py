#!/usr/bin/env python
#coding=utf-8
from DBUtils.PooledDB import PooledDB 
import MySQLdb as mysql
from utils import util                                                                                        
import traceback
import config
import sys

class DB():
    def __init__(self):
        self.host = config.db_host
        self.name = config.db_name
        self.user = config.db_user
        self.passwd = config.db_passwd
        self.port = config.db_port
        self.pool = PooledDB(mysql, mincached=2, maxcached=50, host=self.host,db=self.name,user=self.user,port=self.port,passwd=self.passwd,setsession=['SET AUTOCOMMIT = 1'],charset="utf8")

    def connect_db(self):
        self.db = self.pool.connection()
        self.cur = self.db.cursor()

    def close_db(self):
        self.cur.close()
        self.db.close()

    def execute(self, sql):
        self.connect_db()
        return self.cur.execute(sql)
    
    def get_list(self,table,fields):
        sql = "select %s from %s"% (",".join(fields),table)
        try: 
            util.WriteLog('db').info("sql: %s" % sql)
            self.execute(sql)
            result = self.cur.fetchall()
            if result:
                result = [dict((k,row[i]) for i, k in enumerate(fields)) for row in result]
            else:
                result = {}
            return result;
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()

    def get_list_where(self,table,fields,where):
        if isinstance(where, dict) and where:
            conditions = []
            for k,v in where.items():
                conditions.append("%s='%s'" % (k, v))
        sql = "select %s from %s where %s" % (",".join(fields),table,' AND '.join(conditions))
        try: 
            util.WriteLog('db').info("sql: %s" % sql)
            self.execute(sql)
            result = self.cur.fetchall()
            if result:
                result = [dict((k,row[i]) for i, k in enumerate(fields)) for row in result]
            else:
                result = {}
            return result;
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()

    def get_list_where_and_not_where(self,table,fields,where,not_where):
        if isinstance(where, dict) and where:
            conditions = []
            for k,v in where.items():
                conditions.append("%s='%s'" % (k, v))
        if isinstance(not_where, dict) and not_where:
            conditions_1 = []
            for k,v in not_where.items():
                conditions_1.append("%s != '%s'" % (k, v))
        sql = "select %s from %s where %s AND %s" % (",".join(fields),table,' AND '.join(conditions),' AND '.join(conditions_1))
        try: 
            self.execute(sql)
            result = self.cur.fetchall()
            if result:
                result = [dict((k,row[i]) for i, k in enumerate(fields)) for row in result]
            else:
                result = {}
            return result;
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()

    def get_one(self,table,fields,where):
        if isinstance(where, dict) and where:
            conditions = []
            for k,v in where.items():
                conditions.append("%s='%s'" % (k, v))
        sql = "select %s from %s where %s" % (",".join(fields),table,' AND '.join(conditions))
        try:
            self.execute(sql)
            result = self.cur.fetchone()
            if result:
                result = dict((k, result[i])for i, k in enumerate(fields))
            else:
                result = {}
            return result
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()


    def update(self,table,fields):
        data = ",".join(["%s='%s'"%(k,v) for k,v in fields.items()])
        sql = "update %s set %s where id=%s " % (table,data,fields["id"])
        try:
            return self.execute(sql)
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()

    def update_where(self,table,fields,where):
        if isinstance(where, dict) and where:
            conditions = []
            for k,v in where.items():
                conditions.append("%s='%s'" % (k, v))
        data = " and ".join(["%s='%s'"%(k,v) for k,v in fields.items()])
        sql = "update %s set %s where %s " % (table,data,' AND '.join(conditions))
        try:
            return self.execute(sql)
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()

    def create(self,table,data):
        fields,values = [],[]
        for k, v in data.items():
            fields.append(k)
            values.append("'%s'" % v)
        sql = "insert into %s (%s) values (%s)" % (table,",".join(fields),",".join(values))
        #print sql
        try:
            return self.execute(sql)
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()

    def delete(self,table,where):
        if isinstance(where, dict) and where:
            conditions = []
            for k,v in where.items():
                conditions.append("%s='%s'" % (k, v))
        sql = "delete from %s where %s;" % (table,' AND '.join(conditions))
        try:
            #util.WriteLog('db').info("sql: %s" % sql)
            self.execute(sql)
            return self.execute(sql)
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()


    def check(self,table,fields,where):
        if isinstance(where, dict) and where:
            conditions = []
            for k,v in where.items():
                conditions.append("%s='%s'" % (k, v))
        sql = "select %s from %s where %s" % (','.join(fields),table,' AND '.join(conditions))
        try:
            self.execute(sql)
            result = self.cur.fetchone()
            if result:
                result = dict((k, result[i]) for i, k in enumerate(fields))
            else:
                result = ""
            return result
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()


    def check_more_id(self,table,fields,where):
        if isinstance(where, dict) and where:
            conditions = []
            for k,v in where.items():
                conditions.append("%s in (%s)" % (k, v))
        sql = "select %s from %s where %s" % (','.join(fields),table,' AND '.join(conditions))
        try:
            self.execute(sql)
            result = self.cur.fetchone()
            if result:
                result = dict((k, result[i]) for i, k in enumerate(fields))
            else:
                result = ""
            return result
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()


    def check_max_last_id(self,table,fields):
        sql = "select %s from %s where id=(select max(id) from %s)"% (",".join(fields),table,table)
        try:
            #util.WriteLog('db').info("sql: %s" % sql)
            self.execute(sql)
            result = self.cur.fetchone()
            if result:
                result = dict((k, result[i])for i, k in enumerate(fields))
            else:
                result = {}
            return result;
        except:
            util.WriteLog('db').info("Execute '%s' error: %s" % (sql, traceback.format_exc()))
        finally:
            self.close_db()

            

