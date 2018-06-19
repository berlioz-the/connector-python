from flask import Flask
import berlioz


berlioz.monitorPeers('service', 'app', 'client', lambda x: berlioz.logger.info(x))

# logger = berlioz.log.get('berlioz')
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello World!"

# if __name__ == '__main__':
#     app.run()
