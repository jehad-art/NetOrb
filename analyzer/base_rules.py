import re

BASE_RULES = {
    "misconfigurations": [
        {
            "id": "R01",
            "tag": "telnet_enabled",
            "severity": "high",
            "description": "Telnet is enabled on VTY lines.",
            "check": lambda d: any("transport input telnet" in l for b in d["parsed"].get("vty", []) for l in b)
        },
        {
            "id": "R03",
            "tag": "enable_plaintext",
            "severity": "high",
            "description": "Enable password is configured in plain text.",
            "check": lambda d: d["parsed"].get("enable", {}).get("type") == "password"
        },
        {
            "id": "R04",
            "tag": "password_no_encryption",
            "severity": "medium",
            "description": "Plain-text passwords found, but no encryption service enabled.",
            "check": lambda d: any("password " in l for l in d["raw"]) and
                                 not any("service password-encryption" in s for s in d["parsed"].get("services", []))
        },
        {
            "id": "R05",
            "tag": "snmp_default_community",
            "severity": "critical",
            "description": "SNMP uses default community string.",
            "check": lambda d: any(re.search(r"community (public|private)", l, re.I)
                                     for l in d["parsed"].get("snmp", []))
        },
        {
            "id": "R12",
            "tag": "ssh_v1_enabled",
            "severity": "high",
            "description": "SSH version 1 is enabled.",
            "check": lambda d: any("ip ssh version 1" in l.lower() for l in d["raw"])
        },
    ],
    "missing_recommendations": [
        {
            "id": "R17",
            "tag": "ssh_v2_missing",
            "severity": "high",
            "description": "SSH version 2 not configured.",
            "check": lambda d: not any("ip ssh version 2" in l for l in d["raw"])
        },
        {
            "id": "R18",
            "tag": "service_encryption_missing",
            "severity": "medium",
            "description": "Service password-encryption is not configured.",
            "check": lambda d: not any("service password-encryption" in s
                                         for s in d["parsed"].get("services", []))
        }
    ]
}
