import streamlit as st
import math

# 웹페이지 설정
st.set_page_config(page_title="한진 0424 업무지원", layout="centered")

st.title("📏 중공철근(3872) 통합 계산기")
st.write("치수를 입력하여 단면적을 구하고, 시험 하중(kN)을 입력해 응력(MPa)을 확인하세요.")
st.divider()

# 1. 단면적 계산 섹션
st.subheader("📍 1. 단면적 계산")
col1, col2 = st.columns(2)
with col1:
    od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1, key="od")
with col2:
    wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1, key="wt")

# 계산 로직 및 결과 표시
area = 0.0
if od > 0 and wt > 0:
    if od <= 2 * wt:
        st.error("⚠️ 두께가 외경보다 두꺼울 수 없습니다!")
    else:
        id_val = od - (2 * wt)
        area = (math.pi * (od**2 - id_val**2)) / 4
        
        st.success(f"✅ 단면적 계산 완료")
        res_c1, res_c2 = st.columns(2)
        res_c1.metric("내경 (ID)", f"{id_val:.2f} mm")
        res_c2.metric("단면적 (Area)", f"{area:.2f} mm²")

        st.divider()

        # 2. 응력 변환 섹션 (kN -> MPa)
        st.subheader("⚙️ 2. 응력(MPa) 변환")
        st.info(f"현재 적용 단면적: {area:.2f} mm²")
        
        kn_val = st.number_input("시험 하중 입력 (kN)", min_value=0.0, step=0.1, key="kn_val")
        
        if kn_val > 0:
            # MPa = (kN * 1000) / mm²
            mpa = (kn_val * 1000) / area
            st.metric("계산된 응력 (Stress)", f"{mpa:.2f} MPa")
            
            with st.expander("📝 변환 수식 보기"):
                st.write(f"공식: (하중 {kn_val} kN × 1000) ÷ 단면적 {area:.2f} mm²")
                st.write(f"결과: **{mpa:.2f} N/mm² (MPa)**")
        else:
            st.write("하중(kN)을 입력하면 MPa 결과가 여기에 표시됩니다.")

else:
    st.info("외경과 두께를 입력하면 계산이 시작됩니다.")

st.divider()

# 하중 단위 변환 (참고용으로 하단 배치)
with st.expander("⚖️ 하중 단위 간편 변환 (kN ↔ ton)"):
    col_a, col_b = st.columns(2)
    with col_a:
        unit_val = st.number_input("값 입력", min_value=0.0, key="unit_val")
    with col_b:
        unit_mode = st.radio("방향", ["kN → ton", "ton → kN"], horizontal=True)
    
    if unit_val > 0:
        if unit_mode == "kN → ton":
            st.write(f"결과: **{unit_val / 9.80665:.3f} ton**")
        else:
            st.write(f"결과: **{unit_val * 9.80665:.3f} kN**")
