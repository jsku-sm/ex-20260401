import streamlit as st
import base64

st.set_page_config(page_title="구정숙 프로필", page_icon="✨", layout="centered")

# 배경 이미지를 base64로 인코딩하여 설정
def get_base64_image(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    img_base64 = get_base64_image("ex-20260401/cherry_blossom.jpg")
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)),
            url('data:image/jpeg;base64,{img_base64}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp > header {{
        background-color: rgba(255, 255, 255, 0);
    }}

    .stMarkdown, .stHeader, .stSubheader, .stWrite {{
        color: rgba(0, 0, 0, 1);
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3), 0px 0px 3px rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }}

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: rgba(0, 0, 0, 1);
        text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.3), 0px 0px 4px rgba(255, 255, 255, 0.9);
        font-weight: 600;
    }}
    </style>
    """, unsafe_allow_html=True)
except:
    st.markdown("""
    <style>
    .stMarkdown, .stHeader, .stSubheader, .stWrite {
        color: rgba(0, 0, 0, 0.85);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("안녕하세요, 저는 구정숙입니다 ✨")
st.subheader("🚀 도전으로 변화를 만들고  |  📈 성장을 지속하며  |  🎯 교육의 본질을 지향하는 교사")

st.markdown("---")

st.header("👤 기본 정보")
st.markdown("- **이름:** 구정숙")
st.markdown("- **직업:** 25년차 수학교사 / 연구특성화부장")

st.header("🎯 2026년 목표")
st.markdown("일보다 삶을 우선하고, 여유를 선택하며, 나를 아끼는 힘을 기르는 해")


st.header("⭐ 핵심 관심 분야")
st.markdown("""
-  AI·디지털 기반 교육혁신
-  학생 참여형 수업 설계
-  과정 중심 평가 & 수업-평가 일체화
-  기초학력 향상 & 학습격차 해결
-  교사 성장 & 조직 변화
-  교육 정책 ↔ 현장 연결
""")

st.header("🏃‍♂️ Lifestyle")
st.markdown("""
🚴‍♂️ 자전거 라이딩, 🎾 테니스, 🏊‍♂️ 수영을 즐기는 활동적인 라이프스타일
🏋️ 규칙적인 운동, 요즘 헬스 열심히 합니다. 
🥤 건강한 식습관 
💧 좋은 물을 충분히 마시는 생활 습관
🌱 긍정적인 생각과 마음가짐 유지
""")

st.markdown("---")

st.header("연락처")
st.markdown("**📧 scatchi@sen.go.kr**")

st.markdown("---")

st.write("© 2026년 4월 1일 구정숙. All rights reserved.")