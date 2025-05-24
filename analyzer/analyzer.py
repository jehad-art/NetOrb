from .base_rules import BASE_RULES
from .router_rules import ROUTER_RULES
from .switch_rules import SWITCH_RULES


def analyze_config(sections: dict, device_type: str) -> dict:
    print("[DEBUG] sections keys:", sections.keys())
    print("[DEBUG] raw_config sample:", sections.get("raw_config", [])[:5])
    print("[DEBUG] parsed_config keys:", sections.get("parsed_config", {}).keys())
    print("[DEBUG] normalized parsed enable:", normalized.get("parsed", {}).get("enable"))
    print("[DEBUG] normalized raw length:", len(normalized.get("raw", [])))

    from .base_rules import BASE_RULES

    try:
        if device_type == "router":
            from .router_rules import ROUTER_RULES as DEVICE_RULES
        elif device_type == "switch":
            from .switch_rules import SWITCH_RULES as DEVICE_RULES
        else:
            DEVICE_RULES = {"misconfigurations": [], "missing_recommendations": []}
    except Exception as e:
        print(f"[!] Failed to load rules for {device_type}: {e}")
        DEVICE_RULES = {"misconfigurations": [], "missing_recommendations": []}

    # Merge base + device-specific rules
    rules = {
        "misconfigurations": BASE_RULES.get("misconfigurations", []) + DEVICE_RULES.get("misconfigurations", []),
        "missing_recommendations": BASE_RULES.get("missing_recommendations", []) + DEVICE_RULES.get("missing_recommendations", [])
    }

    print("[Loaded misconfigs]:", [r["tag"] for r in rules["misconfigurations"]])
    print("[Loaded recs]:", [r["tag"] for r in rules["missing_recommendations"]])

    # Normalize input for consistent rule evaluation
    normalized = {
        "parsed": sections.get("parsed_config", {}),
        "raw": sections.get("raw_config", []),
        **sections
    }

    misconfigurations = []
    missing_recommendations = []

    for rule in rules["misconfigurations"]:
        try:
            result = rule["check"](normalized)
            print(f"[DEBUG] {rule['tag']} => {result}")  # Print match result
            if result:
                misconfigurations.append(rule)
        except Exception as e:
            print(f"[!] Rule error: {rule.get('tag', 'unknown')} - {e}")

    for rule in rules["missing_recommendations"]:
        try:
            result = rule["check"](normalized)
            print(f"[DEBUG] {rule['tag']} => {result}")  # Print match result
            if result:
                missing_recommendations.append(rule)
        except Exception as e:
            print(f"[!] Rule error: {rule.get('tag', 'unknown')} - {e}")

    def strip_check_field(rules):
        return [{k: v for k, v in rule.items() if k != "check"} for rule in rules]

    score = 100 - len(misconfigurations) * 10 - len(missing_recommendations) * 5

    return {
        "score": max(0, min(score, 100)),
        "misconfigurations": strip_check_field(misconfigurations),
        "missing_recommendations": strip_check_field(missing_recommendations),
        "rules_loaded": [r["tag"] for r in misconfigurations + missing_recommendations]
    }




def calculate_security_score(issues: list) -> int:
    weights = {"critical": 5, "high": 3, "medium": 2, "low": 1}
    score = sum(weights.get(issue["severity"], 1) for issue in issues)
    return max(100 - score, 0)
