import sys
from app import app, manager
from flask_restful import Api, reqparse
from logging.handlers import RotatingFileHandler
import logging, sys


api = Api(app, catch_all_404s=True)

if __name__ == "__main__":
    try:
        if sys.argv[1] == 'db':
            manager.run()
    except Exception as e:
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../logs/app.log'), maxBytes=10000000,
                                          backupCount=10)
        log_handler.setLevel(logging.NOTSET)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)
        # app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
        app.run(debug=True, host='0.0.0.0', port=5000)