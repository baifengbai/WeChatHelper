#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import os
import logging
from logging.handlers import RotatingFileHandler

# logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')])
def getMyLogger(name=None, fn=None, level=None):
    logger = logging.getLogger(name)
    if fn != None:
        if level != None:
            logger.setLevel(level)
        else:
            logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                                    "%Y-%m-%d %H:%M")
        # create console handler and set level to debug
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logfn = 'logs\\'+os.path.basename(fn).replace('.json', '.log')
        # handler = RotatingFileHandler(logfn, maxBytes=100000, backupCount=1)
        handler = logging.FileHandler(logfn, 'a', 'utf-8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
