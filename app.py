import streamlit as st
import random

# 페이지 설정 (터미널 느낌을 내기 위해 어두운 테마 사용 권장)
st.set_page_config(page_title="서버 해킹 시뮬레이션", page_icon="💻", layout="centered")

st.title("💻 시스템 메인프레임 해킹")
st.write("보안 시스템이 작동 중입니다. **중복되지 않는 4자리 비밀번호**를 해독하여 서버에 침투하세요.")
st.write("- **Strike (자리 일치):** 숫자와 자리가 모두 맞음")
st.write("- **Ball (숫자 포함):** 숫자는 맞지만 자리가 틀림")

# 세션 상태 초기화 (게임 데이터 저장)
if 'password' not in st.session_state:
    # 중복 없는 4자리 난수 생성
    numbers = list(range(10))
    random.shuffle(numbers)
    st.session_state.password = ''.join(map(str, numbers[:4]))
    st.session_state.attempts = 10
    st.session_state.logs = []
    st.session_state.is_hacked = False
    st.session_state.is_locked = False

# 게임 리셋 함수
def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# 1. 해킹 성공 시 화면
if st.session_state.is_hacked:
    st.success("ACCESS GRANTED: 보안 시스템을 무력화했습니다! 서버 데이터에 접근합니다...")
    st.balloons()
    if st.button("시스템 로그아웃 (게임 다시 시작)"):
        reset_game()
        st.rerun()

# 2. 해킹 실패 시 화면 (시도 횟수 초과)
elif st.session_state.is_locked:
    st.error(f"SYSTEM LOCKED: 접근 횟수를 초과하여 시스템이 잠겼습니다. (정답: {st.session_state.password})")
    if st.button("우회 접속 시도 (게임 다시 시작)"):
        reset_game()
        st.rerun()

# 3. 게임 진행 화면
else:
    st.info(f"남은 해킹 시도 횟수: **{st.session_state.attempts}**")
    
    # 사용자 입력
    guess = st.text_input("4자리 숫자를 입력하고 Enter를 누르세요:", max_chars=4)
    
    if st.button("코드 인젝션 (입력)"):
        if len(guess) != 4 or not guess.isdigit():
            st.warning("오류: 4자리 숫자로만 입력해야 합니다.")
        elif len(set(guess)) != 4:
            st.warning("오류: 각 자릿수는 중복되지 않는 숫자여야 합니다.")
        else:
            # 횟수 차감
            st.session_state.attempts -= 1
            
            strike = 0
            ball = 0
            
            # Strike / Ball 판별 로직
            for i in range(4):
                if guess[i] == st.session_state.password[i]:
                    strike += 1
                elif guess[i] in st.session_state.password:
                    ball += 1
            
            # 로그 기록
            log_entry = f"입력: {guess} ➔ [ 분석 결과 ] {strike} Strike, {ball} Ball"
            st.session_state.logs.append(log_entry)
            
            # 종료 조건 확인
            if strike == 4:
                st.session_state.is_hacked = True
            elif st.session_state.attempts <= 0:
                st.session_state.is_locked = True
            
            # 화면 갱신
            st.rerun()
            
    # 해킹 로그 출력
    st.markdown("### 📜 터미널 로그")
    for log in reversed(st.session_state.logs):
        st.code(log, language="bash")
