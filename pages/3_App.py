from contextlib import contextmanager
from datetime import date, timedelta
import csv
import hashlib
import hmac
import io
import os
from pathlib import Path
import secrets
import sqlite3
from typing import Iterator

import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = Path(os.environ.get("SUDANOTE_DB_PATH", DATA_DIR / "sudanoat.sqlite3"))
PIN_ITERATIONS = 310_000

QUESTIONS = [
	"오늘 배운 내용 중 가장 중요하다고 생각한 개념은 무엇인가요?",
	"오늘 문제나 활동에서 내가 사용한 수학적 생각이나 방법을 설명해 주세요.",
	"처음에는 잘못 생각했거나 어려웠지만, 수업 중 새롭게 알게 된 것은 무엇인가요?",
	"오늘 내가 잘했다고 생각하는 행동이나 학습 태도는 무엇인가요?",
	"다음 시간에 더 알아보고 싶거나 다시 확인하고 싶은 것은 무엇인가요?",
]

QUESTION_LABELS = [
	"중요하게 생각한 개념",
	"사용한 수학적 생각이나 방법",
	"새롭게 알게 된 점",
	"잘한 행동이나 학습 태도",
	"다음 시간에 더 알고 싶은 점",
]

st.set_page_config(page_title="수다노트 | 수학 수업 성찰", page_icon="📝", layout="wide")

st.html("""
<style>
.stApp {
	background: linear-gradient(145deg, #f5f8f2 0%, #fbfaf6 58%, #f3f6f5 100%);
	color: #273a31;
}
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1080px; padding-top: 2.2rem; padding-bottom: 2.5rem; }
h1, h2, h3 { color: #293f34; }
[data-testid="stForm"] {
	background: rgba(255, 255, 255, .72);
	border: 1px solid #e1e8df;
	border-radius: 12px;
	padding: 1.2rem;
}
[data-testid="stMetric"] {
	background: rgba(255, 255, 255, .82);
	border: 1px solid #e1e8df;
	border-radius: 8px;
	padding: .85rem 1rem;
}
@media (max-width: 700px) {
	.block-container { padding: 1.2rem .8rem 2rem; }
	[data-testid="stForm"] { padding: .8rem; }
}
</style>
""")


@contextmanager
def database() -> Iterator[sqlite3.Connection]:
	DATA_DIR.mkdir(parents=True, exist_ok=True)
	connection = sqlite3.connect(DATABASE_PATH, timeout=10)
	connection.row_factory = sqlite3.Row
	connection.execute("PRAGMA foreign_keys = ON")
	try:
		yield connection
		connection.commit()
	finally:
		connection.close()


def initialize_database() -> None:
	with database() as connection:
		connection.executescript("""
			CREATE TABLE IF NOT EXISTS students (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				class_name TEXT COLLATE NOCASE NOT NULL,
				student_name TEXT COLLATE NOCASE NOT NULL,
				pin_salt TEXT NOT NULL,
				pin_hash TEXT NOT NULL,
				created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
				UNIQUE (class_name, student_name)
			);
			CREATE TABLE IF NOT EXISTS reflections (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
				lesson_date TEXT NOT NULL,
				lesson_title TEXT NOT NULL,
				answer_1 TEXT NOT NULL DEFAULT '',
				answer_2 TEXT NOT NULL DEFAULT '',
				answer_3 TEXT NOT NULL DEFAULT '',
				answer_4 TEXT NOT NULL DEFAULT '',
				answer_5 TEXT NOT NULL DEFAULT '',
				created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
			);
			CREATE INDEX IF NOT EXISTS reflections_student_date
			ON reflections(student_id, lesson_date DESC);
		""")


def hash_pin(pin: str, salt: bytes) -> bytes:
	return hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), salt, PIN_ITERATIONS)


def register_student(class_name: str, student_name: str, pin: str) -> int | None:
	salt = secrets.token_bytes(16)
	try:
		with database() as connection:
			cursor = connection.execute(
				"INSERT INTO students (class_name, student_name, pin_salt, pin_hash) "
				"VALUES (?, ?, ?, ?)",
				(class_name, student_name, salt.hex(), hash_pin(pin, salt).hex()),
			)
			return int(cursor.lastrowid)
	except sqlite3.IntegrityError:
		return None


def authenticate_student(class_name: str, student_name: str, pin: str) -> sqlite3.Row | None:
	with database() as connection:
		student = connection.execute(
			"SELECT * FROM students WHERE class_name = ? AND student_name = ?",
			(class_name, student_name),
		).fetchone()
	if student is None:
		return None
	expected = bytes.fromhex(student["pin_hash"])
	actual = hash_pin(pin, bytes.fromhex(student["pin_salt"]))
	return student if hmac.compare_digest(actual, expected) else None


def save_reflection(
	student_id: int,
	lesson_date: date,
	lesson_title: str,
	answers: list[str],
) -> None:
	with database() as connection:
		connection.execute(
			"""INSERT INTO reflections (
				student_id, lesson_date, lesson_title,
				answer_1, answer_2, answer_3, answer_4, answer_5
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
			(student_id, lesson_date.isoformat(), lesson_title, *answers),
		)


def get_student_reflections(student_id: int, lesson_date: str | None = None) -> list[sqlite3.Row]:
	query = "SELECT * FROM reflections WHERE student_id = ?"
	parameters: list[object] = [student_id]
	if lesson_date:
		query += " AND lesson_date = ?"
		parameters.append(lesson_date)
	query += " ORDER BY lesson_date DESC, created_at DESC, id DESC"
	with database() as connection:
		return list(connection.execute(query, parameters).fetchall())


def get_classes() -> list[str]:
	with database() as connection:
		rows = connection.execute(
			"SELECT DISTINCT class_name FROM students ORDER BY class_name COLLATE NOCASE"
		).fetchall()
	return [row["class_name"] for row in rows]


def get_students(class_name: str) -> list[sqlite3.Row]:
	with database() as connection:
		return list(connection.execute(
			"SELECT id, class_name, student_name FROM students "
			"WHERE class_name = ? ORDER BY student_name COLLATE NOCASE",
			(class_name,),
		).fetchall())


def get_class_reflections(
	class_name: str,
	student_name: str | None = None,
	days: int | None = None,
) -> list[sqlite3.Row]:
	query = """SELECT r.*, s.class_name, s.student_name
		FROM reflections AS r
		JOIN students AS s ON s.id = r.student_id
		WHERE s.class_name = ?"""
	parameters: list[object] = [class_name]
	if student_name:
		query += " AND s.student_name = ?"
		parameters.append(student_name)
	if days:
		cutoff = (date.today() - timedelta(days=days)).isoformat()
		query += " AND r.lesson_date >= ?"
		parameters.append(cutoff)
	query += " ORDER BY r.lesson_date DESC, r.created_at DESC, r.id DESC"
	with database() as connection:
		return list(connection.execute(query, parameters).fetchall())


def configured_teacher_password() -> str:
	password = os.environ.get("TEACHER_PASSWORD", "")
	if password:
		return password
	try:
		return str(st.secrets.get("TEACHER_PASSWORD", ""))
	except Exception:
		return ""


def show_student_login() -> None:
	login_tab, signup_tab = st.tabs(["학생 로그인", "처음 이용하기"])

	with login_tab:
		with st.form("student_login"):
			class_name = st.text_input("반", placeholder="예: 1학년 3반", max_chars=40)
			student_name = st.text_input("이름", max_chars=40)
			pin = st.text_input("개인 PIN", type="password", max_chars=32)
			submitted = st.form_submit_button("내 기록 열기", type="primary", width="stretch")
		if submitted:
			student = authenticate_student(class_name.strip(), student_name.strip(), pin)
			if student:
				st.session_state.student_id = int(student["id"])
				st.session_state.student_class = student["class_name"]
				st.session_state.student_name = student["student_name"]
				st.rerun()
			st.error("반, 이름 또는 PIN을 확인해 주세요.")

	with signup_tab:
		st.caption("처음 한 번 계정을 만들면, 같은 반·이름·PIN으로 다음에도 기록을 이어갈 수 있어요.")
		with st.form("student_signup"):
			class_name = st.text_input("반 이름", placeholder="예: 1학년 3반", max_chars=40)
			student_name = st.text_input("학생 이름", max_chars=40)
			pin = st.text_input("개인 PIN 만들기 (숫자 4자리 이상)", type="password", max_chars=32)
			pin_confirm = st.text_input("PIN 확인", type="password", max_chars=32)
			submitted = st.form_submit_button("계정 만들기", type="primary", width="stretch")
		if submitted:
			class_name = class_name.strip()
			student_name = student_name.strip()
			if not class_name or not student_name:
				st.error("반과 이름을 입력해 주세요.")
			elif not pin.isdigit() or len(pin) < 4:
				st.error("PIN은 숫자 4자리 이상으로 설정해 주세요.")
			elif pin != pin_confirm:
				st.error("PIN 확인이 일치하지 않습니다.")
			else:
				student_id = register_student(class_name, student_name, pin)
				if student_id is None:
					st.error("이미 등록된 반과 이름입니다. 로그인하거나 선생님께 문의해 주세요.")
				else:
					st.session_state.student_id = student_id
					st.session_state.student_class = class_name
					st.session_state.student_name = student_name
					st.session_state.student_flash = "계정이 만들어졌어요. 오늘의 배움을 기록해 보세요."
					st.rerun()


def show_student_workspace() -> None:
	student_id = int(st.session_state.student_id)
	st.caption(f"{st.session_state.student_class} · {st.session_state.student_name}")
	if st.button("로그아웃", key="student_logout"):
		for key in ("student_id", "student_class", "student_name"):
			st.session_state.pop(key, None)
		st.rerun()

	flash = st.session_state.pop("student_flash", None)
	if flash:
		st.success(flash)

	write_tab, history_tab = st.tabs(["오늘 기록하기", "내 기록 보기"])
	with write_tab:
		st.subheader("오늘의 수다노트")
		st.caption("정답은 없어요. 오늘의 생각을 내 말로 편하게 남겨 보세요.")
		with st.form("reflection_form"):
			lesson_date = st.date_input("수업 날짜", value=date.today())
			lesson_title = st.text_input(
				"오늘의 수업 또는 차시",
				placeholder="예: 3차시 · 집합의 연산",
				max_chars=80,
			)
			answers = [
				st.text_area(question, max_chars=2000, height=100, key=f"reflection_answer_{index}")
				for index, question in enumerate(QUESTIONS, start=1)
			]
			submitted = st.form_submit_button("수다노트 저장", type="primary", width="stretch")
		if submitted:
			if not lesson_title.strip():
				st.error("수업 또는 차시를 입력해 주세요.")
			elif not any(answer.strip() for answer in answers):
				st.error("질문 중 하나 이상에 답을 적어 주세요.")
			else:
				save_reflection(student_id, lesson_date, lesson_title.strip(), answers)
				st.session_state.student_flash = "기록을 저장했어요. 오늘의 생각을 잘 간직해 둘게요."
				st.rerun()

	with history_tab:
		st.subheader("날짜별 내 기록")
		records = get_student_reflections(student_id)
		if not records:
			st.info("아직 저장한 기록이 없어요. 첫 수다노트를 남겨 보세요.")
		else:
			available_dates = list(dict.fromkeys(record["lesson_date"] for record in records))
			selected_date = st.selectbox("확인할 날짜", available_dates, key="student_history_date")
			selected_records = [record for record in records if record["lesson_date"] == selected_date]
			for record in selected_records:
				with st.expander(f"{record['lesson_date']} · {record['lesson_title']}", expanded=True):
					for index, question in enumerate(QUESTIONS, start=1):
						answer = record[f"answer_{index}"]
						st.markdown(f"**{question}**")
						st.write(answer if answer else "_(작성하지 않음)_")


def record_answers(record: sqlite3.Row) -> list[str]:
	return [record[f"answer_{index}"] for index in range(1, 6)]


def show_record(record: sqlite3.Row, include_class: bool = False) -> None:
	parts = [record["lesson_date"]]
	if include_class:
		parts.append(f"{record['class_name']} {record['student_name']}")
	else:
		parts.append(record["student_name"])
	parts.append(record["lesson_title"])
	with st.expander(" · ".join(parts)):
		for question, answer in zip(QUESTIONS, record_answers(record)):
			if answer.strip():
				st.markdown(f"**{question}**")
				st.write(answer)


def make_school_record_draft(student_name: str, records: list[sqlite3.Row]) -> str:
	statements: list[str] = []
	templates = [
		"중요 개념으로 ‘{answer}’을(를) 제시함.",
		"문제 해결에 활용한 수학적 생각과 방법을 ‘{answer}’이라고 설명함.",
		"수업 중 새롭게 알게 된 점으로 ‘{answer}’을(를) 기록함.",
		"자신의 학습 태도에서 잘한 점으로 ‘{answer}’을(를) 꼽음.",
		"다음 시간에 더 알아보고 싶은 내용으로 ‘{answer}’을(를) 제시함.",
	]
	for record in reversed(records[:20]):
		reflections = [
			template.format(answer=answer.strip())
			for template, answer in zip(templates, record_answers(record))
			if answer.strip()
		]
		if reflections:
			statements.append(
				f"{record['lesson_date']} {record['lesson_title']} 수업 성찰에서 "
				+ " ".join(reflections)
			)
	if not statements:
		return "선택한 기간에 작성된 성찰 응답이 없습니다."
	return (
		f"{student_name} 학생은 수업 후 작성한 수다노트에서 다음과 같이 배움과 성찰을 기록함.\n\n"
		+ "\n\n".join(statements)
	)


def show_teacher_login() -> bool:
	if st.session_state.get("teacher_authenticated"):
		if st.button("교사 로그아웃", key="teacher_logout"):
			st.session_state.pop("teacher_authenticated", None)
			st.rerun()
		return True

	configured_password = configured_teacher_password()
	if not configured_password:
		st.warning("교사 화면은 잠겨 있습니다. 먼저 교사 비밀번호를 비밀 설정에 등록해 주세요.")
		st.markdown("프로젝트의 `.streamlit/secrets.toml`에 다음 항목을 추가하거나 `TEACHER_PASSWORD` 환경 변수를 설정하세요.")
		st.code('TEACHER_PASSWORD = "충분히 길고 추측하기 어려운 비밀번호"', language="toml")
		return False

	with st.form("teacher_login"):
		password = st.text_input("교사 비밀번호", type="password")
		submitted = st.form_submit_button("교사 인증", type="primary", width="stretch")
	if submitted:
		if hmac.compare_digest(password, configured_password):
			st.session_state.teacher_authenticated = True
			st.rerun()
		st.error("비밀번호가 올바르지 않습니다.")
	return False


def show_teacher_workspace() -> None:
	classes = get_classes()
	st.subheader("교사용 기록 검토")
	if not classes:
		st.info("아직 등록된 학생이 없습니다. 학생이 계정을 만든 뒤 기록을 남기면 여기에서 확인할 수 있습니다.")
		return

	class_name = st.selectbox("반 선택", classes, key="teacher_class_filter")
	students = get_students(class_name)
	student_names = [student["student_name"] for student in students]
	selected_student = st.selectbox(
		"학생 선택",
		["전체 학생", *student_names],
		key="teacher_student_filter",
	)
	student_filter = None if selected_student == "전체 학생" else selected_student
	st.caption("학생 선택을 ‘전체 학생’으로 두면 해당 반의 기록을 모두 확인합니다.")

	student_tab, question_tab, school_record_tab = st.tabs([
		"학생별 기록", "문항별 모아보기", "교과세특 초안",
	])

	with student_tab:
		records = get_class_reflections(class_name, student_filter)
		st.metric("확인 가능한 기록", f"{len(records)}건")
		if records:
			csv_buffer = io.StringIO()
			writer = csv.writer(csv_buffer)
			writer.writerow(["반", "학생", "수업 날짜", "수업/차시", *QUESTION_LABELS])
			for record in records:
				writer.writerow([
					record["class_name"], record["student_name"], record["lesson_date"],
					record["lesson_title"], *record_answers(record),
				])
			st.download_button(
				"현재 기록 CSV 다운로드",
				data=csv_buffer.getvalue().encode("utf-8-sig"),
				file_name=f"{class_name}_수다노트.csv",
				mime="text/csv",
			)
			for record in records:
				show_record(record, include_class=True)
		else:
			st.info("선택한 조건에 해당하는 기록이 없습니다.")

	with question_tab:
		question_index = st.selectbox(
			"모아 볼 문항",
			range(len(QUESTIONS)),
			format_func=lambda index: f"{index + 1}. {QUESTION_LABELS[index]}",
			key="teacher_question_filter",
		)
		records = get_class_reflections(class_name, student_filter)
		responses = [record for record in records if record[f"answer_{question_index + 1}"].strip()]
		st.caption(f"응답 {len(responses)}건 · {class_name}")
		if responses:
			for record in responses:
				with st.expander(
					f"{record['lesson_date']} · {record['student_name']} · {record['lesson_title']}"
				):
					st.write(record[f"answer_{question_index + 1}"])
		else:
			st.info("선택한 문항에 작성된 응답이 없습니다.")

	with school_record_tab:
		if not student_filter:
			st.info("세특 초안을 만들 학생 한 명을 먼저 선택해 주세요.")
		else:
			period_label = st.selectbox(
				"반영할 기록 기간",
				["전체 기록", "최근 30일", "최근 90일"],
				key="school_record_period",
			)
			period_days = {"전체 기록": None, "최근 30일": 30, "최근 90일": 90}[period_label]
			student_records = get_class_reflections(class_name, student_filter, period_days)
			st.caption(f"초안 근거 기록 {len(student_records)}건 · 최대 최근 20건 반영")
			if not student_records:
				st.info("선택한 기간에 작성된 기록이 없습니다.")
			else:
				if st.button("기록을 바탕으로 세특 초안 만들기", type="primary"):
					st.session_state.school_record_draft = make_school_record_draft(
						student_filter, student_records
					)
				st.text_area(
					"교과세특 초안 · 사실관계를 확인하고 교사가 다듬어 사용하세요",
					key="school_record_draft",
					height=280,
					help="학생의 자기 성찰 응답을 문장으로 정리한 초안입니다. 교사의 관찰과 평가를 반영해 수정하세요.",
				)
				draft = st.session_state.get("school_record_draft", "")
				if draft:
					st.download_button(
						"초안 텍스트 다운로드",
						data=draft,
						file_name=f"{student_filter}_교과세특_초안.txt",
						mime="text/plain",
					)
				st.caption("이 초안은 학생의 자기 성찰 내용을 정리한 것으로, 교사의 직접 관찰을 대신하지 않습니다.")


initialize_database()
st.title("수다노트")
st.caption("수학 수업에서 배운 것과 생각한 것을 차곡차곡 기록해요.")

mode = st.radio("이용 화면", ["학생", "교사"], horizontal=True, label_visibility="collapsed")
if mode == "학생":
	st.info("나만의 PIN으로 로그인하면 내가 쓴 기록만 볼 수 있어요. PIN은 다른 사람에게 알려 주지 마세요.")
	if st.session_state.get("student_id"):
		show_student_workspace()
	else:
		show_student_login()
else:
	st.warning("교사용 화면에는 학생의 성찰 기록이 표시됩니다. 교사 계정으로만 접근하세요.")
	if show_teacher_login():
		show_teacher_workspace()
