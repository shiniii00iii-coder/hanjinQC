import streamlit as st
import math

# 웹페이지 설정
st.set_page_config(page_title="한진QC 통합 계산기", layout="centered")

st.title("🏭 한진QC 품질관리 시스템")
st.divider()

# 메뉴 선택
menu = st.sidebar.selectbox("기능 선택", ["편평시험 계산", "하중(kN) 역계산"])

if menu == "편평시험 계산":
    st.subheader("🔨 품목별 편평시험 목표치")
    item = st.selectbox("품목 선택", [
        "STG800 (지반보강용)", "SGT275 (일반구조용)", "SGT355 (일반구조용)", 
        "SGT550 (일반구조용)", "SPP (배관용)", "SPPS (압력배관용)", 
        "STKM12B (기계구조용)", "SNT275E (건축구조용)", "SNT355E (건축구조용)"
    ])
    d_val = st.number_input("파이프 외경(D) 입력", min_value=0.0, step=0.1)
    
    if d_val > 0:
        if "지반보강용" in item:
            h = (3/4) * d_val
            ratio = "3/4 D"
        elif item in ["SGT355 (일반구조용)", "SGT550 (일반구조용)", "SNT355E (건축구조용)"]:
            h = (7/8) * d_val
            ratio = "7/8 D"
        else:
            h = (2/3) * d_val
            ratio = "2/3 D"
        
        st.info(f"✅ 목표 높이(H): {h:.2f} mm\n\n✅ 압착량: {d_val - h:.2f} mm ({ratio})")

elif menu == "하중(kN) 역계산":
    st.subheader("⚖️ 강도 기반 하중 예측")
    area = st.number_input("단면적 입력 (mm²)", min_value=0.0, step=0.1)
    col1, col2 = st.columns(2)
    with col1: ts = st.number_input("인장강도 목표 (MPa)", min_value=0.0)
    with col2: ys = st.number_input("항복강도 목표 (MPa)", min_value=0.0)
    
    if area > 0:
        if ts > 0: st.metric("예상 인장하중", f"{(ts * area / 1000):.2f} kN")
        if ys > 0: st.metric("예상 항복하중", f"{(ys * area / 1000):.2f} kN")

st.divider()
st.caption("© 2026 한진QC - 모바일 지원 시스템")