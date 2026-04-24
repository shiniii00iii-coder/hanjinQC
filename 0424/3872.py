import streamlit as st
import math

# 웹페이지 설정
st.set_page_config(page_title="한진 0424 프로젝트", layout="centered")

st.title("📏 중공철근(3872) 업무지원 툴")
st.divider()

# 탭을 나눠서 계산기와 변환기를 깔끔하게 분리
tab1, tab2 = st.tabs(["중공철근 단면적 계산", "kN ↔ ton 단위 변환"])

with tab1:
    st.subheader("📍 단면적 계산기")
    col1, col2 = st.columns(2)
    with col1:
        od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1, key="od_input")
    with col2:
        wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1, key="wt_input")

    if st.button("단면적 계산 실행", use_container_width=True):
        if od > 0 and wt > 0:
            if od <= 2 * wt:
                st.error("⚠️ 두께가 외경보다 두꺼울 수 없습니다!")
            else:
                id_val = od - (2 * wt)
                area = (math.pi * (od**2 - id_val**2)) / 4
                
                st.success("✅ 계산 완료")
                res_c1, res_c2 = st.columns(2)
                res_c1.metric("내경 (ID)", f"{id_val:.2f} mm")
                res_c2.metric("단면적 (Area)", f"{area:.2f} mm²")
        else:
            st.warning("치수를 입력해 주세요.")

with tab2:
    st.subheader("⚖️ 하중 단위 변환기")
    st.write("인장하중 값을 입력하면 자동으로 변환됩니다.")
    
    input_val = st.number_input("변환할 하중 입력", min_value=0.0, step=1.0)
    direction = st.radio("변환 방향 선택", ["kN → ton", "ton → kN"], horizontal=True)
    
    # 변환 상수 (표준 중력 가속도 9.80665 적용)
    # 1 ton(f) = 9.80665 kN
    if st.button("단위 변환 실행", use_container_width=True):
        if input_val > 0:
            if direction == "kN → ton":
                result = input_val / 9.80665
                st.metric(f"{input_val} kN", f"{result:.3f} ton")
            else:
                result = input_val * 9.80665
                st.metric(f"{input_val} ton", f"{result:.3f} kN")
            
            st.caption("※ 적용 공식: 1 ton = 9.80665 kN")
        else:
            st.warning("변환할 값을 입력해 주세요.")

st.divider()
st.caption("© 2026 한진QC 0424 프로젝트")
