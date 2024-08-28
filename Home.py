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
        <h4>1. 이미지 분석 도구</h4>
        <a href="https://students-ai.streamlit.app/vision(new)" target="_blank" style="text-decoration: none;">
            <span style="font-size: 100px;">🖼️</span>
            <div style="text-align: center; font-size: 20px;">클릭하세요</div>
        </a>
        <p>이 도구를 사용하여 이미지를 분석하고, AI가 제공하는 다양한 인사이트를 학습할 수 있습니다.</p>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <h4>2. 텍스트 생성 도구</h4>
        <a href="https://students-ai.streamlit.app/text_gen(new)" target="_blank" style="text-decoration: none;">
            <span style="font-size: 100px;">📝</span>
            <div style="text-align: center; font-size: 20px;">클릭하세요</div>
        </a>
        <p>이 도구를 사용하여 AI가 생성한 텍스트를 학습 자료로 활용할 수 있습니다. 창의적 글쓰기와 학습에 도움을 줍니다.</p>
        """,
        unsafe_allow_html=True
    )

with col1:
    st.markdown(
        """
        <h4>3. 이미지 생성 도구</h4>
        <a href="https://students-ai.streamlit.app/image_gen(new)" target="_blank" style="text-decoration: none;">
            <span style="font-size: 100px;">🖌️</span>
            <div style="text-align: center; font-size: 20px;">클릭하세요</div>
        </a>
        <p>이 도구를 사용하여 AI가 생성한 이미지를 학습 자료로 사용할 수 있습니다. 창의적인 이미지 만들기에 도전해보세요.</p>
        """,
        unsafe_allow_html=True
    )