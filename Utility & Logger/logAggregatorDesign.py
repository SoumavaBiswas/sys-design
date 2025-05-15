from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from typing import List, Optional
import uuid

"""
LogEntry: Represents a single log.

LogProducer: Service that emits logs.

LogAggregator: Central system that ingests and stores logs.

LogStore: Storage backend (in-memory or persistent).

LogConsumer: Service querying logs.
"""


@dataclass
class LogEntry:
    log_id: str
    timestamp: datetime
    service_name: str
    level: str  # e.g., INFO, ERROR, DEBUG
    message: str


class LogStore:
    def __init__(self):
        self.logs: List[LogEntry] = []
        self.lock = Lock()

    def add_log(self, entry: LogEntry):
        with self.lock:
            self.logs.append(entry)

    def query_logs(
        self,
        service_name: Optional[str] = None,
        level: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> List[LogEntry]:
        with self.lock:
            result = self.logs
            if service_name:
                result = [log for log in result if log.service_name == service_name]
            if level:
                result = [log for log in result if log.level == level]
            if start:
                result = [log for log in result if log.timestamp >= start]
            if end:
                result = [log for log in result if log.timestamp <= end]
            return result


class LogAggregator:
    def __init__(self):
        self.store = LogStore()

    def receive_log(self, service_name: str, level: str, message: str):
        entry = LogEntry(
            log_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            service_name=service_name,
            level=level,
            message=message
        )
        self.store.add_log(entry)

    def query_logs(self, **kwargs) -> List[LogEntry]:
        return self.store.query_logs(**kwargs)


class LogProducer:
    def __init__(self, service_name: str, aggregator: LogAggregator):
        self.service_name = service_name
        self.aggregator = aggregator

    def log(self, level: str, message: str):
        self.aggregator.receive_log(self.service_name, level, message)


class LogConsumer:
    def __init__(self, aggregator: LogAggregator):
        self.aggregator = aggregator

    def fetch_logs(self, **kwargs) -> List[LogEntry]:
        return self.aggregator.query_logs(**kwargs)


aggregator = LogAggregator()
serviceA = LogProducer("AuthService", aggregator)
serviceB = LogProducer("PaymentService", aggregator)
consumer = LogConsumer(aggregator)

serviceA.log("INFO", "User login successful")
serviceB.log("ERROR", "Payment gateway timeout")

logs = consumer.fetch_logs(level="ERROR")
for log in logs:
    print(log)
