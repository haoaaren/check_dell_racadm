#coding:utf-8
from flask import request,render_template, redirect,session
from . import app
from  dbutil import DB
import json
import hashlib



# 首页，个人中心
@app.route('/')
@app.route('/index')
def index():
   if not session.get('username',None):
        return redirect("/login")
   fields = ["id","name","name_cn","mobile","email","role","status"]
   where = {'name':session['username']}
   result = DB().get_one('users',fields,where)
   return  render_template('index.html',info=session,user=result)

