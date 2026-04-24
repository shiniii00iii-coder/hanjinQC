import streamlit as st
import math

# 웹페이지 설정
st.set_page_config(page_title="한진 0424 업무지원", layout="centered")

st.title("📏 중공철근(3872) 통합 계산기")
st.divider()

# 세션 상태를 사용하여 단면적 값을 탭 간에 공유
if 'area' not in st.session_state:
    st.session_state.area = 0.0

tab1, tab2 = st.tabs(["📏 단면적 계산", "⚖️ 단위 및 강도 변환"])

with tab1:
    st.subheader("📍 단면적 계산")
    col1, col2 = st.columns(2)
    with col1:
        od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1)
    with col2:
        wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1)

    if st.button("단면적 계산 실행", use_container_width=True):
        if od > 2 * wt and wt > 0:
            id_val = od - (2 * wt)
            st.session_state.area = (math.pi * (od**2 - id_val**2)) / 4
            
            st.success(f"✅ 계산 완료: 단면적 {st.session_state.area:.2f} mm²")
            c1, c2 = st.columns(2)
            c1.metric("내경 (ID)", f"{id_val:.2f} mm")
            c2.metric("단면적 (Area)", f"{st.session_state.area:.2f} mm²")
        else:
            st.error("⚠️ 치수 입력을 확인해 주세요.")

with tab2:
    st.subheader("⚙️ 하중 및 응력(MPa) 변환")
    
    # kN <-> ton 변환 섹션
    st.write("---")
    st.markdown("**1. 하중 단위 변환 (kN ↔ ton)**")
    load_val = st.number_input("하중 값 입력", min_value=0.0, step=1.0)
    mode = st.radio("방향", ["kN → ton", "ton → kN"], horizontal=True)
    
    if st.button("하중 변환", use_container_width=True):
        if mode == "kN → ton":
            res = load_val / 9.80665
            st.info(f"결과: **{res:.3f} ton**")
        else:
            res = load_val * 9.80665
            st.info(f"결과: **{res:.3f} kN**")

    # MPa 계산 섹션
    st.write("---")
    st.markdown("**2. 응력 계산 (kN → MPa)**")
    kn_val = st.number_input("시험 하중 입력 (kN)", min_value=0.0, step=1.0)
    
    # 단면적이 계산되어 있는지 확인
    if st.session_state.area > 0:
        st.write(f"현재 적용된 단면적: **{st.session_state.area:.2f} mm²**")
        if st.button("MPa 계산 (Stress)", use_container_width=True):
            # MPa = N/mm2 이므로 kN에 1000을 곱함
            mpa = (kn_val * 1000) / st.session_state.area
            st.metric("계산된 응력 (Stress)", f"{mpa:.2f} MPa")
            st.caption(f"공식: ({kn_val} × 1000) / {st.session_state.area:.2f}")
    else:
        st.warning("⚠️ 첫 번째 탭에서 먼저 '단면적 계산'을 완료해 주세요.")

st.divider()
st.caption("© 2026 한진QC 0424 프로젝트")
