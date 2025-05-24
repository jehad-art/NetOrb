from .base_rules import BASE_RULES
from .router_rules import ROUTER_RULES
from .switch_rules import SWITCH_RULES

def analyze_config(sections: dict, device_type: str) -> dict:
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

    # Merge rules
    rules = {
        "misconfigurations": BASE_RULES.get("misconfigurations", []) + DEVICE_RULES.get("misconfigurations", []),
        "missing_recommendations": BASE_RULES.get("missing_recommendations", []) + DEVICE_RULES.get("missing_recommendations", [])
    }

    misconfigurations = []
    missing_recommendations = []

    for rule in rules["misconfigurations"]:
        try:
            if rule["check"](sections):
                misconfigurations.append(rule)
        except Exception as e:
            print(f"[!] Rule error: {rule.get('tag', 'unknown')} - {e}")

    for rule in rules["missing_recommendations"]:
        try:
            if rule["check"](sections):
                missing_recommendations.append(rule)
        except Exception as e:
            print(f"[!] Rule error: {rule.get('tag', 'unknown')} - {e}")

    score = 100 - len(misconfigurations) * 10 - len(missing_recommendations) * 5

    return {
        "score": max(0, min(score, 100)),
        "misconfigurations": misconfigurations,
        "missing_recommendations": missing_recommendations,
        "rules_loaded": [r["tag"] for r in rules["misconfigurations"] + rules["missing_recommendations"]]
    }



def calculate_security_score(issues: list) -> int:
    weights = {"critical": 5, "high": 3, "medium": 2, "low": 1}
    score = sum(weights.get(issue["severity"], 1) for issue in issues)
    return max(100 - score, 0)
