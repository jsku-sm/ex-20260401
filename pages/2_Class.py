from html import escape

import streamlit as st


st.set_page_config(
	page_title="공통수학Ⅱ | 학습 자료",
	page_icon="📐",
	layout="wide",
)

st.title("공통수학Ⅱ")
st.caption("단원별 인터랙티브 학습 자료")

resources = [
	("픽토그램", "https://jsku-sm.github.io/pictogram/"),
	("집합 개념 퀴즈", "https://jsku-sm.github.io/math_setQuiz/"),
	("좌표평면", "https://js-math.streamlit.app/?embed=true"),
	("집합의 연산 · 벤다이어그램", "https://jsku-sm.github.io/math_quiz/"),
	("직선의 방정식 · 퀴즈", "https://jsku-sm.github.io/line_mathQuiz/"),
]

rows = "".join(
	"<tr>"
	f'<td class="number">{index:02}</td>'
	f'<td class="topic"><a href="{escape(url, quote=True)}" target="_blank" '
	f'rel="noopener noreferrer">{escape(topic)}</a></td>'
	f'<td class="address"><a href="{escape(url, quote=True)}" target="_blank" '
	f'rel="noopener noreferrer">{escape(url)}</a></td>'
	"</tr>"
	for index, (topic, url) in enumerate(resources, start=1)
)

st.html(f"""
<style>
.resource-table-wrap {{
	overflow-x: auto;
	border: 1px solid #dfe6dd;
	border-radius: 12px;
	background: rgba(255, 255, 255, .88);
}}
.resource-table {{
	width: 100%;
	border-collapse: collapse;
	color: #34453c;
	font-size: .98rem;
}}
.resource-table th, .resource-table td {{
	padding: 1rem 1.2rem;
	border-bottom: 1px solid #e9eee7;
	text-align: left;
	vertical-align: middle;
}}
.resource-table th {{
	background: #edf2eb;
	color: #526358;
	font-size: .82rem;
	font-weight: 700;
}}
.resource-table tr:last-child td {{ border-bottom: 0; }}
.resource-table .number {{ width: 5rem; color: #829384; font-variant-numeric: tabular-nums; }}
.resource-table .topic {{ width: 34%; font-weight: 650; }}
.resource-table a {{ color: #365f49; text-decoration: none; }}
.resource-table a:hover {{ color: #75578d; text-decoration: underline; }}
.resource-table .address {{ overflow-wrap: anywhere; font-size: .9rem; }}
@media (max-width: 640px) {{
	.resource-table th, .resource-table td {{ padding: .8rem .65rem; }}
	.resource-table .number {{ width: 2.5rem; }}
	.resource-table .topic {{ width: 42%; }}
}}
</style>
<div class="resource-table-wrap">
  <table class="resource-table">
	<thead><tr><th>번호</th><th>학습 주제</th><th>웹페이지 주소</th></tr></thead>
	<tbody>{rows}</tbody>
  </table>
</div>
""")
