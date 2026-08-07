from typing import Any

from mist.core.base_pass import BasePass


class IdentityPass(BasePass):
    @property
    def name(self) -> str:
        return "identity"

    def apply(self, tree: Any, context: Any) -> Any:
        return tree
