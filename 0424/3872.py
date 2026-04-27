import streamlit as st
import pandas as pd
import math
import os

# 웹페이지 설정
st.set_page_config(page_title="한진 품질관리 통합 시스템", layout="centered")

st.title("🏭 파이프 품질관리 통합 시스템")
st.divider()

# 엑셀 파일 경로 설정 (파일명이 정확해야 함)
EXCEL_FILE = "0424/3월 품질우려제품리스트.xlsx"

# 엑셀 데이터 불러오기 함수
@st.cache_data # 데이터를 매번 새로 읽지 않고 캐시에 저장해 속도를 높임
def load_data():
    if os.path.exists(EXCEL_FILE):
        # 엑셀 파일을 읽어옴
        df = pd.read_excel(EXCEL_FILE)
        return df
    else:
        return None

df_spec = load_data()

# 왼쪽 사이드바 메뉴
menu = st.sidebar.selectbox("기능 선택", ["편평시험(Flattening) 계산", "단면적/인장강도 계산"])

# --- 1. 편평시험 계산 기능 (엑셀 연동) ---
if menu == "편평시험(Flattening) 계산":
    st.subheader("🔨 엑셀 기반 편평시험 목표치 계산")
    
    if df_spec is not None:
        # 엑셀의 '품목명' 열을 리스트로 가져와서 선택 상자 만듦
        # 주의: 엑셀의 열 이름이 '품목명'이 아니면 그에 맞게 수정 필요
        item_list = df_spec['품목명'].tolist()
        selected_item = st.selectbox("품목 선택 (엑셀 데이터)", item_list)
        
        # 선택된 품목의 정보 가져오기
        item_info = df_spec[df_spec['품목명'] == selected_item].iloc[0]
        
        # 계산 방식(비율) 가져오기 (예: '2/3', '7/8' 또는 0.66, 0.87)
        # 엑셀에 '계산방식'이라는 열이 있다고 가정
        raw_ratio = item_info['계산방식']
        
        # 문자열(2/3)을 숫자(0.666)로 변환하는 로직
        if isinstance(raw_ratio, str):
            if "/" in raw_ratio:
                num, den = raw_ratio.split('/')
                ratio = float(num) / float(den)
            else:
                ratio = float(raw_ratio)
        else:
            ratio = float(raw_ratio)

        st.divider()
        d_val = st.number_input("파이프 외경 입력 (D, mm)", min_value=0.0, step=0.1, format="%.2f")
        
        if d_val > 0:
            h_val = ratio * d_val
            press_val = d_val - h_val
            
            st.divider()
            st.subheader("📊 시험 결과")
            st.info(f"**목표 높이(H): {h_val:.2f}mm ({press_val:.2f}mm 누를 것)**")
            
            c1, c2 = st.columns(2)
            c1.metric("최종 목표 높이 (H)", f"{h_val:.2f} mm")
            c2.metric("압착 필요량 (Press)", f"{press_val:.2f} mm")
            
            st.warning(f"💡 해당 품목은 외경의 {raw_ratio}까지 압착합니다.")
    else:
        st.error(f"엑셀 파일({EXCEL_FILE})을 찾을 수 없습니다. 깃허브에 파일을 올렸는지 확인해 주세요.")

# --- 2. 단면적 및 인장강도 계산 기능 ---
elif menu == "단면적/인장강도 계산":
    st.subheader("📏 단면적 및 인장강도 계산")
    od = st.number_input("외경 (OD, mm)", min_value=0.0, step=0.1)
    wt = st.number_input("두께 (WT, mm)", min_value=0.0, step=0.1)
    
    if od > 2*wt and wt > 0:
        area = (math.pi * (od**2 - (od - 2*wt)**2)) / 4
        st.success(f"✅ 단면적: {area:.2f} mm²")
        st.divider()
        max_load = st.number_input("시험 최대 하중 (kN)", min_value=0.0, step=0.1)
        if max_load > 0:
            ts = (max_load * 1000) / area
            st.metric("인장강도 (UTS)", f"{ts:.2f} MPa")

st.divider()
st.caption("© 2026 한진QC - 엑셀 연동 품질관리 시스템")
