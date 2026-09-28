import streamlit as st

st.set_page_config(page_title="구정숙 | 수학교사", page_icon="✨", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #fffaf5 0%, #f4f7f2 55%, #f7f8fc 100%);
}
[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 820px;
    padding-top: 3.5rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #202b27;
}
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.78);
    border: 1px solid rgba(32, 43, 39, 0.08);
    border-radius: 8px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.caption("MATH EDUCATOR · SEOUL")
st.title("구정숙")
st.subheader("도전으로 변화를 만들고, 교육의 본질을 향합니다.")

metric_cols = st.columns(3)
metric_cols[0].metric("교육 경력", "25년")
metric_cols[1].metric("전문 분야", "수학교육")
metric_cols[2].metric("현재 역할", "연구특성화부장")

st.info("🎯 2026년의 방향  ·  일보다 삶을 우선하고, 여유와 자기 돌봄을 선택합니다.")

education_tab, life_tab = st.tabs(["교육과 관심 분야", "일상과 연락처"])

with education_tab:
    st.subheader("더 나은 배움의 경험을 만듭니다")
    focus_cols = st.columns(2)
    with focus_cols[0]:
        st.markdown("#### 수업과 평가")
        st.markdown("학생 참여형 수업 설계  ·  과정 중심 평가  ·  수업-평가 일체화")
        st.markdown("#### 학습 지원")
        st.markdown("기초학력 향상  ·  학습격차 해결")
    with focus_cols[1]:
        st.markdown("#### 교육의 변화")
        st.markdown("AI·디지털 기반 교육혁신  ·  교육 정책과 현장의 연결")
        st.markdown("#### 함께 성장하기")
        st.markdown("교사 성장  ·  조직 변화")

with life_tab:
    st.subheader("움직이고, 꾸준히 돌봅니다")
    st.markdown("🚴 자전거  ·  🎾 테니스  ·  🏊 수영  ·  🏋️ 헬스")
    st.markdown("건강한 식습관과 충분한 수분 섭취, 긍정적인 마음가짐을 지향합니다.")
    st.markdown("---")
    st.markdown("**연락처**")
    st.markdown("[📧 scatchi@sen.go.kr](mailto:scatchi@sen.go.kr)")

st.divider()
st.caption("© 2026 구정숙")