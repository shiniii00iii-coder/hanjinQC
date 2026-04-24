import streamlit as st
import math

# 웹페이지 설정 (브라우저 탭에 보일 이름)
st.set_page_config(page_title="한진 0424 프로젝트", layout="centered")

# 화면에 보일 제목
st.title("📏 중공철근(3872) 단면적 계산기")
st.info("외경과 두께를 입력하면 내경과 단면적을 계산합니다.")
st.divider()

# 숫자 입력 받는 칸
col1, col2 = st.columns(2)

with col1:
    od = st.number_input("외경 (OD, mm)", min_value=0.0, value=0.0, step=0.1)

with col2:
    wt = st.number_input("두께 (WT, mm)", min_value=0.0, value=0.0, step=0.1)

# 계산하기 버튼
if st.button("계산 실행", use_container_width=True):
    if od > 0 and wt > 0:
        if od <= 2 * wt:
            st.error("⚠️ 두께가 외경보다 두꺼울 수 없습니다. 수치를 확인해 주세요!")
        else:
            # 계산 로직
            id_val = od - (2 * wt)
            area = (math.pi * (od**2 - id_val**2)) / 4
            
            # 결과 표시
            st.success("✅ 계산 완료")
            res_col1, res_col2 = st.columns(2)
            
            res_col1.metric("내경 (ID)", f"{id_val:.2f} mm")
            res_col2.metric("단면적 (Area)", f"{area:.2f} mm²")
            
            # 수식 설명 (현장에서 검증할 때 편리함)
            with st.expander("📝 계산 수식 보기"):
                st.write(f"- 내경: {od} - (2 × {wt}) = **{id_val:.2f} mm**")
                st.write(f"- 단면적: (π/4) × ({od}² - {id_val:.2f}²) = **{area:.2f} mm²**")
    else:
        st.warning("계산할 외경과 두께를 입력해 주세요.")

st.divider()
st.caption("© 2026 한진QC 0424 프로젝트 - 품질관리 지원팀")
