#coding:utf-8
from flask import Flask


app = Flask(__name__)

app.secret_key = "UIsadl;oi3&*(&9023sd"

import users
import demo
import dell_racadm
import dell_racadm_disk
import dell_racadm_toolkit
import dell_racadm_warning
import dell_racadm_info_update
import dell_racadm_page
