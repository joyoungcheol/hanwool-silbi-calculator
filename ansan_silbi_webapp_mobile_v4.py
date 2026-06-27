# hanwool_silbi_webapp.py
# 안산 실손의료비 계산기 - 모바일 반응형 웹앱 V4
# 실행: streamlit run hanwool_silbi_webapp_mobile_v4.py

import streamlit as st
from dataclasses import dataclass
from typing import Dict, Tuple

st.set_page_config(
    page_title="안산 실손의료비 계산기",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get Help": None, "Report a bug": None, "About": "표준 약관 기준 단건 예상 계산기입니다. 실제 보험금 지급액은 가입 상품의 약관, 가입시기, 회사별 지급 조건에 따라 달라질 수 있습니다."}
)

# -----------------------------
# CSS: 모바일 우선 + KB 느낌 색상
# -----------------------------
st.markdown(
    """
<style>
:root {
    --kb-yellow: #ffbc00;
    --kb-dark: #2f2f2f;
    --kb-gray: #f7f3e8;
    --kb-border: #d9d2bf;
    --kb-blue: #0057b8;
    --danger: #c62828;
    --green: #0b7d32;
    --orange: #ef5b2a;
}
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif !important;
    color: #2f2f2f !important;
}
.stApp {
    background: #faf7ee;
}
.block-container {
    max-width: 1180px;
    padding-top: 1.4rem;
    padding-bottom: 5rem;
}
h1 {
    font-size: 2.0rem !important;
    font-weight: 900 !important;
    color: #2f2f2f !important;
    letter-spacing: -0.04em;
}
h2, h3 {
    color: #2f2f2f !important;
    font-weight: 850 !important;
}
.notice-box {
    background: #fff4f2;
    border-left: 8px solid #c62828;
    border-radius: 12px;
    padding: 14px 16px;
    color: #b71c1c;
    font-weight: 800;
    line-height: 1.7;
    margin-bottom: 18px;
}
.section-card {
    background: #ffffff;
    border: 1.5px solid var(--kb-border);
    border-radius: 14px;
    padding: 16px 16px 18px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(60, 45, 15, 0.05);
}
.section-title {
    font-size: 1.25rem;
    font-weight: 900;
    margin-bottom: 10px;
    color: #333;
}
.small-help {
    font-size: 0.9rem;
    color: #666;
    line-height: 1.55;
}
.result-card {
    background: #fff;
    border: 1.5px solid #d7d7d7;
    border-radius: 14px;
    padding: 18px 18px;
    margin-top: 18px;
    font-size: 1.04rem;
    line-height: 1.65;
    white-space: pre-wrap;
}
.result-title {
    color: var(--kb-blue);
    font-weight: 900;
    font-size: 1.25rem;
}
.final-pay {
    color: #0066ff;
    font-weight: 950;
    font-size: 1.45rem;
}
.own-pay {
    color: #d32f2f;
    font-weight: 850;
}
hr {
    border: none;
    border-top: 1px solid #e5ddca;
    margin: 16px 0;
}
/* Streamlit 기본 위젯 색상 보정 */
.stRadio label, .stCheckbox label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    color: #2f2f2f !important;
    font-weight: 800 !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #fff3bf !important;
    color: #111 !important;
    font-weight: 750 !important;
    border: 1.5px solid #555 !important;
}
div[data-testid="stDateInput"] input {
    background: #fff3bf !important;
    color: #111 !important;
    font-weight: 750 !important;
    border: 1.5px solid #555 !important;
}
.stButton > button {
    background: #303030 !important;
    color: var(--kb-yellow) !important;
    border: 0 !important;
    border-radius: 8px !important;
    font-size: 1.15rem !important;
    font-weight: 900 !important;
    min-height: 48px;
}
.stButton > button:hover {
    background: #111 !important;
    color: #ffd34e !important;
}
div[role="radiogroup"] label {
    color: #2f2f2f !important;
}
@media (max-width: 760px) {
    .block-container {
        padding: 0.8rem 0.8rem 5rem;
    }
    h1 {
        font-size: 1.55rem !important;
        line-height: 1.25;
    }
    .notice-box {
        padding: 12px 12px;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 12px;
    }
    .section-card {
        padding: 13px 12px;
        border-radius: 12px;
    }
    .section-title {
        font-size: 1.08rem;
    }
    .result-card {
        font-size: 0.96rem;
        padding: 14px 12px;
    }
    .final-pay {
        font-size: 1.28rem;
    }
    /* 모바일에서 위젯 간격 축소 */
    div[data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }
}

/* V5: 모바일/다크모드 글자색 강제 보정 */
.stApp, .stApp * {
    color: #2f2f2f !important;
    opacity: 1 !important;
}
.stApp {
    background-color: #faf7ee !important;
}
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] *,
div[data-testid="stWidgetLabel"],
div[data-testid="stWidgetLabel"] *,
div[role="radiogroup"],
div[role="radiogroup"] *,
label, label *, p, span {
    color: #2f2f2f !important;
    opacity: 1 !important;
}
.notice-box, .notice-box * {
    color: #b71c1c !important;
    font-weight: 900 !important;
}
.result-title, .result-title * {
    color: #0057b8 !important;
}
.final-pay, .final-pay * {
    color: #0066ff !important;
    font-weight: 950 !important;
}
.own-pay, .own-pay * {
    color: #d32f2f !important;
}
.stButton > button,
.stButton > button *,
button[kind="primary"],
button[kind="primary"] * {
    background: #303030 !important;
    color: #ffbc00 !important;
    font-weight: 950 !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input {
    background-color: #fff3bf !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    font-weight: 850 !important;
}
div[data-testid="stNumberInput"] button,
div[data-testid="stNumberInput"] button * {
    background-color: #303040 !important;
    color: #ffffff !important;
}
div[data-testid="stAlert"],
div[data-testid="stAlert"] * {
    color: #2f2f2f !important;
}
@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 760px !important;
    }
    h1 {
        font-size: 1.6rem !important;
        text-align: left !important;
    }
    div[role="radiogroup"] {
        gap: 0.25rem !important;
    }
    div[role="radiogroup"] label {
        min-height: 34px !important;
    }
}


</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# 유틸
# -----------------------------
def won(value: float | int) -> str:
    try:
        return f"{int(round(value)):,}원"
    except Exception:
        return "0원"


def positive(value: float | int) -> int:
    return max(0, int(round(value or 0)))


def capped_pay(amount: int, deductible: int, limit: int | None = None) -> Tuple[int, int]:
    pay_before_limit = max(0, amount - deductible)
    pay = min(pay_before_limit, limit) if limit else pay_before_limit
    own = max(0, amount - pay)
    return pay, own


def hospital_deductible(hospital_type: str) -> int:
    if hospital_type == "의원":
        return 10_000
    if hospital_type == "병원":
        return 15_000
    return 20_000


def hospital_health_rate_5th(hospital_type: str) -> float:
    if hospital_type == "의원":
        return 0.30
    if hospital_type == "병원":
        return 0.40
    return 0.50


def room_pay(room_fee: int, days: int, base_two_bed_fee: int = 0, first_gen_nonlife: bool = False) -> Tuple[int, int, str]:
    if room_fee <= 0 or days <= 0:
        return 0, 0, ""
    if first_gen_nonlife and base_two_bed_fee > 0:
        pay = min(int(room_fee * 0.5), int(base_two_bed_fee * 0.5))
        desc = f"병실 이용료 : {won(room_fee)}\n2인실 기준 병실료 : {won(base_two_bed_fee)}\nmin(실제차액×50%, 2인실차액×50%) = {won(pay)} 적용"
    else:
        pay = min(int(room_fee * 0.5), 100_000 * days)
        desc = f"병실 이용료 : {won(room_fee)}\n입원일수 {days}일 적용\n50% 보상 (1일 최대 10만 원 한도) 적용"
    own = max(0, room_fee - pay)
    return pay, own, desc


# -----------------------------
# 계산 로직
# -----------------------------
@dataclass
class Inputs:
    generation: str
    join_period: str
    insurer: str
    plan_type: str
    life_type: str
    care_type: str
    hospital_type: str
    date: str
    hospital_name: str
    covered_medical: int
    uncovered_medical: int
    severe_uncovered_medical: int
    special3_medical: int
    covered_drug: int
    uncovered_drug: int
    room_fee: int
    two_bed_fee: int
    days: int


def calc_first(i: Inputs) -> Dict[str, str | int]:
    total_med = i.covered_medical + i.uncovered_medical + i.special3_medical
    drug_total = i.covered_drug + i.uncovered_drug
    lines = [f"[진료 1 · {i.date} · {i.hospital_name}]", f"■ 1세대 실손 (~2009.07) · {i.insurer} · {i.care_type}"]

    if i.insurer == "손해보험사":
        outpatient_limit = 300_000
        inpatient_limit = 100_000_000
        drug_limit = 50_000
        lines += [
            "☞ 통원 한도 : 1일 30만원 (통상 연 30회)",
            "☞ 입원 한도 : 연간 1억원",
            "☞ 약제비 한도 : 건당 50,000원",
        ]
        if i.care_type == "통원":
            lines.append("☞ 손해보험사: 기본 공제 5,000원 후 100% 지급")
            ded = 5_000 if total_med > 0 else 0
            pay, own = capped_pay(total_med, ded, outpatient_limit)
            lines += [
                "",
                f"총 진료 의료비 : {won(total_med)}",
                f"기본 공제 5,000원 적용 → 지급액 {won(pay)}" + (" (공제액이 진료비 초과)" if pay == 0 and total_med > 0 else ""),
                "",
                f"본인부담금 : {won(own)}",
                f"수령 예상액 : {won(pay)}",
            ]
        else:
            lines.append("☞ 손해보험사: 자기부담금 없음 — 100% 지급")
            pay = min(total_med, inpatient_limit)
            own = max(0, total_med - pay)
            lines += [
                "",
                f"총 진료 의료비 : {won(total_med)}",
                f"급여 + 비급여 + 특약 100% 지급 → 지급액 {won(pay)}",
                "",
                f"본인부담금 : {won(own)}",
                f"수령 예상액 : {won(pay)}",
                "",
                "※ 입원 보장한도 연 1억원",
            ]
            rpay, rown, rdesc = room_pay(i.room_fee, i.days, i.two_bed_fee, first_gen_nonlife=True)
            if rdesc:
                lines += ["", "■ 상급병실 이용료 보상", "", rdesc, "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]
    else:
        if i.life_type.startswith("구형"):
            outpatient_limit = 100_000
            inpatient_limit = 30_000_000
            life_desc = "생보 구형"
            type_desc = "구형"
        else:
            outpatient_limit = 200_000
            inpatient_limit = 50_000_000
            life_desc = "생보 신형"
            type_desc = "신형"
        drug_limit = 100_000
        lines += [
            f"☞ 통원 한도 : 1일 {outpatient_limit//10000}만원 (통상 연 30회 / {life_desc})",
            f"☞ 입원 한도 : 연간 {inpatient_limit//10000:,}만원",
            "☞ 약제비 한도 : 건당 100,000원",
            "☞ 생명보험사: 진료비 80% 지급 (20% 본인부담)",
        ]
        pay_before = int(total_med * 0.8)
        limit = outpatient_limit if i.care_type == "통원" else inpatient_limit
        pay = min(pay_before, limit)
        own = max(0, total_med - pay)
        lines += [
            "",
            f"총 진료 의료비 : {won(total_med)}",
            f"80% 지급 적용 → 지급액 {won(pay)}" if i.care_type == "통원" else f"80% 지급 적용 → {won(pay)}",
            "",
            f"본인부담금 : {won(own)}",
            f"수령 예상액 : {won(pay)}",
        ]
        if i.care_type == "입원":
            lines += ["", "※ 입원 보장한도 연 5천만원" if type_desc == "신형" else "※ 입원 보장한도 연 3천만원"]
            rpay, rown, rdesc = room_pay(i.room_fee, i.days)
            if rdesc:
                lines += ["", "■ 상급병실 이용료 보상", "", rdesc.replace("50% 보상", "1세대 생명보험: 50% 보상"), "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]

    if i.care_type == "통원" and drug_total > 0:
        drug_pay = min(max(0, drug_total - 5_000), drug_limit)
        drug_own = max(0, drug_total - drug_pay)
        lines += [
            "",
            "■ 1세대 실손 · 약제비 보상액",
            "",
            f"처방조제 합계 금액 : {won(drug_total)}",
            f"고정 공제 5,000원 → 처방 한도({won(drug_limit)}) 적용 → {won(drug_pay)}",
            "",
            f"본인부담금 : {won(drug_own)}",
            f"수령 예상액 : {won(drug_pay)}",
        ]
    final = _last_receipt(lines)
    return {"text": "\n".join(lines), "final_pay": final}


def _rate_second(i: Inputs) -> Tuple[float, float]:
    # MHS 테스트 기준:
    # 2009.08~2013.03 선택형: 급여/비급여 10%
    # 2013.04~2015.08 이후 선택형: 급여 10%, 비급여 20%
    # 표준형: 급여/비급여 20%
    if i.plan_type == "표준형":
        return 0.20, 0.20
    if i.join_period == "2009.08 ~ 2013.03":
        return 0.10, 0.10
    return 0.10, 0.20


def calc_second(i: Inputs) -> Dict[str, str | int]:
    covered_rate, uncovered_rate = _rate_second(i)
    outpatient_limit = 250_000 if i.insurer == "손해보험사" else 200_000
    drug_limit = 50_000 if i.insurer == "손해보험사" else 100_000
    inpatient_limit = 50_000_000
    total_med = i.covered_medical + i.uncovered_medical
    drug_total = i.covered_drug + i.uncovered_drug
    plan_label = i.plan_type
    lines = [f"[진료 1 · {i.date} · {i.hospital_name}]", f"■ 2세대 실손 (2009.08~2017.03) · {plan_label} · {i.care_type}"]
    lines += [
        f"☞ 통원 한도 : 1일 {won(outpatient_limit)} (연 180회 / {'손해보험' if i.insurer=='손해보험사' else '생명보험'})",
        "☞ 입원 한도 : 연간 5,000만원",
        f"☞ 약제비 한도 : 건당 {won(drug_limit)} (연 180건)",
    ]

    if i.care_type == "통원":
        fixed = hospital_deductible(i.hospital_type)
        if covered_rate == uncovered_rate:
            rate_desc = f"{int(covered_rate*100)}%"
        else:
            rate_desc = f"{int(covered_rate*100)}~{int(uncovered_rate*100)}%"
        lines.append(f"☞ 비용 공제 {won(fixed)} VS 비율 공제 {rate_desc} 중 더 큰 금액 공제")
        lines.append("")
        med_parts = []
        if i.covered_medical > 0:
            med_parts.append(f"급여 진료 의료비 : {won(i.covered_medical)}")
        if i.uncovered_medical > 0 or (total_med == 0 and drug_total > 0):
            med_parts.append(f"비급여 진료 의료비 : {won(i.uncovered_medical)}")
        if med_parts:
            lines.append(" | ".join(med_parts))
            lines.append("")
        rate_ded = int(i.covered_medical * covered_rate) + int(i.uncovered_medical * uncovered_rate)
        if total_med > 0:
            ded = max(fixed, rate_ded)
        else:
            ded = 0
        pay, own = capped_pay(total_med, ded, outpatient_limit)
        formula = []
        if i.covered_medical > 0:
            formula.append(f"급여 {won(int(i.covered_medical*covered_rate))}({int(covered_rate*100)}%)")
        if i.uncovered_medical > 0:
            formula.append(f"비급여 {won(int(i.uncovered_medical*uncovered_rate))}({int(uncovered_rate*100)}%)")
        formula_text = " + ".join(formula)
        lines += [
            f"진료비 합산 : 비용 공제 {won(fixed)} VS 비율 공제 {formula_text} = {won(rate_ded)}",
            f"→ 지급액 {won(pay)}" + (" (공제액이 진료비 초과)" if pay == 0 and total_med > 0 else ""),
            "",
            f"본인부담금 : {won(own)}",
            f"수령 예상액 : {won(pay)}",
        ]
        if drug_total > 0:
            drug_rate_ded = int(i.covered_drug * covered_rate) + int(i.uncovered_drug * uncovered_rate)
            drug_ded = max(8_000, drug_rate_ded)
            drug_pay, drug_own = capped_pay(drug_total, drug_ded, drug_limit)
            drug_parts = []
            if i.covered_drug > 0:
                drug_parts.append(f"급여 약제비 : {won(i.covered_drug)}")
            if i.uncovered_drug > 0:
                drug_parts.append(f"비급여 약제비 : {won(i.uncovered_drug)}")
            lines += [
                "",
                "■ 2세대 실손 · 약제비 보상액",
                "",
                " | ".join(drug_parts),
                "",
                f"적용 공제 : 비용 공제 8,000원 VS 비율 공제 {won(drug_rate_ded)}(급여{int(covered_rate*100)}%+비급여{int(uncovered_rate*100)}%)",
                f"→ 지급액 {won(drug_pay)}",
                "",
                f"본인부담금 : {won(drug_own)}",
                f"수령 예상액 : {won(drug_pay)}",
            ]
    else:
        lines.append(f"☞ 급여 {int(covered_rate*100)}% / 비급여 {int(uncovered_rate*100)}% 비율 공제 (최소공제 없음)")
        ded_cov = int(i.covered_medical * covered_rate)
        ded_unc = int(i.uncovered_medical * uncovered_rate)
        ded = ded_cov + ded_unc
        pay, own = capped_pay(total_med, ded, inpatient_limit)
        lines += [
            "",
            f"총 진료 의료비 : {won(total_med)}",
            f"급여 {int(covered_rate*100)}% 공제 : {won(ded_cov)}",
            f"비급여 {int(uncovered_rate*100)}% 공제 : {won(ded_unc)}",
            f"→ 지급액 {won(pay)}",
            "",
            f"본인부담금 : {won(own)}",
            f"수령 예상액 : {won(pay)}",
            "",
            "※ 입원 보장한도 연 5천만원",
        ]
        rpay, rown, rdesc = room_pay(i.room_fee, i.days)
        if rdesc:
            lines += ["", "■ 상급병실 이용료 보상", "", rdesc, "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]
    return {"text": "\n".join(lines), "final_pay": _last_receipt(lines)}


def calc_third(i: Inputs) -> Dict[str, str | int]:
    total_base = i.covered_medical + i.uncovered_medical
    total = total_base + i.special3_medical
    drug_total = i.covered_drug + i.uncovered_drug
    outpatient_limit = 250_000 if i.insurer == "손해보험사" else 200_000
    drug_limit = 50_000 if i.insurer == "손해보험사" else 100_000
    lines = [f"[진료 1 · {i.date} · {i.hospital_name}]", f"■ 3세대 실손 (2017.04~2021.06) · {i.care_type}"]
    lines += [
        f"☞ 통원 한도 : 1일 {won(outpatient_limit)} (연 180회 / {'손해보험' if i.insurer=='손해보험사' else '생명보험'})",
        "☞ 입원 한도 : 연간 5,000만원",
        f"☞ 약제비 한도 : 건당 {won(drug_limit)} (연 180건)",
    ]
    if i.care_type == "통원":
        fixed = hospital_deductible(i.hospital_type)
        lines.append("☞ 비용 공제 VS 비율 공제 중 더 큰 금액 공제")
        lines.append("")
        if i.covered_medical or i.uncovered_medical:
            med = []
            if i.covered_medical: med.append(f"급여 진료 의료비 : {won(i.covered_medical)}")
            if i.uncovered_medical: med.append(f"비급여 진료 의료비 : {won(i.uncovered_medical)}")
            lines.append(" | ".join(med))
        if i.special3_medical:
            lines.append(f"3대 특약 의료비 : {won(i.special3_medical)}")
        if total_base > 0:
            rate_ded = int(i.covered_medical * 0.10) + int(i.uncovered_medical * 0.20)
            ded = max(fixed, rate_ded)
            base_pay, base_own = capped_pay(total_base, ded, outpatient_limit)
            formula = []
            if i.covered_medical: formula.append(f"급여 {won(int(i.covered_medical*0.10))}(10%)")
            if i.uncovered_medical: formula.append(f"비급여 {won(int(i.uncovered_medical*0.20))}(20%)")
            lines += ["", f"진료비 합산 : 비용 공제 {won(fixed)} VS 비율 공제 {' + '.join(formula)} = {won(rate_ded)}", f"→ 지급액 {won(base_pay)}"]
        else:
            base_pay, base_own = 0, 0
        if i.special3_medical > 0:
            sp_rate = int(i.special3_medical * 0.30)
            sp_ded = max(20_000, sp_rate)
            sp_pay, sp_own = capped_pay(i.special3_medical, sp_ded)
            lines += [f"3대 특약 공제 : 비용 공제 20,000원 VS 비율 공제 {won(sp_rate)}(30%)", f"→ 지급액 {won(sp_pay)}" + (" (공제액이 진료비 초과)" if sp_pay == 0 else "")]
        else:
            sp_pay, sp_own = 0, 0
        pay = base_pay + sp_pay
        own = total - pay
        lines += ["", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}"]
        if drug_total > 0:
            drug_rate = int(i.covered_drug*0.10) + int(i.uncovered_drug*0.20)
            drug_ded = max(8_000, drug_rate)
            dpay, down = capped_pay(drug_total, drug_ded, drug_limit)
            parts = []
            if i.covered_drug: parts.append(f"급여 약제비 : {won(i.covered_drug)}")
            if i.uncovered_drug: parts.append(f"비급여 약제비 : {won(i.uncovered_drug)}")
            lines += ["", "■ 3세대 실손 · 약제비 보상액", "", " | ".join(parts), "", f"적용 공제 : 비용 공제 8,000원 VS 비율 공제 {won(drug_rate)}(급여10%+비급여20%)", f"→ 지급액 {won(dpay)}", "", f"본인부담금 : {won(down)}", f"수령 예상액 : {won(dpay)}"]
    else:
        lines.append("☞ 급여 10% / 비급여 20% 비율 공제 (최소공제 없음)")
        cov_d = int(i.covered_medical*0.10)
        unc_d = int(i.uncovered_medical*0.20)
        sp_d = int(i.special3_medical*0.30)
        ded = cov_d + unc_d + sp_d
        pay, own = capped_pay(total, ded, 50_000_000)
        lines += ["", f"총 진료 의료비 : {won(total)}", f"급여 10% 공제 : {won(cov_d)}", f"비급여 20% 공제 : {won(unc_d)}", f"3대 특약 공제 : 비용 공제 20,000원 VS 비율 공제 {won(sp_d)}(30%)", f"→ 지급액 {won(pay)}", "", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}", "", "※ 입원 보장한도 연 5천만원"]
        rpay, rown, rdesc = room_pay(i.room_fee, i.days)
        if rdesc:
            lines += ["", "■ 상급병실 이용료 보상", "", rdesc, "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]
    return {"text": "\n".join(lines), "final_pay": _last_receipt(lines)}


def calc_fourth(i: Inputs) -> Dict[str, str | int]:
    total = i.covered_medical + i.uncovered_medical + i.special3_medical + i.covered_drug + i.uncovered_drug
    lines = [f"[진료 1 · {i.date} · {i.hospital_name}]", f"■ 4세대 실손 (2021.07~2026.03) · {i.care_type}"]
    lines += [
        "☞ 통원 한도 : 1일 20만원 (연 100회)",
        "☞ 입원 한도 : 연간 5,000만원",
        "☞ 약제비 한도 : 1일 통원 한도(20만원) 합산 내 보상",
    ]
    if i.care_type == "통원":
        lines.append("☞ 급여(진료+약제) 합산 / 비급여(진료+약제) 합산 후 각각 공제")
        lines.append("")
        covered_sum = i.covered_medical + i.covered_drug
        uncovered_sum = i.uncovered_medical + i.uncovered_drug
        pay = 0
        if i.covered_medical: lines.append(f"급여 진료 의료비 : {won(i.covered_medical)}")
        if i.uncovered_medical: lines.append(f"비급여 진료 의료비 : {won(i.uncovered_medical)}")
        if i.special3_medical: lines.append(f"3대 특약 의료비 : {won(i.special3_medical)}")
        if i.covered_drug: lines.append(f"급여 약제비 : {won(i.covered_drug)}")
        if i.uncovered_drug: lines.append(f"비급여 약제비 : {won(i.uncovered_drug)}")
        if covered_sum > 0:
            fixed = hospital_deductible(i.hospital_type)
            rate = int(covered_sum * 0.20)
            ded = max(fixed, rate)
            p, _ = capped_pay(covered_sum, ded)
            pay += p
            lines += ["", f"급여 합산({won(covered_sum)}) : 비용 공제 {won(fixed)} VS 비율 공제 {won(rate)}(20%)", f"→ 지급액 {won(p)}"]
        if uncovered_sum > 0:
            rate = int(uncovered_sum * 0.30)
            ded = max(30_000, rate)
            p, _ = capped_pay(uncovered_sum, ded)
            pay += p
            lines += [f"비급여 합산({won(uncovered_sum)}) : 비용 공제 30,000원 VS 비율 공제 {won(rate)}(30%)", f"→ 지급액 {won(p)}" + (" (공제액이 비급여 합산액 초과)" if p == 0 else "")]
        if i.special3_medical > 0:
            rate = int(i.special3_medical*0.30)
            ded = max(30_000, rate)
            p, _ = capped_pay(i.special3_medical, ded)
            pay += p
            lines += [f"3대 특약 공제 : 비용 공제 30,000원 VS 비율 공제 {won(rate)}(30%)", f"→ 지급액 {won(p)}" + (" (공제액이 진료비 초과)" if p == 0 else "")]
        pay = min(pay, 200_000)
        own = max(0, total - pay)
        lines += ["", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}"]
    else:
        lines.append("☞ 급여 20% / 비급여 30% 비율 공제 (최소공제 없음)")
        cov_d = int(i.covered_medical*0.20)
        unc_d = int(i.uncovered_medical*0.30)
        sp_d = int(i.special3_medical*0.30)
        ded = cov_d + unc_d + sp_d
        med_total = i.covered_medical + i.uncovered_medical + i.special3_medical
        pay, own = capped_pay(med_total, ded, 50_000_000)
        lines += ["", f"총 진료 의료비 : {won(med_total)}", f"급여 20% 공제 : {won(cov_d)}", f"비급여 30% 공제 : {won(unc_d)}", f"3대 특약 30% 공제 : {won(sp_d)}", f"→ 지급액 {won(pay)}", "", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}", "", "※ 입원 보장한도 연 5천만원"]
        rpay, rown, rdesc = room_pay(i.room_fee, i.days)
        if rdesc:
            lines += ["", "■ 상급병실 이용료 보상", "", rdesc, "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]
    return {"text": "\n".join(lines), "final_pay": _last_receipt(lines)}


def calc_fifth(i: Inputs) -> Dict[str, str | int]:
    lines = [f"[진료 1 · {i.date} · {i.hospital_name}]", f"■ 5세대 실손 (2026.05~) · {i.care_type}"]
    lines += [
        "☞ 통원 한도 : 1일 20만원 (연 100회)",
        "☞ 입원 한도 : 연간 5,000만원",
        "☞ 약제비 한도 : 1일 통원 한도(20만원) 합산 내 보상",
    ]
    if i.care_type == "통원":
        health_rate = hospital_health_rate_5th(i.hospital_type)
        fixed = hospital_deductible(i.hospital_type)
        lines.append(f"☞ 급여: 건보연동({i.hospital_type}{int(health_rate*100)}%) / 비중증 비급여: max(50%, 5만원) / 중증 비급여: max(30%, 3만원)")
        lines.append("")
        covered_sum = i.covered_medical + i.covered_drug
        non_severe_sum = i.uncovered_medical + i.uncovered_drug
        severe_sum = i.severe_uncovered_medical
        pay = 0
        total = covered_sum + non_severe_sum + severe_sum
        if i.covered_medical: lines.append(f"급여 진료 의료비 : {won(i.covered_medical)}")
        if i.covered_drug: lines.append(f"급여 약제비 : {won(i.covered_drug)}")
        if non_severe_sum: lines.append(f"비중증 비급여 진료비/약제비 : {won(non_severe_sum)}")
        if severe_sum: lines.append(f"중증 비급여 진료비용 : {won(severe_sum)}")
        if covered_sum > 0:
            health_d = int(covered_sum * health_rate)
            rate_d = int(covered_sum * 0.20)
            ded = max(health_d, rate_d, fixed)
            p, _ = capped_pay(covered_sum, ded)
            pay += p
            reason = "건보연동" if ded == health_d else ("비율공제" if ded == rate_d else "최소공제")
            lines += ["", f"급여 합산({won(covered_sum)}) : 건보연동 {won(health_d)}({int(health_rate*100)}%+약제30%) VS 비율 공제 {won(rate_d)}(20%) VS 비용 공제 {won(fixed)}", f"→ 적용 공제 {won(ded)}({reason})", f"→ 지급액 {won(p)}"]
        if non_severe_sum > 0:
            rate_d = int(non_severe_sum * 0.50)
            ded = max(50_000, rate_d)
            p, _ = capped_pay(non_severe_sum, ded)
            pay += p
            lines += [f"비중증 비급여 합산({won(non_severe_sum)}) : 비용 공제 50,000원 VS 비율 공제 {won(rate_d)}(50%)", f"→ 지급액 {won(p)}" + (" (공제액이 비중증 합산액 초과)" if p == 0 else "")]
        if severe_sum > 0:
            rate_d = int(severe_sum * 0.30)
            ded = max(30_000, rate_d)
            p, _ = capped_pay(severe_sum, ded)
            pay += p
            lines += [f"중증 비급여 : 비용 공제 30,000원 VS 비율 공제 {won(rate_d)}(30%)", f"→ 지급액 {won(p)}" + (" (공제액이 진료비 초과)" if p == 0 else "")]
        pay = min(pay, 200_000)
        own = max(0, total - pay)
        lines += ["", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}"]
    else:
        lines.append("☞ 급여 20% / 비중증 비급여 50% / 중증 비급여 30% 비율 공제 (최소공제 없음)")
        total = i.covered_medical + i.uncovered_medical + i.severe_uncovered_medical
        cov_d = int(i.covered_medical*0.20)
        non_d = int(i.uncovered_medical*0.50)
        sev_d = int(i.severe_uncovered_medical*0.30)
        ded = cov_d + non_d + sev_d
        pay, own = capped_pay(total, ded, 50_000_000)
        lines += ["", f"총 진료 의료비 : {won(total)}", f"급여 20% 공제 : {won(cov_d)}", f"비중증 비급여 50% 공제 : {won(non_d)}", f"중증 비급여 30% 공제 : {won(sev_d)}", f"→ 지급액 {won(pay)}", "", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}", "", "※ 입원 보장한도 합산 5천만원"]
        rpay, rown, rdesc = room_pay(i.room_fee, i.days)
        if rdesc:
            lines += ["", "■ 상급병실 이용료 보상", "", rdesc, "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]
    return {"text": "\n".join(lines), "final_pay": _last_receipt(lines)}


def calc_senior(i: Inputs) -> Dict[str, str | int]:
    total = i.covered_medical + i.uncovered_medical
    drug_total = i.covered_drug + i.uncovered_drug
    lines = [f"[진료 1 · {i.date} · {i.hospital_name}]"]
    if i.care_type == "통원":
        lines += [
            "■ 노후 실비 (2014.08~) · 통원 진료비",
            "☞ 통원 한도 : 회당 100만원 (횟수 제한 없음 / 우선공제 3만원)",
            "☞ 입원 한도 : 연간 1억원 (우선공제 30만원)",
            "☞ 약제비 한도 : 연간 100만원 (20% 공제)",
            "☞ max(3만원, 급여 20% + 비급여 30%) 공제",
        ]
        cov_d = int(i.covered_medical*0.20)
        unc_d = int(i.uncovered_medical*0.30)
        ded = max(30_000 if total > 0 else 0, cov_d + unc_d)
        pay, own = capped_pay(total, ded, 1_000_000)
        lines += ["", f"총 진료 의료비 : {won(total)}", f"급여 20% 공제 : {won(cov_d)}", f"비급여 30% 공제 : {won(unc_d)}", f"비율공제 합산 {won(cov_d+unc_d)} / 최소공제 3만원", f"공제액 max(3만원, 비율공제) = {won(ded)}", f"통원 한도(100만원) 적용 → 지급액 {won(pay)}", "", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}"]
        if drug_total > 0:
            d = int(drug_total*0.20)
            dpay, down = capped_pay(drug_total, d, 1_000_000)
            lines += ["", "■ 노후 실비 (2014.08~) · 약제비 보상액", "", f"처방조제 합계 금액 : {won(drug_total)}", f"20% 공제 : {won(d)}", f"처방 한도(연 100만원) 적용 → {won(dpay)}", "", f"본인부담금 : {won(down)}", f"수령 예상액 : {won(dpay)}"]
    else:
        lines += [
            "■ 노후 실비 (2014.08~) · 입원 진료비",
            "☞ 통원 한도 : 회당 100만원 (횟수 제한 없음 / 우선공제 3만원)",
            "☞ 입원 한도 : 연간 1억원 (우선공제 30만원)",
            "☞ 약제비 한도 : 연간 100만원 (20% 공제)",
            "☞ max(30만원, 급여 20% + 비급여 30%) 공제",
        ]
        cov_d = int(i.covered_medical*0.20)
        unc_d = int(i.uncovered_medical*0.30)
        ded = max(300_000 if total > 0 else 0, cov_d + unc_d)
        pay, own = capped_pay(total, ded, 100_000_000)
        lines += ["", f"총 진료 의료비 : {won(total)}", f"급여 20% 공제 : {won(cov_d)}", f"비급여 30% 공제 : {won(unc_d)}", f"비율공제 합산 {won(cov_d+unc_d)} / 최소공제 30만원", f"공제액 max(30만원, 비율공제) = {won(ded)}", f"→ 지급액 {won(pay)}", "", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}", "", "※ 입원 최소공제 30만원 / 보장한도 연 1억원"]
        rpay, rown, rdesc = room_pay(i.room_fee, i.days)
        if rdesc:
            lines += ["", "■ 상급병실 이용료 보상", "", rdesc, "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]
    return {"text": "\n".join(lines), "final_pay": _last_receipt(lines)}


def calc_impaired(i: Inputs) -> Dict[str, str | int]:
    total = i.covered_medical + i.uncovered_medical
    lines = [f"[진료 1 · {i.date} · {i.hospital_name}]"]
    if i.care_type == "통원":
        lines += [
            "■ 유병자 실비 (2018.04~) · 통원 진료비",
            "☞ 통원 한도 : 회당 20만원 (연 180회) | 처방조제비 미보상",
            "☞ 입원 한도 : 연간 5,000만원 / 자기부담 연 200만원 한도",
            "☞ 입원공제 : max(10만원, 합산×30%) | 통원공제 : max(2만원, 합산×30%)",
        ]
        rate = int(total*0.30)
        ded = max(20_000 if total > 0 else 0, rate)
        pay, own = capped_pay(total, ded, 200_000)
        lines += [f"☞ max(2만원, 합산×30%) = {won(ded)} 공제 / ※처방조제비 미보상", "", f"총 진료 의료비 (급여+비급여) : {won(total)}", f"합산×30% = {won(rate)} / 최소공제 2만원", f"공제액 max(2만원, 30%) = {won(ded)}", f"통원 한도(20만원) 적용 → 지급액 {won(pay)}", "", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}"]
    else:
        lines += [
            "■ 유병자 실비 (2018.04~) · 입원 진료비",
            "☞ 통원 한도 : 회당 20만원 (연 180회) | 처방조제비 미보상",
            "☞ 입원 한도 : 연간 5,000만원 / 자기부담 연 200만원 한도",
            "☞ 입원공제 : max(10만원, 합산×30%) | 통원공제 : max(2만원, 합산×30%)",
        ]
        rate = int(total*0.30)
        ded = max(100_000 if total > 0 else 0, rate)
        pay, own = capped_pay(total, ded, 50_000_000)
        lines += [f"☞ max(10만원, 합산×30%) = {won(ded)} 공제", "", f"총 진료 의료비 (급여+비급여) : {won(total)}", f"합산×30% = {won(rate)} / 최소공제 10만원", f"공제액 max(10만원, 30%) = {won(ded)}", f"→ 지급액 {won(pay)}", "", f"본인부담금 : {won(own)}", f"수령 예상액 : {won(pay)}", "", "※ 보장한도 연 5천만원 (동일 상병 합산) / 자기부담 연 200만원 한도"]
        rpay, rown, rdesc = room_pay(i.room_fee, i.days)
        if rdesc:
            lines += ["", "■ 상급병실 이용료 보상", "", rdesc, "", f"본인부담금 : {won(rown)}", f"수령 예상액 : {won(rpay)}"]
    return {"text": "\n".join(lines), "final_pay": _last_receipt(lines)}


def _last_receipt(lines) -> int:
    # 마지막 "수령 예상액"을 추출하되, UI 강조용으로는 총합이 아닌 각 섹션 마지막값이 아닌 전체 수령합이 더 자연스러움.
    # 현재는 결과문 마지막 섹션 금액을 반환하므로, 본문에서 직접 확인 가능.
    # 아래는 본문 내 모든 "수령 예상액" 합계 추출.
    import re
    total = 0
    for line in lines:
        m = re.search(r"수령 예상액\s*:\s*([\d,]+)원", line)
        if m:
            total += int(m.group(1).replace(",", ""))
    return total


# -----------------------------
# UI
# -----------------------------
st.title("안산 실손의료비 계산기")
st.markdown(
    """
<div class="notice-box">
① 고객님의 진료비 영수증의 금액을 입력하여 단건 기준(누적 아님) 예상 지급액을 확인합니다.<br>
② 표준 약관 기준으로 실제 보험금 지급액은 가입 상품의 약관 및 가입시기, 일부 회사별 지급 조건에 따라 달라질 수 있습니다.<br>
&nbsp;&nbsp;&nbsp;&nbsp;(전체적인 참고용으로만 안내 / 활용 부탁드립니다)
</div>
""",
    unsafe_allow_html=True,
)

# 모바일에서는 자동으로 세로, 태블릿/PC에서는 2열에 가깝게 표시됨
left, right = st.columns([0.95, 1.15], gap="large")

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">1. 실비 가입 정보</div>', unsafe_allow_html=True)
    generation = st.radio(
        "가입 상품",
        ["1세대", "2세대", "3세대", "4세대", "5세대", "노후실비", "유병자실비"],
        horizontal=True,
        index=1,
    )

    join_period = ""
    plan_type = "선택형"
    life_type = "구형 (통원 10만 / 입원 3천)"
    if generation == "2세대":
        join_period = st.radio(
            "가입 시기",
            ["2009.08 ~ 2013.03", "2013.04 ~ 2015.08", "2015.09 ~ 2015.12", "2016.01 ~ 2017.03"],
            horizontal=True,
        )
        plan_type = st.radio("공제 유형", ["선택형", "표준형"], horizontal=True)
    insurer = st.radio("가입 보험사", ["손해보험사", "생명보험사"], horizontal=True)
    if generation == "1세대" and insurer == "생명보험사":
        life_type = st.radio("생보 유형", ["구형 (통원 10만 / 입원 3천)", "신형 (통원 20만 / 입원 5천)"], horizontal=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">2. 진료 내용</div>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        date_val = st.text_input("진료일", value="2025-01-15")
    with r1c2:
        hospital_name = st.text_input("병원명", value="테스트병원")

    care_type = st.radio("진료 유형", ["통원", "입원"], horizontal=True)
    hospital_type = "의원"
    if care_type == "통원" and generation not in ["1세대", "노후실비", "유병자실비"]:
        hospital_type = st.radio("진료 병원", ["의원", "병원", "종합/상급종합"], horizontal=True)

    # 세대별 입력 필드
    if generation == "5세대":
        covered_label = "급여 진료비용 (원)"
        uncovered_label = "비중증 비급여 진료비용 (원)"
        severe_label = "중증 비급여 진료비용 (원)"
    else:
        covered_label = "급여 진료비용 (원)"
        uncovered_label = "비급여 진료비용 (원)"
        severe_label = "중증 비급여 진료비용 (원)"

    covered_medical = st.number_input(covered_label, min_value=0, value=0, step=1000, format="%d")
    uncovered_medical = st.number_input(uncovered_label, min_value=0, value=0, step=1000, format="%d")

    special3_medical = 0
    severe_uncovered_medical = 0
    if generation == "3세대":
        special3_medical = st.number_input("3대 비급여(도수·주사·MRI) 진료비용 (원)", min_value=0, value=0, step=1000, format="%d")
    if generation == "4세대":
        special3_medical = st.number_input("3대 비급여(도수·주사·MRI) 진료비용 (원)", min_value=0, value=0, step=1000, format="%d")
    if generation == "5세대":
        severe_uncovered_medical = st.number_input(severe_label, min_value=0, value=0, step=1000, format="%d")

    covered_drug = 0
    uncovered_drug = 0
    if care_type == "통원" and generation != "유병자실비":
        st.markdown("<hr>", unsafe_allow_html=True)
        covered_drug = st.number_input("급여 약제비 (처방조제) (원)", min_value=0, value=0, step=1000, format="%d")
        # 모바일에서도 반드시 보이도록 항상 표시
        if generation != "노후실비":
            uncovered_drug = st.number_input("비급여 약제비 (처방조제) (원)", min_value=0, value=0, step=1000, format="%d")

    room_fee = 0
    two_bed_fee = 0
    days = 0
    if care_type == "입원":
        st.markdown("<hr>", unsafe_allow_html=True)
        room_fee = st.number_input("상급병실 이용료 (원)", min_value=0, value=0, step=1000, format="%d")
        if generation == "1세대" and insurer == "손해보험사":
            two_bed_fee = st.number_input("2인실 기준 병실료 (1인실 등 이용 시) (원)", min_value=0, value=0, step=1000, format="%d")
        days = st.number_input("입원일수 (일)", min_value=0, value=0, step=1, format="%d")

    st.markdown('</div>', unsafe_allow_html=True)

calculate = st.button("계산하기", use_container_width=True)

if calculate:
    inputs = Inputs(
        generation=generation,
        join_period=join_period,
        insurer=insurer,
        plan_type=plan_type,
        life_type=life_type,
        care_type=care_type,
        hospital_type=hospital_type,
        date=date_val,
        hospital_name=hospital_name,
        covered_medical=positive(covered_medical),
        uncovered_medical=positive(uncovered_medical),
        severe_uncovered_medical=positive(severe_uncovered_medical),
        special3_medical=positive(special3_medical),
        covered_drug=positive(covered_drug),
        uncovered_drug=positive(uncovered_drug),
        room_fee=positive(room_fee),
        two_bed_fee=positive(two_bed_fee),
        days=positive(days),
    )

    if generation == "1세대":
        result = calc_first(inputs)
    elif generation == "2세대":
        result = calc_second(inputs)
    elif generation == "3세대":
        result = calc_third(inputs)
    elif generation == "4세대":
        result = calc_fourth(inputs)
    elif generation == "5세대":
        result = calc_fifth(inputs)
    elif generation == "노후실비":
        result = calc_senior(inputs)
    else:
        result = calc_impaired(inputs)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-title">계산 결과</div>', unsafe_allow_html=True)
    st.text(result["text"])
    st.markdown(f'<div class="final-pay">총 수령 예상액: {won(result["final_pay"])}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "결과 텍스트 다운로드",
        data=result["text"],
        file_name="안산_실손의료비_계산결과.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.info("가입 정보와 진료비를 입력한 뒤 계산하기를 눌러주세요.")



