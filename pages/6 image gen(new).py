import streamlit as st
from openai import OpenAI
import requests
import pathlib
import toml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 페이지 설정 - 아이콘과 제목 설정
st.set_page_config(
    page_title="학생용 교육 도구 홈",
    page_icon="🤖",
)

# Streamlit의 기본 메뉴와 푸터 숨기기
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=secrets["api"]["keys"][0])  # 첫 번째 API 키 사용

# Notion API 설정
NOTION_API_KEY = secrets["notion"]["api_key"]
NOTION_DATABASE_ID = secrets["notion"]["database_id"]

# Notion에서 프롬프트와 교사 이메일 가져오기
def get_prompt_and_teacher_email_from_notion(setting_name):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "filter": {
            "property": "setting_name",
            "rich_text": {
                "equals": setting_name
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            for result in results:
                page_text = result["properties"]["page"]["rich_text"][0]["text"]["content"]
                if "image" in page_text:
                    prompt = result["properties"]["prompt"]["rich_text"][0]["text"]["content"]
                    teacher_email = result["properties"]["email"]["rich_text"][0]["plain_text"]
                    return prompt, teacher_email
    return None, None

# 이메일 전송 기능
def send_email_to_teacher(student_name, teacher_email, prompt, adjectives, image_url):
    msg = MIMEMultipart()
    msg["From"] = secrets["email"]["address"]
    msg["To"] = teacher_email
    msg["Subject"] = f"{student_name} 학생의 이미지 생성 결과"

    body = f"""
    학생 이름: {student_name}
    주제: {prompt}
    형용사: {adjectives}

    생성된 이미지 URL:
    {image_url}
    """
    msg.attach(MIMEText(body, "plain"))

    # 이메일 전송
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(secrets["email"]["address"], secrets["email"]["password"])
            server.send_message(msg)
        return True  # 이메일 전송 성공 시 True 반환
    except Exception as e:
        st.error(f"이메일 전송에 실패했습니다: {e}")
        return False  # 이메일 전송 실패 시 False 반환

# 학생용 UI
st.header('🎨 학생용: 이미지 생성 도구')

# 사용 설명 추가
st.markdown("""
    **안내:** 이 도구를 사용하여 교사가 제공한 프롬프트에 따라 이미지를 생성할 수 있습니다.
    1. **학생 이름 입력**: 본인의 이름을 입력하세요.
    2. **코드 입력**: 수업과 관련된 코드를 입력하세요.
    3. **프롬프트 가져오기**: 코드를 입력한 후 '프롬프트 가져오기' 버튼을 클릭하면, 교사가 설정한 프롬프트를 불러옵니다.
    4. **형용사 선택**: 이미지의 스타일이나 느낌을 나타내는 형용사를 선택하세요.
    5. **이미지 생성**: 교사 프롬프트와 선택한 형용사를 바탕으로 이미지를 생성합니다.
    6. **결과 확인**: 생성된 이미지를 확인하고 필요시 다운로드하세요.
""")

# 학생 이름 입력 필드
student_name = st.text_input("🔑 학생 이름 입력", value="", max_chars=50)
if not student_name:
    st.warning("학생 이름을 입력하세요.")

# 코드 입력 필드
setting_name = st.text_input("🔑 코드 입력")

if st.button("📄 프롬프트 가져오기", key="get_prompt"):
    with st.spinner("🔍 프롬프트를 불러오는 중..."):
        prompt, teacher_email = get_prompt_and_teacher_email_from_notion(setting_name)
        if prompt and teacher_email:
            st.session_state.prompt = prompt
            st.session_state.teacher_email = teacher_email
            st.success("✅ 프롬프트를 성공적으로 불러왔습니다.")
        else:
            st.error("⚠️ 해당 코드에 대한 프롬프트를 찾을 수 없습니다.")

if "prompt" in st.session_state and st.session_state.prompt:
    st.write("**프롬프트:** " + st.session_state.prompt)

    # 사전 정의된 형용사 옵션 제공
    with st.expander("형용사 선택"):

        col1, col2 = st.columns(2)

        with col1:
            selected_color = st.radio("🎨 색감 선택", ["선택하지 않음"] + [
                "밝은", "어두운", "선명한", "부드러운", "따뜻한", 
                "차가운", "다채로운", "흑백의", "파스텔톤의", "무채색의"
            ])
            selected_mood = st.radio("🌅 분위기 선택", ["선택하지 않음"] + [
                "몽환적인", "현실적인", "우아한", "고요한", "활기찬", 
                "긴장감 있는", "로맨틱한", "공포스러운", "신비로운", "평화로운"
            ])

        with col2:
            selected_style = st.radio("🖌️ 스타일 선택", ["선택하지 않음"] + [
                "미니멀한", "복잡한", "빈티지한", "모던한", "고전적인", 
                "미래적인", "자연주의적인", "기하학적인", "추상적인", "대담한"
            ])
            selected_texture = st.radio("🧶 텍스처 선택", ["선택하지 않음"] + [
                "매끄러운", "거친", "부드러운", "뾰족한", "질감이 느껴지는", 
                "광택 있는", "매트한", "무광의", "플러시한"
            ])
            selected_emotion = st.radio("😊 감정 표현 선택", ["선택하지 않음"] + [
                "즐거운", "슬픈", "분노한", "평온한", "감동적인", 
                "따뜻한", "외로운", "흥미로운", "짜릿한", "사려 깊은"
            ])

    # 선택된 "선택하지 않음"을 제외한 형용사 결합
    combined_concept = " ".join([option for option in [selected_color, selected_mood, selected_style, selected_texture, selected_emotion] if option != "선택하지 않음"])

    if st.button("🖼️ 이미지 생성", key="generate_image"):
        if combined_concept:
            with st.spinner("🖼️ 이미지를 생성하는 중..."):
                combined_prompt = f"{st.session_state.prompt} {combined_concept}"
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=combined_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                image_url = response.data[0].url
                st.session_state.image_url = image_url
                st.image(image_url, caption="Generated Image", use_column_width=True)
                st.success("✅ 이미지가 성공적으로 생성되었습니다!")
                st.download_button(label="💾 이미지 다운로드", data=image_url, file_name="generated_image.png")

                # 이메일로 결과 전송
                if send_email_to_teacher(student_name, st.session_state.teacher_email, st.session_state.prompt, combined_concept, image_url):
                    st.success("📧 교사에게 이메일로 결과가 전송되었습니다.")
        else:
            st.error("⚠️ 최소한 하나의 형용사를 선택하세요.")
else:
    st.info("프롬프트를 업로드하세요.")
