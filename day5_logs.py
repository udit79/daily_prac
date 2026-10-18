from enum import Enum
class levels(Enum):
    INFO="INFO"
    WARNING="WARNING"
    ERROR="ERROR"
    DEBUG="DEBUG"
allowed_levels=[level.value for level in levels if level!=levels.DEBUG]
print(allowed_levels)
repeated_logs = [
    {"service": "api", "level": "INFO", "event": "request_received"},
    {"service": "api", "level": "INFO", "event": "request_received"},
    {"service": "api", "level": "ERROR", "event": "request_failed"},
]
logs = [
    {"service": "auth", "level": "INFO", "event": "login_success"},
    {"service": "auth", "level": "ERROR", "event": "login_failed"},
    {"service": "payments", "level": "INFO", "event": "payment_created"},
    {"service": "auth", "level": "INFO", "event": "login_success"},
    {"service": "payments", "level": "ERROR", "event": "payment_failed"},
    {"service": "auth", "level": "DEBUG", "event": "token_refreshed"},
    {"service": "payments", "level": "INFO", "event": "payment_created"},
    {"service": "payments", "level": "INFO", "event": "payment_created"},
    {"service": "auth", "level": "WARNING", "event": "password_expiring"},
    {"service": "auth", "level": "ERROR", "event": "login_failed"},
    {"service": "orders", "level": "INFO", "event": "order_created"},
    {"service": "orders", "level": "ERROR", "event": "order_failed"},
]
debug_logs = [
    {"service": "auth", "level": "DEBUG", "event": "token_refreshed"},
    {"service": "payments", "level": "DEBUG", "event": "cache_hit"},
]
def count_service_events(logs:list[dict]|list)->dict[str,dict[str,int]]|dict:
    final_report={}
    for log in logs:
        service=log["service"]
        event=log["event"]
        if log["level"] in allowed_levels:
            if service in final_report:
                field=final_report[service]
            else:
                field={}
            field[event]=field.get(event,0)+1
            final_report[service]=field
    return final_report
print(f"case1:\n\tDataset:\n\t\t{logs}\n\tResult:\n\t\t{count_service_events(logs)}")
print(f"case2:\n\tDataset:\n\t\t{{}}\n\tResult:\n\t\t{count_service_events([])}")
print(f"case3:\n\tDataset:\n\t\t{debug_logs}\n\tResult:\n\t\t{count_service_events(debug_logs)}")
print(f"case4:\n\tDataset:\n\t\t{repeated_logs}\n\tResult:\n\t\t{count_service_events(repeated_logs)}")