import json
import logging 
import os

conf = {
    "log_level": "INFO",
    "host": "127.0.0.1",
    "port": os.environ.get("PORT", 5000),
    "database_name": "",
    "database_uri": "",
    "expire_time": 120,
    "emailname": "",
    "emailpassword": ""
}

def initialize(config_file):
    with open(config_file) as f:
        conf_in_file = json.load(f)
        for k,v in conf_in_file.items():
            if k in conf:
                conf[k] = v
    log_level = logging.INFO
    if conf['log_level'].upper() == 'DEBUG':
        log_level = logging.DEBUG
    elif conf['log_level'].upper() == 'WARNING':
        log_level = logging.WARNING
    elif conf['log_level'].upper() == 'ERROR':
        log_level = logging.ERROR
    else:
        print ('Unknown logging level in config: {}. Will use INFO'.format(conf['log_level']))
        conf['log_level'] = 'INFO'
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')