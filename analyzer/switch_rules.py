SWITCH_RULES = {
    "misconfigurations": [
        {
            "id": "S01",
            "tag": "default_vlan_1_used",
            "severity": "medium",
            "description": "Interface assigned to default VLAN 1.",
            "check": lambda d: any(intf.get("vlan") == "1" for intf in d["parsed"].get("interfaces", []))
        },
        {
            "id": "S02",
            "tag": "trunk_port_without_tagging",
            "severity": "medium",
            "description": "Trunk port has no allowed VLANs specified.",
            "check": lambda d: any("switchport mode trunk" in line and not any("allowed vlan" in l for l in intf.get("lines", []))
                                   for intf in d["parsed"].get("interfaces", [])
                                   for line in intf.get("lines", []))
        },
        {
            "id": "S03",
            "tag": "bpdu_guard_not_enabled",
            "severity": "low",
            "description": "BPDU Guard is not enabled on access ports.",
            "check": lambda d: any("switchport mode access" in l and not any("bpduguard enable" in l for l in intf.get("lines", []))
                                   for intf in d["parsed"].get("interfaces", [])
                                   for l in intf.get("lines", []))
        },
        {
            "id": "S05",
            "tag": "stp_not_enabled",
            "severity": "high",
            "description": "Spanning Tree Protocol is not enabled.",
            "check": lambda d: not any("spanning-tree" in l.lower() for l in d["raw"])
        }
    ],
    "missing_recommendations": [
        {
            "id": "S04",
            "tag": "storm_control_missing",
            "severity": "medium",
            "description": "Storm control is not configured on interfaces.",
            "check": lambda d: all(not any("storm-control" in l for l in intf.get("lines", []))
                                   for intf in d["parsed"].get("interfaces", []))
        },
        {
            "id": "S06",
            "tag": "root_guard_not_enabled",
            "severity": "medium",
            "description": "Root Guard is not configured on any interface.",
            "check": lambda d: all(not any("spanning-tree guard root" in l for l in intf.get("lines", []))
                                for intf in d["parsed"].get("interfaces", []))
        }
    ]
}