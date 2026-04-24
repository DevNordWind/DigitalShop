from collections import deque
from decimal import Decimal

from domain.common.money import Currency

type Graph = dict[Currency, dict[Currency, Decimal]]


class ExchangeRateGraph:
    def __init__(self) -> None:
        self._graph: Graph = {}

    def add_rate(
        self,
        source: Currency,
        target: Currency,
        rate: Decimal,
    ) -> None:
        self._graph.setdefault(source, {})[target] = rate
        self._graph.setdefault(target, {})[source] = Decimal(1) / rate

    def find_rate(self, source: Currency, target: Currency) -> Decimal | None:
        if source == target:
            return Decimal("1.00")

        visited: set[Currency] = set()
        queue: deque[tuple[Currency, Decimal]] = deque(
            [(source, Decimal("1.00"))],
        )

        while queue:
            current, acc = queue.popleft()
            if current == target:
                return acc
            visited.add(current)
            for neighbor, rate in self._graph.get(current, {}).items():
                if neighbor not in visited:
                    queue.append((neighbor, acc * rate))

        return None

    def currencies(self) -> list[Currency]:
        return list(self._graph.keys())
