import streamlit as st


APP_NAME = "한울지점 실손의료비 계산기"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root {
  --kb-yellow: #ffbc00;
  --kb-dark: #3a3a3a;
  --kb-blue: #005bac;
  --soft-bg: #f7f4ea;
  --warn-red: #c62828;
}
.stApp {
  background: var(--soft-bg);
}
/* 글씨 안 보임 방지: Streamlit 다크 테마에서도 본문을 강제로 진한 색으로 표시 */
.stApp, .stApp p, .stApp div, .stApp span, .stApp label {
  color: #2f2f2f !important;
}
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] * {
  color: #f7f7f7 !important;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
  color: #111111 !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stRadio"] label,
div[data-testid="stSelectbox"] label {
  color: #4a4a4a !important;
  font-weight: 800 !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
  color: #111111 !important;
  font-weight: 700 !important;
}
.notice, .notice * {
  color: var(--warn-red) !important;
}
.result-title, .result-title * {
  color: var(--kb-blue) !important;
}
.receive, .receive * {
  color: var(--kb-blue) !important;
}
.patient, .patient * {
  color: var(--warn-red) !important;
}

.main-title {
  color: var(--kb-dark);
  font-size: 30px;
  font-weight: 900;
  margin-bottom: 4px;
}
.notice {
  color: var(--warn-red);
  font-weight: 800;
  line-height: 1.65;
  padding: 12px 14px;
  border-left: 6px solid var(--warn-red);
  background: #fff7f5;
  border-radius: 8px;
}
.section-card {
  background: white;
  border: 1px solid #ddd6c5;
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 16px;
}
.result-card {
  background: white;
  border: 2px solid var(--kb-blue);
  border-radius: 16px;
  padding: 20px;
}
.result-title {
  color: var(--kb-blue);
  font-weight: 900;
  font-size: 24px;
}
.receive {
  color: var(--kb-blue);
  font-weight: 900;
  font-size: 34px;
}
.patient {
  color: var(--warn-red);
  font-weight: 800;
  font-size: 24px;
}
.small-muted {
  color: #666;
  font-size: 13px;
}
div[data-testid="stNumberInput"] input {
  background-color: #fff4bf;
}
div[data-testid="stTextInput"] input {
  background-color: #fff4bf;
}
.stButton > button {
  background: var(--kb-dark);
  color: var(--kb-yellow);
  font-weight: 900;
  border-radius: 10px;
  border: 0;
}
</style>
""",
    unsafe_allow_html=True,
)


# -------------------------
# 공통 함수
# -------------------------

def won(v: int | float) -> str:
    return f"{int(round(v)):,}원"


def safe_pay(total: int, deductible: int, limit: int | None = None):
    before = max(0, total - deductible)
    pay = min(before, limit) if limit is not None else before
    patient = total - pay
    return before, pay, patient


def premium_room(premium: int, days: int):
    before = int(premium * 0.5)
    limit = days * 100000
    pay = min(before, limit) if premium > 0 else 0
    patient = premium - pay
    return pay, patient


def markdown_result(title, lines, receive, patient, extra_receive=None, extra_patient=None):
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="result-title">{title}</div>', unsafe_allow_html=True)
    st.markdown("---")
    for line in lines:
        st.write(line)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="patient">본인부담금: {won(patient)}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="receive">수령 예상액: {won(receive)}</div>', unsafe_allow_html=True)

    if extra_receive is not None:
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="patient">상급병실 본인부담금: {won(extra_patient)}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="receive">상급병실 수령액: {won(extra_receive)}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


HOSPITAL_FIXED = {
    "의원": 10000,
    "병원": 15000,
    "종합/상급종합": 20000,
}

COMPANY_LIMITS_2_3 = {
    "손해보험사": {"outpatient": 250000, "drug": 50000, "inpatient": 50000000},
    "생명보험사": {"outpatient": 200000, "drug": 100000, "inpatient": 50000000},
}


# -------------------------
# 화면
# -------------------------

st.markdown(f'<div class="main-title">{APP_NAME}</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="notice">
① 고객님의 진료비 영수증의 금액을 입력하여 단건 기준(누적 아님) 예상 지급액을 확인합니다.<br>
② 표준 약관 기준으로 실제 보험금 지급액은 가입 상품의 약관 및 가입시기, 일부 회사별 지급 조건에 따라 달라질수 있습니다
(전체적인 참고용으로만 안내 / 활용 부탁드립니다)
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("1. 실비 가입 정보")

    generation = st.radio(
        "가입 상품",
        ["1세대", "2세대", "3세대", "4세대", "5세대", "노후실비", "유병자실비"],
        index=1,
    )

    company = None
    life_type = None
    join_period = None
    deductible_type = None

    if generation in ["1세대", "2세대", "3세대"]:
        company = st.radio("가입 보험사", ["손해보험사", "생명보험사"], horizontal=True)

    if generation == "1세대" and company == "생명보험사":
        life_type = st.radio("생명보험사 유형", ["구형", "신형"], horizontal=True)

    if generation == "2세대":
        join_period = st.selectbox(
            "가입 시기",
            ["2009.08~2013.03", "2013.04~2015.08", "2015.09~2015.12", "2016.01~2017.03"],
        )
        deductible_type = st.radio("공제 유형", ["선택형", "표준형"], horizontal=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("2. 진료 내용")

c1, c2 = st.columns(2)
with c1:
    visit_date = st.text_input("진료일", value="2025-01-15")
with c2:
    hospital_name = st.text_input("병원명", value="테스트병원")

treatment = st.radio("진료 유형", ["통원", "입원"], horizontal=True)

show_hospital = generation in ["2세대", "3세대", "4세대", "5세대"] and treatment == "통원"
hospital_type = None
if show_hospital:
    hospital_type = st.radio("진료 병원", ["의원", "병원", "종합/상급종합"], horizontal=True)

# 입력
if generation == "5세대":
    gubyeo = st.number_input("급여 진료비용", min_value=0, step=1000, value=0)
    nonsevere = st.number_input("비중증 비급여 진료비용", min_value=0, step=1000, value=0)
    severe = st.number_input("중증 비급여 진료비용", min_value=0, step=1000, value=0)
    bigubyeo = 0
    special3 = 0
else:
    gubyeo = st.number_input("급여 진료비용", min_value=0, step=1000, value=0)
    bigubyeo = st.number_input("비급여 진료비용", min_value=0, step=1000, value=0)
    special3 = 0
    nonsevere = 0
    severe = 0

if generation in ["3세대", "4세대"]:
    special3 = st.number_input("3대 비급여(도수·주사·MRI) 진료비용", min_value=0, step=1000, value=0)

drug_g = 0
drug_b = 0
if treatment == "통원" and generation != "유병자실비":
    st.markdown("---")
    drug_g = st.number_input("급여 약제비", min_value=0, step=1000, value=0)
    drug_b = st.number_input("비급여 약제비", min_value=0, step=1000, value=0)

premium = 0
days = 0
two_bed = 0
if treatment == "입원":
    st.markdown("---")
    premium = st.number_input("상급병실 이용료", min_value=0, step=1000, value=0)
    if generation == "1세대" and company == "손해보험사":
        two_bed = st.number_input("2인실 기준 병실료", min_value=0, step=1000, value=0)
    days = st.number_input("입원일수", min_value=0, step=1, value=0)

st.markdown("</div>", unsafe_allow_html=True)

calculate = st.button("계산하기", use_container_width=True)


# -------------------------
# 계산 로직
# -------------------------

def calculate_gen1():
    total = gubyeo + bigubyeo

    if company == "손해보험사":
        outpatient_limit = 300000
        drug_limit = 50000
        inpatient_limit = 100000000
    else:
        outpatient_limit = 100000 if life_type == "구형" else 200000
        drug_limit = 100000
        inpatient_limit = 30000000 if life_type == "구형" else 50000000

    if treatment == "통원":
        if company == "손해보험사":
            before, pay, patient = safe_pay(total, 5000, outpatient_limit)
            lines = [
                "■ 1세대 실손 · 손해보험사 · 통원",
                f"총 진료 의료비: {won(total)}",
                "기본 공제 5,000원 후 100% 지급",
                f"계산상 지급액: {won(before)} / 통원 한도: {won(outpatient_limit)}",
            ]
        else:
            before = int(total * 0.8)
            pay = min(before, outpatient_limit)
            patient = total - pay
            lines = [
                f"■ 1세대 실손 · 생명보험사 {life_type} · 통원",
                f"총 진료 의료비: {won(total)}",
                "진료비 80% 지급",
                f"계산상 지급액: {won(before)} / 통원 한도: {won(outpatient_limit)}",
            ]

        drug_total = drug_g + drug_b
        if drug_total > 0:
            drug_before, drug_pay, drug_patient = safe_pay(drug_total, 5000, drug_limit)
            lines += [
                "",
                "■ 약제비 보상액",
                f"처방조제 합계: {won(drug_total)}",
                f"5,000원 공제 후 약제비 한도 {won(drug_limit)} 적용",
                f"약제비 수령 예상액: {won(drug_pay)} / 본인부담금: {won(drug_patient)}",
            ]
        return "1세대 계산 결과", lines, pay, patient

    if company == "손해보험사":
        pay = min(total, inpatient_limit)
        patient = total - pay
        lines = [
            "■ 1세대 실손 · 손해보험사 · 입원",
            "자기부담금 없음 — 100% 지급",
            f"총 진료 의료비: {won(total)}",
            f"입원 한도: {won(inpatient_limit)}",
        ]
        extra_pay = extra_patient = None
        if premium > 0:
            before = int(premium * 0.5)
            two_before = int(two_bed * 0.5)
            extra_pay = min(before, two_before) if two_bed > 0 else before
            extra_patient = premium - extra_pay
        return "1세대 계산 결과", lines, pay, patient, extra_pay, extra_patient

    before = int(total * 0.8)
    pay = min(before, inpatient_limit)
    patient = total - pay
    lines = [
        f"■ 1세대 실손 · 생명보험사 {life_type} · 입원",
        "진료비 80% 지급",
        f"총 진료 의료비: {won(total)}",
        f"입원 한도: {won(inpatient_limit)}",
    ]
    extra_pay = extra_patient = None
    if premium > 0:
        extra_pay, extra_patient = premium_room(premium, days)
    return "1세대 계산 결과", lines, pay, patient, extra_pay, extra_patient


def gen2_rates():
    if deductible_type == "표준형":
        return 0.20, 0.20
    if join_period in ["2009.08~2013.03", "2013.04~2015.08"]:
        return 0.10, 0.10
    return 0.10, 0.20


def gen2_drug_rates():
    if deductible_type == "표준형":
        return 0.20, 0.20
    if join_period == "2009.08~2013.03":
        return 0.10, 0.10
    if join_period == "2013.04~2015.08":
        return 0.20, 0.20
    return 0.10, 0.20


def calculate_gen2():
    limits = COMPANY_LIMITS_2_3[company]
    gr, br = gen2_rates()
    total = gubyeo + bigubyeo

    if treatment == "통원":
        fixed = HOSPITAL_FIXED[hospital_type]
        rate = int(gubyeo * gr) + int(bigubyeo * br)
        deductible = max(fixed, rate) if total > 0 else 0
        before, pay, patient = safe_pay(total, deductible, limits["outpatient"])

        lines = [
            f"■ 2세대 실손 · {join_period} · {company} · {deductible_type} · 통원",
            f"급여 {int(gr*100)}% / 비급여 {int(br*100)}%",
            f"총 진료비: {won(total)}",
            f"비용공제 {won(fixed)} VS 비율공제 {won(rate)} → 공제액 {won(deductible)}",
            f"계산상 지급액: {won(before)} / 통원 한도: {won(limits['outpatient'])}",
        ]

        drug_total = drug_g + drug_b
        if drug_total > 0:
            dgr, dbr = gen2_drug_rates()
            drug_rate = int(drug_g * dgr) + int(drug_b * dbr)
            drug_ded = max(8000, drug_rate)
            drug_before, drug_pay, drug_patient = safe_pay(drug_total, drug_ded, limits["drug"])
            lines += [
                "",
                "■ 약제비 보상액",
                f"약제비 합계: {won(drug_total)}",
                f"비용공제 8,000원 VS 비율공제 {won(drug_rate)} → 공제액 {won(drug_ded)}",
                f"약제비 수령 예상액: {won(drug_pay)} / 본인부담금: {won(drug_patient)}",
            ]
        return "2세대 계산 결과", lines, pay, patient

    rate = int(gubyeo * gr) + int(bigubyeo * br)
    before, pay, patient = safe_pay(total, rate, limits["inpatient"])
    lines = [
        f"■ 2세대 실손 · {join_period} · {company} · {deductible_type} · 입원",
        f"급여 {int(gr*100)}% / 비급여 {int(br*100)} 공제",
        f"총 진료 의료비: {won(total)}",
        f"공제액: {won(rate)} / 입원 한도: {won(limits['inpatient'])}",
    ]
    extra_pay = extra_patient = None
    if premium > 0:
        extra_pay, extra_patient = premium_room(premium, days)
    return "2세대 계산 결과", lines, pay, patient, extra_pay, extra_patient


def calculate_gen3():
    limits = COMPANY_LIMITS_2_3[company]

    if treatment == "통원":
        normal = gubyeo + bigubyeo
        fixed = HOSPITAL_FIXED[hospital_type]
        rate = int(gubyeo * 0.10) + int(bigubyeo * 0.20)
        normal_ded = max(fixed, rate) if normal > 0 else 0
        normal_pay = max(0, normal - normal_ded)

        special_ded = max(20000, int(special3 * 0.30)) if special3 > 0 else 0
        special_pay = max(0, special3 - special_ded)

        before = normal_pay + special_pay
        pay = min(before, limits["outpatient"])
        patient = normal + special3 - pay

        lines = [
            f"■ 3세대 실손 · {company} · 통원",
            "급여 10% / 비급여 20% / 3대 비급여 max(2만원, 30%)",
            f"일반 진료비: {won(normal)} / 일반 공제액: {won(normal_ded)}",
            f"3대 비급여: {won(special3)} / 3대 공제액: {won(special_ded)}",
            f"계산상 지급액: {won(before)} / 통원 한도: {won(limits['outpatient'])}",
        ]

        drug_total = drug_g + drug_b
        if drug_total > 0:
            drug_rate = int(drug_g * 0.10) + int(drug_b * 0.20)
            drug_ded = max(8000, drug_rate)
            drug_before, drug_pay, drug_patient = safe_pay(drug_total, drug_ded, limits["drug"])
            lines += [
                "",
                "■ 약제비 보상액",
                f"약제비 합계: {won(drug_total)}",
                f"비용공제 8,000원 VS 비율공제 {won(drug_rate)} → 공제액 {won(drug_ded)}",
                f"약제비 수령 예상액: {won(drug_pay)} / 본인부담금: {won(drug_patient)}",
            ]
        return "3세대 계산 결과", lines, pay, patient

    total = gubyeo + bigubyeo + special3
    ded = int(gubyeo * 0.10) + int(bigubyeo * 0.20)
    ded += max(20000, int(special3 * 0.30)) if special3 > 0 else 0
    before, pay, patient = safe_pay(total, ded, limits["inpatient"])
    lines = [
        f"■ 3세대 실손 · {company} · 입원",
        "급여 10% / 비급여 20% / 3대 비급여 max(2만원, 30%)",
        f"총 진료 의료비: {won(total)}",
        f"공제액: {won(ded)} / 입원 한도: {won(limits['inpatient'])}",
    ]
    extra_pay = extra_patient = None
    if premium > 0:
        extra_pay, extra_patient = premium_room(premium, days)
    return "3세대 계산 결과", lines, pay, patient, extra_pay, extra_patient


def calculate_gen4():
    if treatment == "통원":
        g_sum = gubyeo + drug_g
        b_sum = bigubyeo + drug_b

        g_fixed = HOSPITAL_FIXED[hospital_type]
        g_ded = max(g_fixed, int(g_sum * 0.20)) if g_sum > 0 else 0
        b_ded = max(30000, int(b_sum * 0.30)) if b_sum > 0 else 0
        s_ded = max(30000, int(special3 * 0.30)) if special3 > 0 else 0

        g_pay = max(0, g_sum - g_ded)
        b_pay = max(0, b_sum - b_ded)
        s_pay = max(0, special3 - s_ded)
        before = g_pay + b_pay + s_pay
        pay = min(before, 200000)
        patient = g_sum + b_sum + special3 - pay

        lines = [
            "■ 4세대 실손 · 통원",
            "급여(진료+약제), 비급여(진료+약제), 3대 비급여 각각 계산",
            f"급여 합산: {won(g_sum)} / 공제액: {won(g_ded)} / 지급액: {won(g_pay)}",
            f"비급여 합산: {won(b_sum)} / 공제액: {won(b_ded)} / 지급액: {won(b_pay)}",
            f"3대 비급여: {won(special3)} / 공제액: {won(s_ded)} / 지급액: {won(s_pay)}",
            f"통원 한도: {won(200000)}",
        ]
        return "4세대 계산 결과", lines, pay, patient

    total = gubyeo + bigubyeo + special3
    ded = int(gubyeo * 0.20) + int(bigubyeo * 0.30) + int(special3 * 0.30)
    before, pay, patient = safe_pay(total, ded, 50000000)
    lines = [
        "■ 4세대 실손 · 입원",
        "급여 20% / 비급여 30% / 3대 비급여 30%",
        f"총 진료 의료비: {won(total)}",
        f"공제액: {won(ded)} / 입원 한도: 50,000,000원",
    ]
    extra_pay = extra_patient = None
    if premium > 0:
        extra_pay, extra_patient = premium_room(premium, days)
    return "4세대 계산 결과", lines, pay, patient, extra_pay, extra_patient


def calculate_gen5():
    if treatment == "통원":
        g_sum = gubyeo + drug_g
        nonsev_sum = nonsevere + drug_b
        health_rate = {"의원": 0.30, "병원": 0.40, "종합/상급종합": 0.50}[hospital_type]
        fixed = HOSPITAL_FIXED[hospital_type]

        health_ded = int(gubyeo * health_rate) + int(drug_g * 0.30)
        ratio_ded = int(g_sum * 0.20)
        g_ded = max(health_ded, ratio_ded, fixed) if g_sum > 0 else 0
        g_pay = max(0, g_sum - g_ded)

        nonsev_ded = max(50000, int(nonsev_sum * 0.50)) if nonsev_sum > 0 else 0
        nonsev_pay = max(0, nonsev_sum - nonsev_ded)

        sev_ded = max(30000, int(severe * 0.30)) if severe > 0 else 0
        sev_pay = max(0, severe - sev_ded)

        before = g_pay + nonsev_pay + sev_pay
        pay = min(before, 200000)
        patient = g_sum + nonsev_sum + severe - pay

        lines = [
            "■ 5세대 실손 · 통원",
            "급여 건보연동 / 비중증 max(5만원, 50%) / 중증 max(3만원, 30%)",
            f"급여 합산: {won(g_sum)} / 공제액: {won(g_ded)} / 지급액: {won(g_pay)}",
            f"비중증 합산: {won(nonsev_sum)} / 공제액: {won(nonsev_ded)} / 지급액: {won(nonsev_pay)}",
            f"중증 비급여: {won(severe)} / 공제액: {won(sev_ded)} / 지급액: {won(sev_pay)}",
            "비급여 약제비는 비중증 비급여 합산에 포함",
            f"통원 한도: {won(200000)}",
        ]
        return "5세대 계산 결과", lines, pay, patient

    total = gubyeo + nonsevere + severe
    ded = int(gubyeo * 0.20) + int(nonsevere * 0.50) + int(severe * 0.30)
    before, pay, patient = safe_pay(total, ded, 50000000)
    lines = [
        "■ 5세대 실손 · 입원",
        "급여 20% / 비중증 비급여 50% / 중증 비급여 30%",
        f"총 진료 의료비: {won(total)}",
        f"공제액: {won(ded)} / 입원 한도: 50,000,000원",
    ]
    extra_pay = extra_patient = None
    if premium > 0:
        extra_pay, extra_patient = premium_room(premium, days)
    return "5세대 계산 결과", lines, pay, patient, extra_pay, extra_patient


def calculate_senior():
    total = gubyeo + bigubyeo

    if treatment == "통원":
        ded = max(30000, int(gubyeo * 0.20) + int(bigubyeo * 0.30)) if total > 0 else 0
        before, pay, patient = safe_pay(total, ded, 1000000)
        lines = [
            "■ 노후실비 · 통원",
            "급여 20% / 비급여 30% / 최소공제 3만원",
            f"총 진료 의료비: {won(total)}",
            f"공제액: {won(ded)} / 통원 한도: 1,000,000원",
        ]

        drug_total = drug_g + drug_b
        if drug_total > 0:
            drug_ded = int(drug_total * 0.20)
            drug_before, drug_pay, drug_patient = safe_pay(drug_total, drug_ded, 1000000)
            lines += [
                "",
                "■ 약제비 보상액",
                f"처방조제 합계: {won(drug_total)}",
                f"20% 공제: {won(drug_ded)}",
                f"약제비 수령 예상액: {won(drug_pay)} / 본인부담금: {won(drug_patient)}",
            ]
        return "노후실비 계산 결과", lines, pay, patient

    ded = max(300000, int(gubyeo * 0.20) + int(bigubyeo * 0.30)) if total > 0 else 0
    before, pay, patient = safe_pay(total, ded, 100000000)
    lines = [
        "■ 노후실비 · 입원",
        "급여 20% / 비급여 30% / 최소공제 30만원",
        f"총 진료 의료비: {won(total)}",
        f"공제액: {won(ded)} / 입원 한도: 100,000,000원",
    ]
    extra_pay = extra_patient = None
    if premium > 0:
        extra_pay, extra_patient = premium_room(premium, days)
    return "노후실비 계산 결과", lines, pay, patient, extra_pay, extra_patient


def calculate_impaired():
    total = gubyeo + bigubyeo

    if treatment == "통원":
        ded = max(20000, int(total * 0.30)) if total > 0 else 0
        before, pay, patient = safe_pay(total, ded, 200000)
        lines = [
            "■ 유병자실비 · 통원",
            "처방조제비 미보상",
            "공제액 = max(2만원, 총 진료비 × 30%)",
            f"총 진료 의료비: {won(total)}",
            f"공제액: {won(ded)} / 통원 한도: 200,000원",
        ]
        return "유병자실비 계산 결과", lines, pay, patient

    ded = max(100000, int(total * 0.30)) if total > 0 else 0
    before, pay, patient = safe_pay(total, ded, 50000000)
    lines = [
        "■ 유병자실비 · 입원",
        "공제액 = max(10만원, 총 진료비 × 30%)",
        "자기부담 연 200만원 한도는 누적 관리 필요",
        f"총 진료 의료비: {won(total)}",
        f"공제액: {won(ded)} / 입원 한도: 50,000,000원",
    ]
    extra_pay = extra_patient = None
    if premium > 0:
        extra_pay, extra_patient = premium_room(premium, days)
    return "유병자실비 계산 결과", lines, pay, patient, extra_pay, extra_patient


if calculate:
    if generation == "1세대":
        result = calculate_gen1()
    elif generation == "2세대":
        result = calculate_gen2()
    elif generation == "3세대":
        result = calculate_gen3()
    elif generation == "4세대":
        result = calculate_gen4()
    elif generation == "5세대":
        result = calculate_gen5()
    elif generation == "노후실비":
        result = calculate_senior()
    else:
        result = calculate_impaired()

    if len(result) == 4:
        title, lines, receive, patient = result
        markdown_result(title, lines, receive, patient)
    else:
        title, lines, receive, patient, extra_receive, extra_patient = result
        markdown_result(title, lines, receive, patient, extra_receive, extra_patient)

else:
    st.markdown(
        """
<div class="section-card">
<b>사용 방법</b><br>
왼쪽에서 가입 상품과 조건을 선택하고, 진료비 영수증 금액을 입력한 뒤 <b>계산하기</b>를 누르세요.
</div>
""",
        unsafe_allow_html=True,
    )
