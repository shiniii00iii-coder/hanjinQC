import streamlit as st
import math

# 웹페이지 설정
st.set_page_config(page_title="한진 품질관리 시스템", layout="centered")

st.title("🏭 파이프 품질관리 통합 시스템")
st.divider()

# 왼쪽 사이드바에서 메뉴 선택
menu = st.sidebar.selectbox("기능 선택", ["단면적/인장강도 계산", "편평시험(Flattening) 계산"])

# --- 1. 단면적 및 인장강도 계산 기능 ---
if menu == "단면적/인장강도 계산":
    st.subheader("📏 단면적 및 인장강도 계산")
    st.write("외경과 두께를 입력해 단면적을 구하고, 최대 하중(kN)으로 강도를 확인하세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1, key="od_main")
    with col2:
        wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1, key="wt_main")
    
    area = 0.0
    if od > 2*wt and wt > 0:
        id_val = od - (2 * wt)
        area = (math.pi * (od**2 - id_val**2)) / 4
        st.success(f"✅ 단면적 계산 완료: {area:.2f} mm²")
        
        res_c1, res_c2 = st.columns(2)
        res_c1.metric("내경 (ID)", f"{id_val:.2f} mm")
        res_c2.metric("단면적 (Area)", f"{area:.2f} mm²")

        st.divider()
        
        # 강도 계산
        st.markdown("**⚙️ 인장강도(MPa) 변환**")
        max_load = st.number_input("시험 최대 하중 (kN)", min_value=0.0, step=0.1)
        if max_load > 0:
            ts = (max_load * 1000) / area
            st.metric("인장강도 (UTS)", f"{ts:.2f} MPa")
            
            with st.expander("추가: 항복하중을 알 경우"):
                y_load = st.number_input("항복 하중 (kN)", min_value=0.0, step=0.1)
                if y_load > 0:
                    ys = (y_load * 1000) / area
                    st.write(f"항복강도: **{ys:.2f} MPa**")
    else:
        st.info("외경과 두께를 입력해 주세요.")

# --- 2. 편평시험(Flattening) 계산 기능 ---
elif menu == "편평시험(Flattening) 계산":
    st.subheader("🔨 품목별 편평시험 목표치 계산")
    st.write("품목을 선택하고 외경(D)을 입력하면 목표 높이(H)를 산출합니다.")
    
    # 품목 선택 (보내주신 기준 적용)
    item = st.selectbox("품목(강종) 선택", [
        "SGT275 (일반구조용)",
        "SGT355 (일반구조용)",
        "SGT550 (일반구조용)",
        "SPP (배관용)",
        "SPPS (압력배관용)",
        "STKM12B (기계구조용)",
        "SNT275E (건축구조용)",
        "SNT355E (건축구조용)"
    ])
    
    st.divider()
    
    d_val = st.number_input("파이프 외경 입력 (D, mm)", min_value=0.0, step=0.1, format="%.2f")
    
    if d_val > 0:
        # 7/8D 그룹
        if item in ["SGT355 (일반구조용)", "SGT550 (일반구조용)", "SNT355E (건축구조용)"]:
            ratio_str = "7/8 D"
            h_val = (7/8) * d_val
        # 2/3D 그룹
        else:
            ratio_str = "2/3 D"
            h_val = (2/3) * d_val
            
        st.divider()
        st.subheader("📊 시험 결과")
        st.metric(label="목표 높이 (H)", value=f"{h_val:.2f} mm")
        
        st.warning(f"💡 {item} 품목은 외경의 {ratio_str}까지 압착해야 합니다.")
        st.info(f"평판 사이의 거리가 **{h_val:.2f} mm**가 될 때까지 누르세요.")
        
        with st.expander("📝 계산 근거 확인"):
            st.write(f"- 적용 기준: {ratio_str}")
            st.write(f"- 계산식: {d_val} × {ratio_str}")
            st.write(f"- 상세결과: {h_val:.4f} mm")
    else:
        st.info("외경(D)을 입력해 주세요.")

st.divider()
st.caption("© 2026 한진QC - 업무지원 통합 시스템")
