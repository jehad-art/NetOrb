from analyzer.router_rules import RULES

def analyze_config(sections: dict) -> dict:
    parsed = sections.get("parsed_config", {})
    raw = sections.get("raw_config", [])
    access_lists = sections.get("access_lists", [])
    data = {
        "parsed": parsed,
        "raw": raw,
        "access_lists": access_lists,
        "sections": sections
    }

    misconfigurations = []
    missing_recommendations = []

    for rule in RULES["misconfigurations"]:
        try:
            if rule["check"](data):
                misconfigurations.append({
                    "type": rule["id"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "category": "misconfiguration"
                })
        except Exception as e:
            print(f"[!] Error in rule {rule['id']}: {e}")

    for rule in RULES["missing_recommendations"]:
        try:
            if rule["check"](data):
                missing_recommendations.append({
                    "type": rule["id"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "category": "missing_recommendation"
                })
        except Exception as e:
            print(f"[!] Error in rule {rule['id']}: {e}")

    issues = misconfigurations + missing_recommendations
    return {
        "misconfigurations": misconfigurations,
        "missing_recommendations": missing_recommendations,
        "score": calculate_security_score(issues)
    }

    

def calculate_security_score(issues: list) -> int:
    weights = {"critical": 5, "high": 3, "medium": 2, "low": 1}
    score = sum(weights.get(issue["severity"], 1) for issue in issues)
    return max(100 - score, 0)