import streamlit as st

# 페이지 설정 - 아이콘과 제목 설정
st.set_page_config(
    page_title="학생용 교육 도구 홈",  # 브라우저 탭에 표시될 제목
    page_icon="🤖",  # 브라우저 탭에 표시될 아이콘 (이모지 또는 이미지 파일 경로)
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

# 홈 화면 제목
st.title("📚 AI 교육 도구 홈")

# 소개 문구
st.markdown("""
## 🎓 학생용 교육 도구 모음
이 페이지에서는 다양한 AI 기반 교육 도구를 사용할 수 있습니다. 각 도구는 교육 활동을 지원하며, 창의적이고 상호작용적인 학습 경험을 제공합니다.
""")
