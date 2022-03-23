# -*- coding: utf-8 -*-
"""
Service handler module for AWS Lambda function. 'HANDLERS' constant dict is
used to map route requests to correct handler.
"""

import logging
from lib.config import LOG_LEVEL
from lib.routes import root

if LOG_LEVEL in ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'):
    level = logging.getLevelName(LOG_LEVEL)
else:
    level = logging.INFO

logging.basicConfig(level=level)
handler = root.handler
