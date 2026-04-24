import streamlit as st
import math

st.set_page_config(page_title="한진 0424 업무지원", layout="centered")

st.title("📏 중공철근(3872) 인장강도 계산기")
st.write("단면적을 구하고 최대 하중(kN)을 입력해 인장강도를 즉시 확인하세요.")
st.divider()

# 1. 단면적 계산
st.subheader("📍 1. 단면적(Area) 산출")
c1, c2 = st.columns(2)
with c1:
    od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1)
with c2:
    wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1)

area = 0.0
if od > 2 * wt and wt > 0:
    id_val = od - (2 * wt)
    area = (math.pi * (od**2 - id_val**2)) / 4
    st.success(f"단면적: {area:.2f} mm²")
else:
    st.info("외경과 두께를 정확히 입력해 줘.")

st.divider()

# 2. 인장강도 계산
if area > 0:
    st.subheader("⚙️ 2. 인장강도(MPa) 변환")
    max_load = st.number_input("시험 최대 하중 (kN)", min_value=0.0, step=0.1)
    
    if max_load > 0:
        tensile_strength = (max_load * 1000) / area
        st.metric("인장강도 (Tensile Strength)", f"{tensile_strength:.2f} MPa")
        
        # 참고용 항복강도 입력 (필요할 때만)
        with st.expander("추가: 항복하중을 알 경우 (클릭)"):
            y_load = st.number_input("항복 하중 (kN)", min_value=0.0, step=0.1)
            if y_load > 0:
                y_strength = (y_load * 1000) / area
                st.write(f"항복강도: **{y_strength:.2f} MPa**")
    else:
        st.write("최대 하중을 입력하면 MPa 결과가 나옵니다.")

st.divider()
st.caption("© 2026 한진QC 0424 프로젝트")
