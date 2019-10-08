#coding:utf-8
from app import app
import sys

reload(sys)

sys.setdefaultencoding('utf-8')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9094,debug=True,threaded=True)
