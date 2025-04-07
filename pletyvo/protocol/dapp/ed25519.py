# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "Schema",
    "ED25519",
)

import typing

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from . import abc
from .auth_header import AuthHeader
from .hash import Hash

if typing.TYPE_CHECKING:
    from os import PathLike


class Schema:
    ED25519 = 1


class ED25519(abc.Signer):
    def __init__(self, seed: typing.Optional[bytes] = None) -> None:
        self._privatek = (
            Ed25519PrivateKey.from_private_bytes(seed)
            if seed
            else Ed25519PrivateKey.generate()
        )
        self._publik = self._privatek.public_key()

    @classmethod
    def from_file(cls, path: str | PathLike[str]) -> ED25519:
        with open(path, "rb") as f:
            return cls(f.read())

    @classmethod
    def schema(cls) -> int:
        return Schema.ED25519

    def sign(self, msg: bytes) -> bytes:
        return self._privatek.sign(msg)

    def public(self) -> bytes:
        return self._publik.public_bytes_raw()

    def hash(self) -> Hash:
        return Hash.gen(
            sch=self.schema(),
            data=self.public(),
        )

    def auth(self, msg: bytes) -> AuthHeader:
        return AuthHeader(
            sch=self.schema(),
            pub=self.public(),
            sig=self.sign(msg),
        )
