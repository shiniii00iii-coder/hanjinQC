import streamlit as st
import math

# 웹페이지 설정
st.set_page_config(page_title="한진 품질관리 시스템", layout="centered")

st.title("🏭 파이프 품질관리 통합 시스템")
st.divider()

# 왼쪽 사이드바에서 메뉴 선택
menu = st.sidebar.selectbox("기능 선택", ["편평시험(Flattening) 계산", "단면적/인장강도 계산"])

# --- 1. 편평시험(Flattening) 계산 기능 ---
if menu == "편평시험(Flattening) 계산":
    st.subheader("🔨 품목별 편평시험 목표치 계산")
    st.write("품목을 선택하고 외경(D)을 입력하면 목표 결과와 눌러야 할 양을 계산합니다.")
    
    # 품목 선택 리스트 (STG800 추가)
    item = st.selectbox("품목(강종) 선택", [
        "SGT275 (일반구조용)",
        "SGT355 (일반구조용)",
        "SGT550 (일반구조용)",
        "STG800 (지반보강용)",  # 신규 추가
        "SPP (배관용)",
        "SPPS (압력배관용)",
        "STKM12B (기계구조용)",
        "SNT275E (건축구조용)",
        "SNT355E (건축구조용)"
    ])
    
    st.divider()
    
    d_val = st.number_input("파이프 외경 입력 (D, mm)", min_value=0.0, step=0.1, format="%.2f")
    
    if d_val > 0:
        # 1. 3/4D 그룹 (신규 STG800)
        if item == "STG800 (지반보강용)":
            ratio_str = "3/4 D"
            h_val = (3/4) * d_val
        # 2. 7/8D 그룹
        elif item in ["SGT355 (일반구조용)", "SGT550 (일반구조용)", "SNT355E (건축구조용)"]:
            ratio_str = "7/8 D"
            h_val = (7/8) * d_val
        # 3. 2/3D 그룹 (기본값)
        else:
            ratio_str = "2/3 D"
            h_val = (2/3) * d_val
            
        # 눌러야 할 양 계산 (외경 - 목표높이)
        press_val = d_val - h_val
            
        st.divider()
        st.subheader("📊 시험 결과")
        
        # 강조 표시
        st.info(f"**시험 결과 목표높이: {h_val:.2f}mm ({press_val:.2f}mm 누를 것)**")
        
        col1, col2 = st.columns(2)
        col1.metric(label="최종 목표 높이 (H)", value=f"{h_val:.2f} mm")
        col2.metric(label="압착 필요량 (Press)", value=f"{press_val:.2f} mm", delta=f"-{press_val:.2f} mm", delta_color="inverse")
        
        st.warning(f"💡 {item} 규격은 외경의 {ratio_str}까지 압착해야 합니다.")
        
        with st.expander("📝 계산 상세 정보"):
            st.write(f"- 입력 외경(D): {d_val} mm")
            st.write(f"- 적용 비율: {ratio_str}")
            st.write(f"- 상세 계산: {d_val} × {ratio_str} = {h_val:.4f}")
    else:
        st.info("외경(D)을 입력해 주세요.")

# --- 2. 단면적 및 인장강도 계산 기능 ---
elif menu == "단면적/인장강도 계산":
    st.subheader("📏 단면적 및 인장강도 계산")
    col1, col2 = st.columns(2)
    with col1:
        od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1, key="od_main")
    with col2:
        wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1, key="wt_main")
    
    if od > 2*wt and wt > 0:
        area = (math.pi * (od**2 - (od - 2*wt)**2)) / 4
        st.success(f"✅ 계산된 단면적: {area:.2f} mm²")
        
        st.divider()
        max_load = st.number_input("시험 최대 하중 (kN)", min_value=0.0, step=0.1)
        if max_load > 0:
            ts = (max_load * 1000) / area
            st.metric("인장강도 (UTS)", f"{ts:.2f} MPa")
    else:
        st.info("파이프의 외경과 두께를 입력해 주세요.")

st.divider()
st.caption("© 2026 한진QC - 업무지원 시스템 (V1.3)")
