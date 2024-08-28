import streamlit as st
from openai import OpenAI
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit의 배경색 변경
background_color = "#FFFACD"

# 배경색 변경을 위한 CSS
page_bg_css = f"""
<style>
    .stApp {{
        background-color: {background_color};
    }}
</style>
"""

# Streamlit의 기본 메뉴와 푸터 숨기기
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        var mainMenu = document.getElementById('MainMenu');
        if (mainMenu) {
            mainMenu.style.display = 'none';
        }
        var footer = document.getElementsByTagName('footer')[0];
        if (footer) {
            footer.style.display = 'none';
        }
        var header = document.getElementsByTagName('header')[0];
        if (header) {
            header.style.display = 'none';
        }
    });
    </script>
"""

# Streamlit에서 HTML 및 CSS 적용
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown(page_bg_css, unsafe_allow_html=True)

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=st.secrets["api"]["keys"][0])

# Notion API를 통해 프롬프트와 교사 이메일 가져오기
NOTION_API_URL = "https://api.notion.com/v1/databases/{database_id}/query"
NOTION_API_KEY = st.secrets["notion"]["api_key"]
DATABASE_ID = st.secrets["notion"]["database_id"]
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def fetch_prompt_and_email_from_notion(setting_name):
    query_payload = {
        "filter": {
            "property": "setting_name",
            "rich_text": {
                "equals": setting_name
            }
        }
    }
    response = requests.post(NOTION_API_URL.format(database_id=DATABASE_ID), headers=headers, json=query_payload)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        for result in data["results"]:
            if ("page" in result["properties"]
                and "rich_text" in result["properties"]["page"]
                and len(result["properties"]["page"]["rich_text"]) > 0
                and "text" in result["properties"]["page"]["rich_text"][0]["text"]["content"].lower()):
                
                prompt = result["properties"]["prompt"]["rich_text"][0]["text"]["content"]
                
                # email 필드에서 plain_text 속성을 가져오기
                teacher_email = result["properties"]["email"]["rich_text"][0]["plain_text"]
                
                return prompt, teacher_email
    return None, None

def send_email_to_teacher(student_name, teacher_email, prompt, student_answer, ai_answer):
    if not teacher_email:
        st.warning("교사 이메일이 설정되어 있지 않습니다.")
        return False  # 이메일 전송 실패

    msg = MIMEMultipart()
    msg["From"] = st.secrets["email"]["address"]
    msg["To"] = teacher_email
    msg["Subject"] = f"{student_name} 학생의 AI 생성 활동 결과"

    body = f"""
    학생 이름: {student_name}
    
    사용된 프롬프트:
    {prompt}

    학생의 입력:
    {student_answer}

    AI가 생성한 대화:
    {ai_answer}
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(st.secrets["email"]["address"], st.secrets["email"]["password"])
            server.send_message(msg)
        return True  # 이메일 전송 성공
    except Exception as e:
        st.error(f"이메일 전송에 실패했습니다: {e}")
        return False  # 이메일 전송 실패

# 학생용 UI
st.header('🎓 학생용: 인공지능 대화 생성 도구')

st.markdown("""
    **안내:** 이 도구를 사용하여 AI가 생성한 프롬프트에 따라 다양한 교육 활동을 수행할 수 있습니다.
    1. **학생 이름 입력**: 본인의 이름을 입력하세요.
    2. **코드 입력**: 수업과 관련된 코드를 입력하세요.
    3. **프롬프트 가져오기**: 코드를 입력한 후 '프롬프트 가져오기' 버튼을 클릭하면, 관련된 프롬프트를 불러옵니다.
    4. **활동 입력**: 제공된 프롬프트를 기반으로 자신의 활동을 작성하세요.
    5. **AI 대화 생성**: 작성한 활동을 바탕으로 AI가 관련된 대화를 생성합니다.
    6. **결과 확인**: AI가 생성한 대화를 확인하고 필요시 저장하세요.
""")

# 학생 이름 입력 필드 추가
student_name = st.text_input("🔑 학생 이름 입력", value="", max_chars=50)
if not student_name:
    st.warning("학생 이름을 입력하세요.")

# 코드 입력 필드
setting_name = st.text_input("🔑 활동 코드 입력")

if st.button("📄 프롬프트 가져오기", key="get_prompt"):
    with st.spinner("🔍 프롬프트를 불러오는 중..."):
        prompt, teacher_email = fetch_prompt_and_email_from_notion(setting_name)
        if prompt:
            st.session_state.prompt = prompt
            st.session_state.teacher_email = teacher_email
        else:
            st.error("활동 코드를 다시 확인하세요.")  # 코드 불러오기 실패 시 오류 메시지

if "prompt" in st.session_state and st.session_state.prompt:
    st.success("✅ 프롬프트를 성공적으로 불러왔습니다.")
    st.write("**프롬프트:** " + st.session_state.prompt)

    student_answer = st.text_area("📝 활동 입력", value=st.session_state.get("student_answer", ""))

    if st.button("🤖 AI 대화 생성", key="generate_answer"):
        if student_answer:
            with st.spinner("💬 AI가 대화를 생성하는 중..."):
                st.session_state.student_answer = student_answer
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": st.session_state.prompt},
                        {"role": "user", "content": student_answer}
                    ]
                )

                st.session_state.ai_answer = response.choices[0].message.content.strip()
                st.write("💡 **AI 생성 대화:** " + st.session_state.ai_answer)

                if send_email_to_teacher(student_name, st.session_state.teacher_email, st.session_state.prompt, student_answer, st.session_state.ai_answer):
                    st.success("📧 교사에게 이메일로 결과가 전송되었습니다.")
        else:
            st.error("⚠️ 활동을 입력하세요.")
else:
    st.info("프롬프트를 업로드하세요.")
