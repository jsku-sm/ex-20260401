import streamlit as st

st.set_page_config(page_title="Streamlit 구성 요소 데모", page_icon="🎉", layout="wide")

st.title("🎈 Streamlit 구성 요소 예제 페이지")
st.write("이 페이지는 Streamlit에서 자주 사용하는 UI 요소들을 보여주는 간단한 데모입니다.")

st.header("1. 텍스트 & 마크다운")
st.markdown("**markdown**과 `code`를 포함할 수 있습니다.")
st.caption("st.caption: 작은 보조 텍스트")
st.subheader("st.subheader: 소제목 테스트")

st.header("2. 입력 위젯")
name = st.text_input("이름", "홍길동")
age = st.number_input("나이", min_value=0, max_value=120, value=25)
option = st.selectbox("좋아하는 과일", ["사과", "바나나", "포도", "오렌지"])
check = st.checkbox("알림 받기")
radio = st.radio("성별", ["남", "여", "선택 안함"])
st.write("입력 결과:", name, age, option, check, radio)

st.header("3. 버튼과 상태")
if st.button("클릭하시오"):
    st.success("버튼 클릭되었습니다!")

agree = st.checkbox("약관에 동의합니다")
if agree:
    st.info("동의하셔서 다음 단계로 진행할 수 있습니다.")

st.header("4. 레이아웃: 컬럼, 컨테이너")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("CPU", "78%", "-2%")
with col2:
    st.metric("메모리", "62%", "+1%")
with col3:
    st.metric("디스크", "54%", "+0.5%")

with st.expander("추가 정보 보기"):
    st.write("여기에 더 많은 설정/도움말을 넣을 수 있습니다.")

st.header("5. 데이터 표시")
import pandas as pd

df = pd.DataFrame({
    "이름": ["철수", "영희", "민수"],
    "점수": [85, 92, 78],
    "통과": [True, True, False],
})

st.dataframe(df)
st.table(df)

st.header("6. 미디어")
st.image("https://docs.streamlit.io/1.0.0/_static/streamlit-logo-secondary-colormark-darktext.svg", width=150)
st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/StarWars3.wav")

st.header("7. 키보드 단축키와 코드")
code = '''
import streamlit as st
st.write("Hello Streamlit")
'''
st.code(code, language="python")

st.write("---")
st.write("완료: 이제 이 페이지에서 다양한 Streamlit 요소를 테스트할 수 있습니다.")
