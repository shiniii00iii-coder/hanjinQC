import streamlit as st
import math

# 웹페이지 설정
st.set_page_config(page_title="한진 0424 업무지원", layout="centered")

st.title("📏 중공철근(3872) 통합 계산기")
st.write("치수를 입력해 단면적을 구하고, 인장/항복 하중(kN)을 입력해 강도를 확인하세요.")
st.divider()

# 1. 단면적 계산 섹션
st.subheader("📍 1. 단면적 계산")
col1, col2 = st.columns(2)
with col1:
    od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1, key="od")
with col2:
    wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1, key="wt")

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

        # 2. 인장 및 항복강도 계산 섹션
        st.subheader("⚙️ 2. 인장강도 및 항복강도 계산")
        st.info(f"현재 적용 단면적: {area:.2f} mm²")
        
        col_tensile, col_yield = st.columns(2)
        
        with col_tensile:
            max_load = st.number_input("최대 하중 (kN)", min_value=0.0, step=0.1, help="인장강도용 최대 하중")
        with col_yield:
            yield_load = st.number_input("항복 하중 (kN)", min_value=0.0, step=0.1, help="항복강도용 항복점 하중")
        
        if st.button("강도 계산 실행", use_container_width=True):
            if max_load > 0 or yield_load > 0:
                res_t1, res_t2 = st.columns(2)
                
                if max_load > 0:
                    tensile_strength = (max_load * 1000) / area
                    res_t1.metric("인장강도", f"{tensile_strength:.2f} MPa")
                
                if yield_load > 0:
                    yield_strength = (yield_load * 1000) / area
                    res_t2.metric("항복강도", f"{yield_strength:.2f} MPa")
                
                st.caption(f"※ 계산 공식: (하중 × 1000) ÷ {area:.2f} mm²")
            else:
                st.warning("하중 값을 입력해 주세요.")

else:
    st.info("외경과 두께를 입력하면 계산이 시작됩니다.")

st.divider()
st.caption("© 2026 한진QC 0424 프로젝트")
