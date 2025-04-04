# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "HashService",
    "EventService",
    "DappService",
)

import typing

from pletyvo.protocol import dapp
from pletyvo.types import uuidlike_as_uuid
from pletyvo.serializer import to_dict

if typing.TYPE_CHECKING:
    from . import abc
    from pletyvo.types import (
        QueryOption,
        JSONType,
        UUIDLike,
    )


class HashService(dapp.abc.HashService):
    def __init__(self, engine: abc.HTTPClient) -> None:
        self._engine = engine

    async def get_by_id(self, id: dapp.Hash) -> dapp.EventResponse:
        response: JSONType = await self._engine.get(f"/api/dapp/v1/hash/{id}")
        return dapp.EventResponse.from_dict(response)


class EventService(dapp.abc.EventService):
    def __init__(self, engine: abc.HTTPClient) -> None:
        self._engine = engine

    async def get(
        self, option: typing.Optional[QueryOption] = None
    ) -> list[dapp.Event]:
        response: JSONType = await self._engine.get(
            f"/api/dapp/v1/events{option or ''}"
        )
        return [dapp.Event.from_dict(d=event) for event in response]  # type: ignore

    async def get_by_id(self, id: UUIDLike) -> dapp.Event:
        response: JSONType = await self._engine.get(
            f"/api/dapp/v1/events/{uuidlike_as_uuid(id)}"
        )
        return dapp.Event.from_dict(response)

    async def create(self, input: dapp.EventInput) -> dapp.EventResponse:
        response: JSONType = await self._engine.post(
            "/api/dapp/v1/events", body=to_dict(input)
        )
        return dapp.EventResponse.from_dict(response)


class DappService:
    __slots__: typing.Sequence[str] = ("hash", "event")

    def __init__(self, engine: abc.HTTPClient):
        self.hash = HashService(engine)
        self.event = EventService(engine)
