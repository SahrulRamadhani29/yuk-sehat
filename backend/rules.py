# rules.py
# =========================================================
# WHO-BASED PRE-TRIAGE RULE ENGINE
#
# References:
# - WHO Emergency Triage Assessment and Treatment (ETAT)
# - WHO Integrated Management of Childhood Illness (IMCI)
# - WHO Digital Clinical Decision Support (CDS)
#
# IMPORTANT:
# - Rules are deterministic
# - No AI decision-making here
# - Suitable for primary care / pre-triage
# =========================================================

from typing import Optional

# -----------------------------
# TRIAGE CATEGORIES
# -----------------------------
TRIAGE_RED = "MERAH"
TRIAGE_YELLOW = "KUNING"
TRIAGE_GREEN = "HIJAU"


# -----------------------------
# RISK GROUP EVALUATION
# -----------------------------
def is_risk_group(
    age: int,
    pregnant: bool,
    comorbidity: bool,
) -> bool:
    """
    Determine WHO-based risk group.
    """
    if pregnant:
        return True

    if comorbidity:
        return True

    if age >= 60:
        return True

    if age < 5:
        return True

    return False


# -----------------------------
# MAIN TRIAGE CLASSIFICATION
# -----------------------------
def classify_triage(
    danger_sign: bool,
    duration_hours: Optional[int],
    risk_group: bool,
) -> str:
    """
    WHO-based pre-triage classification.
    Output:
    - MERAH  : Emergency (immediate referral)
    - KUNING : Priority (needs medical assessment)
    - HIJAU  : Non-urgent
    """

    # 1. EMERGENCY SIGNS (WHO ETAT)
    if danger_sign:
        return TRIAGE_RED

    # 2. PRIORITY SIGNS
    if risk_group:
        return TRIAGE_YELLOW

    if duration_hours is not None and duration_hours > 48:
        return TRIAGE_YELLOW

    # 3. NON-URGENT
    return TRIAGE_GREEN
