import logging
import logging.handlers
import sys

class Logger:

    def __init__(self):


        logger = logging.getLogger()
        # Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
        logger.setLevel(logging.NOTSET)
        # Add stdout handler, with level INFO
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        # Add file rotating handler, with level INFO
        rotatingHandler = logging.handlers.RotatingFileHandler(filename='./hecc.log',
                                                               maxBytes=1000000,
                                                               backupCount=5)
        rotatingHandler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        rotatingHandler.setFormatter(formatter)
        logging.getLogger().addHandler(console)
        logging.getLogger().addHandler(rotatingHandler)

        self.log = logging.getLogger("hecc.py")
