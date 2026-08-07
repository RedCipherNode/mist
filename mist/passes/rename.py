from __future__ import annotations

import secrets
import string

from mist.model import Symbol


class NameGenerator:
    def __init__(self) -> None:
        self._used: set[str] = set()

    def next(self) -> str:

        alphabet = string.ascii_letters + string.digits

        while True:
            name = "_" + "".join(secrets.choice(alphabet) for _ in range(12))

            if name not in self._used:
                self._used.add(name)
                return name


class RenamePass:
    def __init__(self) -> None:
        self.generator = NameGenerator()

    def rename(self, symbols: list[Symbol]) -> None:

        for symbol in symbols:
            symbol.obfuscated_name = self.generator.next()
