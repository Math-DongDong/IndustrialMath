import streamlit as st

# 1. 페이지 레이아웃 설정
st.set_page_config(
    page_title="동동쌤의 수학모음",
    page_icon="./기타/동동이.PNG",
    layout="wide"
)

# 2. 메뉴바 설정(각 페이지의 실제 콘텐츠는 별도의 파일에 존재).
pages = {
    "산업수학": [
        st.Page("./산업수학/MedicalData.py", title="의료 데이터와 건강 상태"),
        st.Page("./산업수학/DistanceOptimization.py", title="원자력 발전소 기중기의 이동 경로 최적화"),
    ],    
}

# 3. 네비게이션 UI 생성(메뉴바 위치)
pg = st.navigation(pages)

# 4. 사용자가 선택한 페이지 실행

pg.run()

