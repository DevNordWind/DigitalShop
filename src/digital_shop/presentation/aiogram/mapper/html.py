from aiogram.types import MessageEntity
from aiogram.utils.text_decorations import html_decoration
from sulguk import transform_html


def map_html(value: str) -> str:
    transformed = transform_html(raw_html=value)

    entities = [
        MessageEntity(**entity)  # type: ignore[arg-type]
        for entity in transformed.entities
        if entity.get("length", 0) > 0
    ]
    return html_decoration.unparse(
        text=transformed.text,
        entities=entities,
    )
