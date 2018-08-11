import math

try:
    from pythonjsonlogger import jsonlogger
except ImportError as exc:
    raise ImportError('To use "{}" you must install "python-json-logger" package.'.format(__name__)) from exc


class StackdriverJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, fmt="%(levelname) %(message)", style="%", *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)

    def add_fields(self, log_record, record, message_dict):
        subsecond, second = math.modf(record.created)
        log_record.update(
            {
                "timestamp": {"seconds": int(second), "nanos": int(subsecond * 1e9)},
                "thread": record.thread,
                "severity": record.levelname,
            }
        )
        super().add_fields(log_record, record, message_dict)
