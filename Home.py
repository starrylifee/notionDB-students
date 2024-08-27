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

# 도구 링크 및 설명
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <h4>1. 학생용: 이미지 분석 교육 활동 도구</h4>
        <a href="https://students.streamlit.app/vision" target="_blank" style="text-decoration: none;">
            <span style="font-size: 100px;">🖼️</span>
            <div style="text-align: center; font-size: 20px;">클릭하세요</div>
        </a>
        <p>이 도구를 사용하여 이미지를 분석하여 다양한 교육 활동을 수행할 수 있습니다. 활동 코드를 입력하고, 제공된 프롬프트와 이미지를 활용하여 AI와 함께 학습하세요.</p>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <h4>2. 학생용: 인공지능 글자기반 교육 활동 도구</h4>
        <a href="https://students.streamlit.app/text_gen" target="_blank" style="text-decoration: none;">
            <span style="font-size: 100px;">📝</span>
            <div style="text-align: center; font-size: 20px;">클릭하세요</div>
        </a>
        <p>이 도구를 사용하여 다양한 글자기반 교육 활동을 수행할 수 있습니다. 코드를 입력하고, 프롬프트를 가져와 나의 입력을 넣으며 학습 내용을 확장하세요.</p>
        """,
        unsafe_allow_html=True
    )

with col1:
    st.markdown(
        """
        <h4>3. 학생용: 이미지 생성 도구</h4>
        <a href="https://students.streamlit.app/image_gen" target="_blank" style="text-decoration: none;">
            <span style="font-size: 100px;">🖌️</span>
            <div style="text-align: center; font-size: 20px;">클릭하세요</div>
        </a>
        <p>이 도구를 사용하여 교사가 제공한 프롬프트에 따라 이미지를 생성할 수 있습니다. 형용사를 선택하여 이미지의 스타일이나 느낌을 조정하고, 생성된 이미지를 학습에 활용하세요.</p>
        """,
        unsafe_allow_html=True
    )

# 사용자가 각 도구를 더 쉽게 이해하고 접근할 수 있도록 각 도구에 대한 간단한 설명과 그 기능을 소개하는 페이지입니다.
