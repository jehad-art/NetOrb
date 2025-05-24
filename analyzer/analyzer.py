from .base_rules import BASE_RULES
from .router_rules import ROUTER_RULES
from .switch_rules import SWITCH_RULES

RULE_MAP = {
    "router": {
        "misconfigurations": BASE_RULES["misconfigurations"] + ROUTER_RULES["misconfigurations"],
        "missing_recommendations": BASE_RULES["missing_recommendations"] + ROUTER_RULES["missing_recommendations"]
    },
    "switch": {
        "misconfigurations": BASE_RULES["misconfigurations"] + SWITCH_RULES["misconfigurations"],
        "missing_recommendations": BASE_RULES["missing_recommendations"] + SWITCH_RULES["missing_recommendations"]
    }
}

def analyze_config(sections: dict, device_type: str) -> dict:
    from .base_rules import BASE_RULES
    try:
        if device_type == "router":
            from .router_rules import ROUTER_RULES as DEVICE_RULES
        elif device_type == "switch":
            from .switch_rules import SWITCH_RULES as DEVICE_RULES
        else:
            DEVICE_RULES = {}
    except Exception as e:
        print(f"[!] Failed to load rules for {device_type}: {e}")
        DEVICE_RULES = {}

    rules = {**BASE_RULES, **DEVICE_RULES}

    misconfigurations = []
    missing_recommendations = []

    for rule_name, rule_func in rules.items():
        try:
            result = rule_func(sections)
            if result and isinstance(result, dict):
                if result.get("type") == "recommendation":
                    missing_recommendations.append(result)
                else:
                    misconfigurations.append(result)
        except Exception as e:
            print(f"[!] Rule error: {rule_name} - {e}")

    score = 100 - len(misconfigurations) * 10 - len(missing_recommendations) * 5

    return {
        "score": max(0, min(score, 100)),
        "misconfigurations": misconfigurations,
        "missing_recommendations": missing_recommendations,
        "rules_loaded": list(rules.keys())
    }


def calculate_security_score(issues: list) -> int:
    weights = {"critical": 5, "high": 3, "medium": 2, "low": 1}
    score = sum(weights.get(issue["severity"], 1) for issue in issues)
    return max(100 - score, 0)
