from typing import NewType

from taskiq import AsyncBroker

PriorityBroker = NewType("PriorityBroker", AsyncBroker)
