import logging
import sys
import os

ASCS_log_level = None

if 'LOG_LEVEL' in os.environ:
    ASCS_log_level = os.environ['LOG_LEVEL']
else:
    ASCS_log_level = logging.INFO

logging.basicConfig(level=ASCS_log_level,
                    stream=sys.stderr,
                    format='%(asctime)s %(name)s %(levelname)-5s %(message)s')

default_logger: logging.Logger = logging.getLogger('default')