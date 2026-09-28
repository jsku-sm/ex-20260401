from html import escape
from pathlib import Path

import streamlit as st


# ── 1. 기본 정보 ─────────────────────────────────────────────
PROFILE = {
    "name": "구정숙",
    "experience": "25년",
    "slogan": "도전으로 변화를 만들고, 교육의 본질을 향합니다.",
    "motto": "연구하는 마음은 배움에 대한 겸손이요, 학생들을 향한 가장 깊은 사랑이다.",
    "email": "scatchi@sen.go.kr",
}

ACTIVITIES = [
    "AI 에듀테크 선도교사단 (2025, 2026)",
    "강서양천 연수기획단(2025, 2026)",
    "인공지능 교육서비스 선도교사",
    "AIDT 선도교원",
    "새싹연구교사",
    "수업평가나눔 분임장",
    "천재교육 서논술형 평가 지원 플랫폼 개발 자문위원",
]

QUALIFICATIONS = [
    "교실혁명선도교사",
    "디지털수업평가 전문가",
    "2022 교육과정 수업전문가",
    "AIEDAP 마스터교원",
    "AI 디지털기반 수업 평가 전문가 프로젝트1기",
    "2026 AI지식역량강화 심화연수",
]

LECTURE_SCHOOLS = [
    "정신여자고등학교", "중동고등학교", "동구고등학교",
    "마포고등학교", "경복여고", "대일고", "여의도중학교",
]

TRAINING_TEXT = "서울시 직업계고 수학교사 대상 기초학력향상 디지털수업연수"

FOCUS_AREAS = [
    ("수업과 평가", ["학생 참여형 수업 설계", "과정 중심 평가 · 수업–평가 일체화"]),
    ("학습 지원", ["기초학력 향상", "학습격차 해소를 위한 맞춤형 지원"]),
    ("교육의 변화", ["AI·디지털 기반 교육혁신", "교육 정책과 교실 현장의 연결"]),
    ("함께 성장하기", ["교사 성장과 수업 나눔", "함께 배우는 학교 문화와 조직 변화"]),
]

SHARING_TOPICS = [
    ("AI·디지털 수업", "기술 활용을 학생의 배움으로 연결하기"),
    ("수업과 평가", "학생 참여형 수업과 과정 중심 평가 설계하기"),
    ("기초학력", "작은 성공 경험으로 학습의 출발점 만들기"),
    ("교사 성장", "실천과 성찰을 나누는 동료 학습 문화 만들기"),
]

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title=f"{PROFILE['name']} | 수학교사 · AI 교육 전문가",
    page_icon="🌿",
    layout="wide",
)


# ── 2. 화면 디자인 ───────────────────────────────────────────
CSS = """
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
.st-key-profile_image img { border-radius: 24px; }
.eyebrow { color: #755d8d; font-size: .8rem; font-weight: 700; letter-spacing: .16em; }
.hero-description { color: #526358; line-height: 1.85; margin-top: .6rem; }
.tag {
    display: inline-block; background: #fff; color: #526458;
    border: 1px solid #dde5dd; border-radius: 999px;
    padding: .32rem .8rem; margin: .15rem .3rem .3rem 0; font-size: .88rem;
}
.profile-quote {
    margin: .9rem .15rem 0;
    padding: .85rem .9rem;
    border-top: 1px solid #d9e2d7;
    color: #526358;
    font-size: .94rem;
    font-style: italic;
    line-height: 1.8;
    text-align: center;
    word-break: keep-all;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,.86); border: 1px solid #e5e9e1;
    border-radius: 18px; padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] { color: #5c6b5f; }
[data-testid="stMetricValue"] { color: #304c39; font-size: 1.55rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: .65rem; margin-top: 1rem; }
.stTabs [data-baseweb="tab"] { color: #526257; font-weight: 600; }
.stTabs [aria-selected="true"] { color: #75578d !important; }
.info-card {
    box-sizing: border-box; background: rgba(255,255,255,.95);
    border: 1px solid #dfe6dd; border-top: 4px solid #98b29b;
    border-radius: 18px; padding: 1.35rem 1.45rem; margin-bottom: 1rem;
    box-shadow: 0 5px 18px rgba(41,57,43,.035);
}
.info-card.purple { border-top-color: #b3a0c8; }
.info-card.gold { border-top-color: #d3b16d; }
.info-card h4 { margin: 0 0 .85rem; padding: 0; font-size: 1.15rem; }
.info-card p { color: #405447; margin: .4rem 0; line-height: 1.85; word-break: keep-all; }
.detail-list { list-style: none; margin: 0; padding: 0; }
.detail-list li {
    color: #405447; padding: .65rem 0; line-height: 1.8;
    border-bottom: 1px solid #edf0ea; word-break: keep-all;
}
.detail-list li:last-child { border-bottom: 0; padding-bottom: .1rem; }
.award-card {
    background: linear-gradient(120deg, #fff6df, #fffdfa);
    border: 1px solid #ead6aa; border-radius: 20px;
    padding: 1.4rem 1.5rem; margin: .6rem 0 1.3rem;
}
.award-card .year { color: #805b22; font-weight: 700; font-size: .85rem; }
.award-card h3 { margin: .3rem 0; padding: 0; font-size: 1.35rem; }
.award-card p { color: #745d36; margin: .35rem 0 0; }

/* 번호와 제목을 하나의 문장으로, 가로 전체 너비에 표시합니다. */
.section-title {
    display: block;
    box-sizing: border-box;
    width: 100%;
    writing-mode: horizontal-tb;
    white-space: nowrap;
    word-break: normal;
    overflow-wrap: normal;
    font-size: clamp(.9rem, 3.5vw, 1.18rem);
    font-weight: 700;
    line-height: 1.6;
    color: #304c39;
    background: #eaf0e8;
    border-left: 4px solid #869d83;
    border-radius: 0 12px 12px 0;
    padding: .75rem 1rem;
    margin: 1.3rem 0 1rem;
}
.school-grid {
    display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: .65rem; list-style: none; margin: 0; padding: 0;
}
.school-grid li {
    background: #f3f6ef; border: 1px solid #e2e9dd;
    border-radius: 10px; padding: .75rem .85rem;
    font-size: 1rem; font-weight: 600; color: #324b39; word-break: keep-all;
}

/* 연수 문구는 한 줄로 표시하며 좁은 화면에서는 가로 스크롤됩니다. */
.training-summary {
    box-sizing: border-box;
    width: 100%;
    margin-top: 1.1rem;
    padding: 1rem 1.1rem;
    border: 1px solid #e4dceb;
    border-radius: 12px;
    background: #f7f3fa;
    color: #4d3f5b;
    font-size: 1.03rem;
    font-weight: 600;
    line-height: 1.8;
    white-space: nowrap;
    overflow-x: auto;
}
.topic-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.topic-grid .info-card { margin-bottom: 0; }
.footer { text-align: center; color: #626e65; font-size: .86rem; padding: .8rem 0; }
@media (max-width: 720px) {
    .block-container { padding: 1.5rem 1rem; }
    .profile-quote { font-size: .9rem; padding: .75rem .5rem; }
    .info-card { padding: 1.1rem; }
    .school-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .topic-grid { grid-template-columns: 1fr; }
}
@media (max-width: 380px) {
    .school-grid { grid-template-columns: 1fr; }
    .section-title { padding: .7rem .6rem; }
}
</style>
"""
st.html(CSS)


# ── 3. 공통 함수 ─────────────────────────────────────────────
def render_html(body: str) -> None:
    """HTML을 현재 영역의 전체 너비로 표시합니다."""
    st.html(body, width="stretch")


def show_profile_image() -> None:
    """코드와 같은 폴더의 프로필 이미지를 표시합니다."""
    path = BASE_DIR / "profile.png"
    if not path.is_file():
        st.warning("profile.png 파일을 streamlit_app.py와 같은 폴더에 넣어 주세요.")
        return
    try:
        st.image(str(path), width="stretch", output_format="PNG")
    except (OSError, ValueError):
        st.warning("profile.png 파일을 읽지 못했습니다. 이미지 파일을 확인해 주세요.")


def tags(items: list[str]) -> None:
    body = "".join(f'<span class="tag">{escape(item)}</span>' for item in items)
    render_html(f"<div>{body}</div>")


def card(title: str, lines: list[str], tone: str = "green") -> None:
    tone = tone if tone in {"green", "purple", "gold"} else "green"
    body = "".join(f"<li>{escape(line)}</li>" for line in lines)
    render_html(
        f'<div class="info-card {tone}"><h4>{escape(title)}</h4>'
        f'<ul class="detail-list">{body}</ul></div>'
    )


def section_heading(number: str, title: str) -> None:
    # 번호와 제목을 서로 다른 칸으로 나누지 않습니다.
    text = escape(f"{number} {title}")
    render_html(
        f'<div class="section-title" role="heading" aria-level="3">{text}</div>'
    )


# ── 4. 메인 프로필 ───────────────────────────────────────────
image_col, intro_col = st.columns([1, 1.85], gap="large", vertical_alignment="center")
with image_col:
    with st.container(key="profile_image"):
        show_profile_image()
    render_html(
        f'<div class="profile-quote">“{escape(PROFILE["motto"])}”</div>'
    )

with intro_col:
    render_html('<div class="eyebrow">MATH × AI · GOOD TEACHER</div>')
    st.title(PROFILE["name"])
    st.markdown("**수학교사 · AI 교육 전문가**")
    st.subheader(PROFILE["slogan"])
    render_html(
        '<p class="hero-description">수학을 통해 학생과 소통하고,<br>'
        'AI·디지털 기술을 더 깊은 배움으로 연결합니다.</p>'
    )
    tags(["수학교육", "AI·디지털 교육", "교사 성장"])

# ── 5. 탭 구성 ───────────────────────────────────────────────
education_tab, career_tab, lecture_tab, contact_tab = st.tabs([
    "🌱 교육과 관심 분야", "🏅 경력과 주요 활동", "🎤 강의와 나눔", "📧 연락처",
])

with education_tab:
    st.subheader("더 나은 배움의 경험을 만듭니다")
    st.write(
        "기술의 새로움보다 학생에게 일어나는 배움의 변화에 주목합니다. "
        "학생이 참여하고, 자신의 생각을 표현하며, 작은 성장을 경험하는 수업을 지향합니다."
    )
    for start in range(0, len(FOCUS_AREAS), 2):
        columns = st.columns(2, gap="medium")
        for col, (title, lines) in zip(columns, FOCUS_AREAS[start:start + 2]):
            with col:
                card(title, lines)
    st.markdown("#### 배움을 멈추지 않는 교사")
    st.write(
        "교실에서 만난 질문을 연구로 이어 가고, 연구에서 얻은 통찰을 다시 수업으로 가져옵니다. "
        "동료 교사들과 경험을 나누며 교육의 본질을 함께 고민합니다."
    )

with career_tab:
    st.subheader("배우고, 실천하고, 나누어 온 발자취")
    render_html(
        '<div class="award-card"><div class="year">🏆 2025 · 수상</div>'
        '<h3>디지털교육부문 교육부장관상</h3>'
        '<p>AI·디지털 교육을 향한 연구와 실천을 이어 갑니다.</p></div>'
    )
    left, right = st.columns(2, gap="medium")
    with left:
        card("주요 활동", ACTIVITIES)
    with right:
        card("연수 · 전문성", QUALIFICATIONS, "purple")
    card("글로벌 연수", ["AI 디지털 해외 글로벌 연수", "프랑스 · 덴마크 | 2026.01"], "gold")

with lecture_tab:
    st.subheader("교실의 경험을 나누고, 함께 성장합니다")

    section_heading("01", "강의·연수 경력")
    school_items = "".join(f"<li>{escape(school)}</li>" for school in LECTURE_SCHOOLS)
    render_html(
        '<div class="info-card"><h4>학교 강의 경력</h4>'
        f'<ul class="school-grid">{school_items}</ul>'
        f'<div class="training-summary">{escape(TRAINING_TEXT)}</div>'
        '</div>'
    )

    section_heading("02", "함께 나누고 싶은 교육 주제")
    topic_cards = "".join(
        f'<div class="info-card"><h4>{escape(title)}</h4>'
        f'<p>{escape(description)}</p></div>'
        for title, description in SHARING_TOPICS
    )
    render_html(f'<div class="topic-grid">{topic_cards}</div>')

with contact_tab:
    # 연락처에는 교육청 이메일만 표시합니다.
    st.markdown("#### 교육청 이메일")
    st.markdown(f"📧 [{PROFILE['email']}](mailto:{PROFILE['email']})")


# ── 6. 공통 하단 문구 ────────────────────────────────────────
st.divider()
render_html(
    f'<div class="footer">© 2026 {escape(PROFILE["name"])}'
    ' · 배우고, 나누고, 함께 성장합니다.</div>'
)