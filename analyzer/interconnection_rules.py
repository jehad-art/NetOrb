# interconnection_rules.py

def find_trunk_mismatches(all_configs: list) -> list:
    issues = []

    device_map = {cfg["device_ip"]: cfg for cfg in all_configs}

    for device in all_configs:
        device_ip = device["device_ip"]
        hostname = device.get("hostname", device_ip)
        interfaces = device["sections"].get("interfaces", [])

        for iface in interfaces:
            local_port = iface.get("name")
            local_mode = iface.get("mode", "").lower()
            neighbor_info = iface.get("cdp_neighbor", {})

            if not neighbor_info:
                continue

            neighbor_id = neighbor_info.get("device_id")
            neighbor_port = neighbor_info.get("port_id")

            # Find matching peer
            for peer in all_configs:
                peer_hostname = peer.get("hostname", peer["device_ip"])
                if neighbor_id in peer_hostname:
                    for peer_iface in peer["sections"].get("interfaces", []):
                        if peer_iface.get("name") == neighbor_port:
                            peer_mode = peer_iface.get("mode", "").lower()
                            if local_mode != peer_mode:
                                issues.append({
                                    "id": "INT01",
                                    "category": "interconnection_misconfiguration",
                                    "severity": "high",
                                    "description": f"Trunk mismatch: {hostname}({local_port}) is {local_mode}, "
                                                   f"but {peer_hostname}({neighbor_port}) is {peer_mode or 'unknown'}."
                                })
                            break
                    break
    return issues


def analyze_interconnections(all_configs: list) -> dict:
    return {
        "interconnection_issues": find_trunk_mismatches(all_configs)
    }
