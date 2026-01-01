from passes.rename_identifiers import obfuscate_code
from passes.strings_obfuscation import obfuscate_strings
from core.level_policy import LEVEL_POLICIES


AVAILABLE_PASSES = {
    "rename_identifiers": obfuscate_code,
    "string_obfuscation": obfuscate_strings
}


def apply_passes(source_code, config):
    result = source_code
    level = config.get("level", "medium")
    policy = LEVEL_POLICIES.get(level, {})

    for name, enabled in config["passes"].items():
        if not enabled:
            continue

        if name not in AVAILABLE_PASSES:
            continue

        if name == "rename_identifiers":
            options = policy.get("rename_identifiers", {})
            result = AVAILABLE_PASSES[name](result, options)

        elif name == "string_obfuscation":
            if not policy.get("string_obfuscation", False):
                continue
            result = AVAILABLE_PASSES[name](result)

    return result
