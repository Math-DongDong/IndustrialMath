import streamlit as st
import psutil
import os

# -----------------------------------------------------------------------------
# 0. 관리자 인증 (모달창)
# -----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

@st.dialog("🔒 관리자 접속")
def login_modal():
    st.write("서버 모니터링 페이지에 접속하기 위해 비밀번호를 입력해주세요.")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("확인", type="primary", use_container_width=True):
        # secrets.toml 파일에서 비밀번호를 가져옵니다.
        correct_password = st.secrets.get("monitor_password", "")
        
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")

if not st.session_state.authenticated:
    login_modal()
    st.stop()

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------------------------------------------
st.title("📊 서버 리소스 모니터링")
st.markdown("스트림릿 호스팅 환경의 제한된 RAM(메모리) 리소스와 CPU 상태를 실시간으로 확인하고 관리합니다.")

# -----------------------------------------------------------------------------
# 2. 리소스 정리 & 새로고침 컨트롤
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    # 스트림릿은 버튼을 누르면 화면이 새로고침(rerun)되면서 최신 상태를 측정합니다.
    if st.button("🔄 실시간 상태 새로고침", use_container_width=True):
        st.rerun()

with col2:
    # 스트림릿 앱에서 RAM을 가장 많이 잡아먹는 주범인 '캐시'를 비워주는 마법의 버튼입니다.
    if st.button("🧹 메모리 캐시 싹 비우기", type="primary", use_container_width=True):
        st.cache_data.clear()      # 데이터 캐시 삭제
        st.cache_resource.clear()  # 리소스/모델 캐시 삭제
        st.toast("✅ 메모리 캐시가 모두 정리되어 RAM이 확보되었습니다!")

st.write("") # 여백

# -----------------------------------------------------------------------------
# 3. 현재 서버 리소스 계산
# -----------------------------------------------------------------------------
# ① 현재 내 스트림릿 앱(프로세스)이 쓰는 RAM 
pid = os.getpid()
python_process = psutil.Process(pid)
process_memory_mb = python_process.memory_info().rss / (1024 ** 2)

# 사용자 지정 최대 RAM 한도 (예: 2700 MB)
MAX_RAM_MB = 2700.0
# 퍼센트 계산 (100%를 넘지 않도록 안전장치 min 사용)
process_percent = min((process_memory_mb / MAX_RAM_MB) * 100, 100.0)

# ② 서버 전체 시스템 메모리 상황
vm = psutil.virtual_memory()
total_memory_mb = vm.total / (1024 ** 2)
used_memory_mb = vm.used / (1024 ** 2)
memory_percent = vm.percent

# ③ CPU 사용량
cpu_percent = psutil.cpu_percent(interval=0.1)

# -----------------------------------------------------------------------------
# 4. 시각화 대시보드 (Metrics & Progress Bar)
# -----------------------------------------------------------------------------
st.subheader("🖥️ 현재 리소스 사용 현황")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(label="앱(현재 프로세스) RAM 사용량", value=f"{process_memory_mb:.1f} MB")
    # 진행률 바 (0.0 ~ 1.0 사이의 값 필요)
    st.progress(process_percent / 100.0, text=f"할당량({int(MAX_RAM_MB)}MB) 대비 {process_percent:.1f}% 사용 중")

with c2:
    st.metric(label="시스템 전체 RAM 사용량", value=f"{used_memory_mb:.1f} MB")
    st.progress(memory_percent / 100.0, text=f"전체 시스템 메모리({total_memory_mb:.0f} MB) 대비 {memory_percent:.1f}% 사용 중")

with c3:
    st.metric(label="서버 CPU 사용량", value=f"{cpu_percent:.1f} %")
    st.progress(cpu_percent / 100.0, text="현재 CPU 부하량")

st.divider()

# 안내 문구
st.info("""
💡 **리소스 관리 Tip:**
*   **앱 RAM 사용량:** 현재 선생님의 웹 서버가 차지하고 있는 메모리입니다. 이 값이 2,500MB에 가까워지면 앱이 튕길(강제 종료) 수 있습니다.
*   데이터셋이나 이미지를 많이 불러올 경우 RAM이 급격히 상승합니다. 사용량이 너무 높을 때는 위쪽의 **'메모리 캐시 싹 비우기'** 버튼을 눌러주세요!
""")