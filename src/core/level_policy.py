LEVEL_POLICIES = {
    "low": {
        "rename_identifiers": {
            "rename_functions": True,
            "rename_variables": False
        },
        "string_obfuscation": False
    },
    "medium": {
        "rename_identifiers": {
            "rename_functions": True,
            "rename_variables": True
        },
        "string_obfuscation": True
    },
    "high": {
        "rename_identifiers": {
            "rename_functions": True,
            "rename_variables": True
        },
        "string_obfuscation": True
    }
}
