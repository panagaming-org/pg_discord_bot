async def report_json_request(user, action, reason, evidence_url=[]):
    report_data = {
        "username": user.name,
        "action_type": action,
        "target_platform": "discord",
        "target_user_id": user.id,
        "reason": reason,
        "evidence_url": evidence_url,
        "active": True,
        "expires_at": ""
    }
    return report_data
    