import datetime
import time

from flask import request
from pythonjsonlogger import jsonlogger


class ElkJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON Formatter used by the web application to log requests.
    Adds some request properties and debugging information.

    Based on code from:
    - https://logz.io/blog/python-logs-elk-elastic-stack/
    - https://github.com/eht16/python-logstash-async/blob/master/logstash_async/formatter.py
    """

    def add_fields(self, log_record, record, message_dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

        debugging_fields = {
            'func_name': record.funcName,
            'line': record.lineno,
            'path': record.pathname,
            'process_name': record.processName,
            'thread_name': record.threadName,
        }
        log_record['debugging_info'] = debugging_fields

        if request:
            request_fields = {}
            request_fields['useragent'] = str(request.user_agent) if request.user_agent else ''
            request_fields['remote_address'] = request.remote_addr
            request_fields['host'] = request.host.split(':', 1)[0]
            request_fields['path'] = request.path
            request_fields['uri'] = request.url
            request_fields['method'] = request.method
            request_fields['data'] = request.get_data().decode('utf-8').strip()
            request_fields['timestamp'] = self._format_timestamp(time.time())
            log_record['request'] = request_fields

    def _format_timestamp(self, time_):
        tstamp = datetime.datetime.utcfromtimestamp(time_)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (tstamp.microsecond / 1000) + "Z"
