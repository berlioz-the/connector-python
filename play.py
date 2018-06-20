import threading
from berlioz.utils import delay

def f():
    print 'RUNNING'


print '**************'
delay(1500, f)



# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello World!"

# if __name__ == '__main__':
#     app.run()
