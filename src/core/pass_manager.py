from passes.rename_identifiers import obfuscate_code
from passes.strings_obfuscation import obfuscate_strings


AVAILABLE_PASSES = {
    "rename_identifiers": obfuscate_code,
    "string_obfuscation": obfuscate_strings
}


def apply_passes(source_code, config):
    result = source_code

    for name, enabled in config["passes"].items():
        if not enabled:
            continue

        if name not in AVAILABLE_PASSES:
            continue

        result = AVAILABLE_PASSES[name](result)

    return result
