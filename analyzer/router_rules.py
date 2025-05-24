import ipaddress

def is_private_ip(ip: str) -> bool:
    try:
        return ipaddress.IPv4Address(ip.split()[0]) in ipaddress.IPv4Network("10.0.0.0/8") \
            or ipaddress.IPv4Address(ip.split()[0]) in ipaddress.IPv4Network("192.168.0.0/16") \
            or ipaddress.IPv4Address(ip.split()[0]) in ipaddress.IPv4Network("172.16.0.0/12")
    except:
        return False

ROUTER_RULES = {
    "misconfigurations": [
        {
            "id": "R02",
            "tag": "vty_no_access_class",
            "severity": "medium",
            "description": "VTY lines have no access-class configured.",
            "check": lambda d: any("line vty" in l for b in d.get("parsed", {}).get("vty", []) for l in b) and
                              not any("access-class" in l for b in d.get("parsed", {}).get("vty", []) for l in b)
        },
        {
            "id": "R06",
            "tag": "empty_acl",
            "severity": "low",
            "description": "ACL exists but has no entries.",
            "check": lambda d: any(len(acl.get("entries", [])) == 0 for acl in d.get("access_lists", []))
        },
        {
            "id": "R07",
            "tag": "acl_no_deny_end",
            "severity": "medium",
            "description": "ACL does not end with a deny.",
            "check": lambda d: any(not acl["entries"][-1]["match"].lower().startswith("deny")
                                   for acl in d.get("access_lists", []) if acl.get("entries"))
        },
        {
            "id": "R08",
            "tag": "acl_permit_any",
            "severity": "high",
            "description": "ACL permits any traffic.",
            "check": lambda d: any("any" in e.get("match", "").lower() or "0.0.0.0" in e.get("match", "")
                                   for acl in d.get("access_lists", [])
                                   for e in acl.get("entries", []))
        },
        {
            "id": "R09",
            "tag": "nat_no_overload",
            "severity": "medium",
            "description": "NAT rule has no overload.",
            "check": lambda d: any(not r.get("overload") for r in d.get("parsed", {}).get("nat", []))
        },
        {
            "id": "R10",
            "tag": "nat_undefined_acl",
            "severity": "medium",
            "description": "NAT references undefined ACL.",
            "check": lambda d: any(r.get("acl") not in [a.get("name") for a in d.get("access_lists", [])]
                                   for r in d.get("parsed", {}).get("nat", []))
        },
        {
            "id": "R11",
            "tag": "nat_private_ip_exposed",
            "severity": "high",
            "description": "Private IP range exposed through NAT.",
            "check": lambda d: any(
                is_private_ip(src)
                for r in d.get("parsed", {}).get("nat", [])
                for src in [
                    s for acl in d.get("access_lists", [])
                    if acl.get("name") == r.get("acl")
                    for e in acl.get("entries", [])
                    if e.get("action") == "permit"
                    for s in [e.get("source", e.get("match"))]
                ]
            )
        },
        {
            "id": "R13",
            "tag": "rsa_key_weak",
            "severity": "high",
            "description": "RSA key is too weak (<2048).",
            "check": lambda d: any("crypto key generate rsa" in l and ("512" in l or "1024" in l)
                                   for l in d.get("raw", []))
        },
        {
            "id": "R14",
            "tag": "logging_buffered_disabled",
            "severity": "high",
            "description": "Buffered logging is disabled.",
            "check": lambda d: any("no logging buffered" in l for l in d.get("raw", []))
        },
        {
            "id": "R15",
            "tag": "logging_console_disabled",
            "severity": "medium",
            "description": "Console logging is disabled.",
            "check": lambda d: any("no logging console" in l for l in d.get("raw", []))
        },
        {
            "id": "R16",
            "tag": "username_plaintext_password",
            "severity": "medium",
            "description": "Username has a plaintext password and encryption is not enabled.",
            "check": lambda d: any("username " in l and " password " in l and "secret" not in l
                                   for l in d.get("raw", [])) and
                               not any("service password-encryption" in s
                                       for s in d.get("parsed", {}).get("services", []))
        },
    ],
    "missing_recommendations": [
        {
            "id": "R19",
            "tag": "usernames_missing",
            "severity": "high",
            "description": "No local usernames configured.",
            "check": lambda d: not d.get("parsed", {}).get("usernames")
        },
        {
            "id": "R20",
            "tag": "aaa_model_missing",
            "severity": "medium",
            "description": "AAA model is not enabled.",
            "check": lambda d: not d.get("parsed", {}).get("aaa")
        },
        {
            "id": "R21",
            "tag": "logging_buffer_missing",
            "severity": "high",
            "description": "No logging buffer is configured.",
            "check": lambda d: not any("logging buffered" in l for l in d.get("raw", []))
        },
        {
            "id": "R22",
            "tag": "vty_access_class_missing",
            "severity": "medium",
            "description": "VTY access-class is not configured.",
            "check": lambda d: any("line vty" in l for b in d.get("parsed", {}).get("vty", []) for l in b) and
                               not any("access-class" in l for b in d.get("parsed", {}).get("vty", []) for l in b)
        }
    ]
}
