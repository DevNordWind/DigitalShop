from collections.abc import Sequence

from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.factory import FulfillmentStrategyFactory
from app.domain.shopping.position.item.value_object import ItemSnapshot
from app.domain.shopping.position.strategy import FulfillmentStrategy
from app.domain.shopping.position.value_object import HoldContext, SellContext


class PositionFulfillmentDomainService:
    def __init__(
        self,
        factory: FulfillmentStrategyFactory,
    ):
        self._factory = factory

    async def hold(
        self, position: Position, ctx: HoldContext
    ) -> tuple[ItemSnapshot, ...]:
        position.ensure_not_archived()
        fulfillment: FulfillmentStrategy = await self._factory.create(
            tp=position.fulfillment_type
        )

        return await fulfillment.hold(position=position, ctx=ctx)

    async def sell(
        self, position: Position, snapshots: Sequence[ItemSnapshot], ctx: SellContext
    ) -> None:
        fulfillment: FulfillmentStrategy = await self._factory.create(
            tp=position.fulfillment_type
        )
        await fulfillment.sell(snapshots=snapshots, ctx=ctx)

    async def rollback(
        self,
        position: Position,
        snapshots: Sequence[ItemSnapshot],
    ) -> None:
        fulfillment: FulfillmentStrategy = await self._factory.create(
            tp=position.fulfillment_type
        )
        await fulfillment.rollback(snapshots=snapshots)
