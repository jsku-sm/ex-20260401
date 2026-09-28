from html import escape
from pathlib import Path

import streamlit as st


# ── 1. 기본 정보: 이후 변경할 내용은 이곳에서 수정하세요. ──────────
PROFILE = {
    "name": "구정숙",
    "experience": "25년",  # 기존 코드의 경력 연수를 유지했습니다.
    "school": "경복비즈니스고등학교",
    "role": "연구특성화부장",
    "degree": "숙명여자대학교 AI융합교육 석사과정",
    "degree_period": "2025.09 ~",
    "slogan": "도전으로 변화를 만들고, 교육의 본질을 향합니다.",
    "motto": "연구하는 마음은 배움에 대한 겸손이요, 학생들을 향한 가장 깊은 사랑이다.",
    "email": "scatchi@sen.go.kr",
    "gmail": "scatchi99@gmail.com",
}

ACTIVITIES = [
    "AI 에듀테크 선도교사단 (2025, 2026)",
    "인공지능 교육서비스 선도교사",
    "AIDT 선도교원",
    "새싹연구교사",
    "수업평가나눔 분임장",
]

QUALIFICATIONS = [
    "교실혁명선도교사",
    "디지털수업평가 전문가",
    "2022 교육과정 수업전문가",
    "AIEDAP 마스터교원",
]

LECTURE_SCHOOLS = [
    "정신여자고등학교", "중동고등학교", "동구고등학교",
    "마포고등학교", "경복여고", "대일고",
]

FOCUS_AREAS = [
    ("수업과 평가", ["학생 참여형 수업 설계", "과정 중심 평가 · 수업–평가 일체화"]),
    ("학습 지원", ["기초학력 향상", "학습격차 해소를 위한 맞춤형 지원"]),
    ("교육의 변화", ["AI·디지털 기반 교육혁신", "교육 정책과 교실 현장의 연결"]),
    ("함께 성장하기", ["교사 성장과 수업 나눔", "함께 배우는 학교 문화와 조직 변화"]),
]

# 실행 명령을 입력한 위치와 관계없이 이 코드 파일의 폴더를 기준으로 찾습니다.
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title=f"{PROFILE['name']} | 수학교사 · AI 교육 전문가",
    page_icon="🌿",
    layout="wide",
)


# ── 2. 화면 디자인 ────────────────────────────────────────────
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(145deg, #fffaf5 0%, #f4f7f2 55%, #f7f5fc 100%);
    color: #263a30;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
                 "Malgun Gothic", sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 2.8rem; padding-bottom: 2rem; }
h1, h2, h3, h4 { color: #263a30 !important; word-break: keep-all; }
[data-testid="stMarkdownContainer"] { color: #34453c; }
[data-testid="stCaptionContainer"] p { color: #747d76; }
[data-testid="stImage"] img { border-radius: 24px; }

/* QR 이미지는 모서리를 자르거나 형태를 바꾸지 않습니다. */
.st-key-contact_qr [data-testid="stImage"] img { border-radius: 0 !important; }

/* 학력 문구는 작은 회색 캡션 대신 진한 글씨로 표시합니다. */
.academic-line {
    color: #24392d !important;
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.8;
    background: #edf2e9;
    border-left: 4px solid #7e967b;
    border-radius: 0 10px 10px 0;
    padding: .75rem 1rem;
    margin: .5rem 0 1rem;
    word-break: keep-all;
}
.eyebrow {
    color: #86719c;
    font-size: .8rem;
    font-weight: 700;
    letter-spacing: .16em;
}
.hero-description { color: #5f6f64; line-height: 1.85; margin-top: .6rem; }
.tag {
    display: inline-block; background: #fff; color: #526458;
    border: 1px solid #dde5dd; border-radius: 999px;
    padding: .32rem .8rem; margin: .15rem .3rem .3rem 0; font-size: .88rem;
}
.quote-banner {
    background: #eaf0e8; border-left: 5px solid #869d83;
    border-radius: 0 18px 18px 0; padding: 1.35rem 1.5rem;
    margin: 1.4rem 0; color: #3a5541;
    font-size: 1.08rem; line-height: 1.8; word-break: keep-all;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,.86); border: 1px solid #e5e9e1;
    border-radius: 18px; padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] { color: #69786c; }
[data-testid="stMetricValue"] { color: #304c39; font-size: 1.55rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: .65rem; margin-top: 1rem; }
.stTabs [data-baseweb="tab"] { color: #637167; font-weight: 600; }
.stTabs [aria-selected="true"] { color: #75578d !important; }
.info-card {
    background: rgba(255,255,255,.93); border: 1px solid #e4e8e1;
    border-top: 4px solid #98b29b; border-radius: 18px;
    padding: 1.3rem 1.4rem; margin-bottom: 1rem;
    box-shadow: 0 5px 18px rgba(41,57,43,.035);
}
.info-card.purple { border-top-color: #b3a0c8; }
.info-card.gold { border-top-color: #d3b16d; }
.info-card h4 { margin: 0 0 .75rem; padding: 0; font-size: 1.1rem; }
.info-card p {
    color: #526156;
    margin: .35rem 0;
    line-height: 1.75;
    word-break: keep-all;
}
.award-card {
    background: linear-gradient(120deg, #fff6df, #fffdfa);
    border: 1px solid #ead6aa; border-radius: 20px;
    padding: 1.4rem 1.5rem; margin: .6rem 0 1.3rem;
}
.award-card .year { color: #8b672e; font-weight: 700; font-size: .85rem; }
.award-card h3 { margin: .3rem 0; padding: 0; font-size: 1.35rem; }
.award-card p { color: #846e48; margin: .35rem 0 0; }
[data-testid="stExpander"] details {
    background: #fff;
    color: #34453c;
    border-radius: 14px;
}
[data-testid="stExpander"] summary { color: #34453c; }
.stDownloadButton button { background: #fff; color: #34453c; border-radius: 12px; }
.footer { text-align: center; color: #7c857d; font-size: .86rem; padding: .8rem 0; }
@media (max-width: 640px) {
    .block-container { padding: 1.5rem 1rem; }
    .quote-banner { font-size: 1rem; padding: 1rem; }
    .info-card { padding: 1.1rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ── 3. 공통 표시 함수 ──────────────────────────────────────────
def show_image(
    filename: str,
    caption: str | None = None,
    width: int | str = "stretch",
) -> None:
    """코드와 같은 폴더의 이미지를 표시하고, 없으면 안내합니다."""
    path = BASE_DIR / filename

    if not path.is_file():
        st.warning(
            f"이미지를 표시하려면 {filename} 파일을 "
            "streamlit_app.py와 같은 폴더에 넣어 주세요."
        )
        return

    try:
        st.image(
            str(path),
            caption=caption,
            width=width,
            output_format="PNG",
        )
    except (OSError, ValueError):
        st.warning(
            f"{filename} 파일을 읽지 못했습니다. "
            "정상적인 PNG 이미지인지 확인해 주세요."
        )


def tags(items: list[str]) -> None:
    html = "".join(
        f'<span class="tag">{escape(item)}</span>'
        for item in items
    )
    st.markdown(html, unsafe_allow_html=True)


def card(title: str, lines: list[str], tone: str = "green") -> None:
    tone = tone if tone in {"green", "purple", "gold"} else "green"
    body = "".join(f"<p>{escape(line)}</p>" for line in lines)

    st.markdown(
        f'<div class="info-card {tone}">'
        f'<h4>{escape(title)}</h4>{body}</div>',
        unsafe_allow_html=True,
    )


def introduction_text() -> str:
    """화면에 표시한 정보로 내려받을 소개문을 만듭니다."""
    lines = [
        f"{PROFILE['name']} | 수학교사 · AI 교육 전문가",
        PROFILE["slogan"], "", PROFILE["motto"], "",
        "[현재]",
        f"{PROFILE['school']} {PROFILE['role']}",
        f"교육 경력: {PROFILE['experience']}",
        f"{PROFILE['degree']} ({PROFILE['degree_period']})", "",
        "[수상]", "2025 디지털교육부문 교육부장관상 수상", "",
        "[주요 활동]", *ACTIVITIES, "",
        "[연수 · 전문성]", *QUALIFICATIONS,
        "AI 디지털 해외 글로벌 연수: 프랑스·덴마크 (2026.01)", "",
        "[강의 경력]", " · ".join(LECTURE_SCHOOLS),
        "서울시 직업계고 전체 수학교사 대상 기초학력향상 디지털수업 연수", "",
        "[교육과 관심 분야]",
    ]

    for title, descriptions in FOCUS_AREAS:
        lines.append(f"{title}: {' · '.join(descriptions)}")

    lines.extend([
        "",
        "[연락처]",
        PROFILE["email"],
        PROFILE["gmail"],
    ])
    return "\n".join(lines)


# ── 4. 메인 프로필 ────────────────────────────────────────────
image_col, intro_col = st.columns(
    [1, 1.85],
    gap="large",
    vertical_alignment="center",
)

with image_col:
    show_image("profile.png")

with intro_col:
    st.markdown(
        '<div class="eyebrow">MATH × AI · GOOD TEACHER</div>',
        unsafe_allow_html=True,
    )
    st.title(PROFILE["name"])
    st.markdown("**수학교사 · AI 교육 전문가**")
    st.subheader(PROFILE["slogan"])
    st.markdown(f"**{PROFILE['school']} · {PROFILE['role']}**")

    # 학력 문구를 진한 색상과 굵은 글씨로 표시합니다.
    st.markdown(
        f'<div class="academic-line">{escape(PROFILE["degree"])}'
        f' | {escape(PROFILE["degree_period"])}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="hero-description">수학을 통해 학생과 소통하고,<br>'
        'AI·디지털 기술을 더 깊은 배움으로 연결합니다.</p>',
        unsafe_allow_html=True,
    )
    tags(["수학교육", "AI·디지털 교육", "교사 성장"])

st.markdown(
    f'<div class="quote-banner">“{escape(PROFILE["motto"])}”</div>',
    unsafe_allow_html=True,
)

metric_cols = st.columns(3)
metric_cols[0].metric("교육 경력", PROFILE["experience"])
metric_cols[1].metric("전문 분야", "수학 · AI 교육")
metric_cols[2].metric("현재 역할", PROFILE["role"])


# ── 5. 네 개의 탭 ──────────────────────────────────────────────
education_tab, career_tab, lecture_tab, contact_tab = st.tabs([
    "🌱 교육과 관심 분야",
    "🏅 경력과 주요 활동",
    "🎤 강의와 나눔",
    "📧 연락처",
])

with education_tab:
    st.subheader("더 나은 배움의 경험을 만듭니다")
    st.write(
        "기술의 새로움보다 학생에게 일어나는 배움의 변화에 주목합니다. "
        "학생이 참여하고, 자신의 생각을 표현하며, "
        "작은 성장을 경험하는 수업을 지향합니다."
    )

    for start in range(0, len(FOCUS_AREAS), 2):
        columns = st.columns(2, gap="medium")
        for col, (title, lines) in zip(
            columns,
            FOCUS_AREAS[start:start + 2],
        ):
            with col:
                card(title, lines)

    st.markdown("#### 배움을 멈추지 않는 교사")
    st.write(
        "교실에서 만난 질문을 연구로 이어 가고, "
        "연구에서 얻은 통찰을 다시 수업으로 가져옵니다. "
        "동료 교사들과 경험을 나누며 교육의 본질을 함께 고민합니다."
    )

with career_tab:
    st.subheader("배우고, 실천하고, 나누어 온 발자취")

    st.markdown(
        '<div class="award-card">'
        '<div class="year">🏆 2025 · 수상</div>'
        '<h3>디지털교육부문 교육부장관상</h3>'
        '<p>AI·디지털 교육을 향한 연구와 실천을 이어 갑니다.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="medium")

    with left:
        card(
            "현재와 학업",
            [
                f"{PROFILE['school']} {PROFILE['role']}",
                PROFILE["degree"],
                PROFILE["degree_period"],
            ],
            "purple",
        )
        card("주요 활동", ACTIVITIES)

    with right:
        card(
            "글로벌 연수",
            [
                "AI 디지털 해외 글로벌 연수",
                "프랑스 · 덴마크",
                "2026.01",
            ],
            "gold",
        )
        card("연수 · 전문성", QUALIFICATIONS, "purple")

with lecture_tab:
    st.subheader("교실의 경험을 나누고, 함께 성장합니다")
    st.markdown("#### 학교 강의 경력")
    tags(LECTURE_SCHOOLS)
    st.write("")

    card(
        "수학교사 대상 연수",
        [
            "서울시 직업계고 전체 수학교사 대상",
            "기초학력향상 디지털수업 연수",
        ],
    )

    with st.expander(
        "💡 함께 나누고 싶은 교육 주제",
        expanded=True,
    ):
        st.markdown(
            "**AI·디지털 수업** — 기술 활용을 학생의 배움으로 연결하기\n\n"
            "**수업과 평가** — 학생 참여형 수업과 과정 중심 평가 설계하기\n\n"
            "**기초학력** — 작은 성공 경험으로 학습의 출발점 만들기\n\n"
            "**교사 성장** — 실천과 성찰을 나누는 동료 학습 문화 만들기"
        )

    st.markdown(
        f"강의·협업 문의: "
        f"[{PROFILE['email']}](mailto:{PROFILE['email']})"
    )


# ── 6. 연락처: 이메일과 첨부 QR 이미지 ─────────────────────────
with contact_tab:
    st.subheader("연락처")
    st.write("강의·연수·교육 협업에 관한 문의를 보내 주세요.")

    email_col, qr_col = st.columns(
        [1.4, 1],
        gap="large",
    )

    with email_col:
        st.markdown("#### 이메일")

        st.markdown("**교육청 이메일**")
        st.markdown(
            f"📧 [{PROFILE['email']}](mailto:{PROFILE['email']})"
        )

        st.markdown("**Gmail**")
        st.markdown(
            f"📧 [{PROFILE['gmail']}](mailto:{PROFILE['gmail']})"
        )

        st.caption(
            "이메일 주소를 클릭하면 기기에 설정된 메일 앱으로 연결됩니다."
        )

    with qr_col:
        with st.container(key="contact_qr"):
            st.markdown("#### QR 코드")

            # 첨부한 QR 이미지를 그대로 표시합니다.
            show_image("contact_qr.png", width=300)

            st.caption("휴대전화 카메라로 QR 코드를 스캔해 주세요.")

    st.divider()

    st.download_button(
        label="📄 소개문 내려받기 (.txt)",
        data=introduction_text().encode("utf-8-sig"),
        file_name="구정숙_프로필.txt",
        mime="text/plain; charset=utf-8",
        on_click="ignore",
        width="stretch",
    )


# ── 7. 하단 문구 ──────────────────────────────────────────────
st.divider()
st.markdown(
    f'<div class="footer">© 2026 {escape(PROFILE["name"])}'
    ' · 배우고, 나누고, 함께 성장합니다.</div>',
    unsafe_allow_html=True,
)