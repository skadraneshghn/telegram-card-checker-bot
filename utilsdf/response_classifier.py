"""
Response Classifier for Telegram Card Checker Bot.
Distinguishes between Card Validation Outcomes (Approved/Declined) and Gateway/Network Errors.
"""

def classify_response(status_raw: str, result_raw: str) -> tuple:
    """
    Parses status and result strings and classifies them into:
    (status_label, clean_result, is_approved, is_gateway_error)
    
    Status Labels:
    - Approved! ✅ (Card Approved / Charged)
    - CCN Live! 🟡 (CVC error / Insufficient funds - Card is valid)
    - Declined! ❌ (Bank Declined card)
    - Gateway Error! ⚠️ (Network / Proxy / Timeout / Gateway breakdown)
    """
    status_str = str(status_raw or "").strip()
    result_str = str(result_raw or "").strip()
    combined_lower = f"{status_str} {result_str}".lower()

    # 1. Check for Gateway System Errors
    gateway_error_keywords = [
        "timeout", "connecterror", "proxyerror", "httperror", "graphql", 
        "jsondecodeerror", "keyerror", "nameerror", "attributeerror", 
        "connection refused", "service unavailable", "bad gateway", 
        "gateway timeout", "cloudflare", "502 bad gateway", "503 service unavailable", 
        "500 internal server error", "403 forbidden", "site error", "proxy connection",
        "error:", "exception", "failed executing", "readtimedout", "connecttimeout"
    ]

    # Exclude normal bank error codes that might contain the word 'error' or 'code'
    bank_decline_keywords = [
        "card declined", "decline", "do not honor", "stolen", "lost", "expired",
        "invalid_number", "pickup", "restricted", "generic_decline", "insufficient_funds",
        "incorrect_cvc", "invalid_cvc", "security code", "avs", "card_not_supported"
    ]

    is_bank_decline = any(k in combined_lower for k in bank_decline_keywords)
    is_gateway_err = any(k in combined_lower for k in gateway_error_keywords) and not is_bank_decline

    if is_gateway_err or status_str == "Gateway Error":
        return (
            "Gateway Error! ⚠️",
            f"Gateway Issue: {result_str}",
            False,  # is_approved
            True    # is_gateway_error
        )

    # 2. Check for Approved / Live Cards
    approved_keywords = [
        "approved", "charged", "thank you", "succeeded", "success", "1000", "00"
    ]
    ccn_live_keywords = [
        "insufficient funds", "incorrect cvc", "security code is incorrect", 
        "cvc_check: fail", "2001", "zip code", "avs mismatch", "insufficient_funds",
        "invalid cvc", "street address"
    ]

    if any(k in combined_lower for k in approved_keywords):
        return (
            "Approved! ✅",
            result_str if result_str else "Transaction Approved",
            True,   # is_approved
            False   # is_gateway_error
        )

    if any(k in combined_lower for k in ccn_live_keywords):
        return (
            "CCN Live! 🟡",
            result_str if result_str else "Card Valid (CVC/Funds Issue)",
            True,   # Live card
            False
        )

    # 3. Default to Declined
    return (
        "Declined! ❌",
        result_str if result_str else "Card Declined by Issuer",
        False,
        False
    )
