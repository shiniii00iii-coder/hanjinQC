import streamlit as st
import os
import base64

# 제목 설정
st.set_page_config(page_title="한진QC 테스트 시스템", layout="wide")
st.title("📋 test423 규격서 관리 시스템")

# 1. 폴더 경로 설정 (test423 폴더 안에 pdf_files 폴더를 기준으로 함)
pdf_path = "pdf_files"

# 폴더가 없으면 자동으로 생성
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)

# 2. 폴더 내 PDF 파일 목록 가져오기
files = [f for f in os.listdir(pdf_path) if f.endswith(".pdf")]

# 사이드바 구성
st.sidebar.header("📁 규격서 목록")
if not files:
    st.sidebar.write("pdf_files 폴더에 PDF를 넣어주세요.")
else:
    selected_file = st.sidebar.selectbox("열람할 파일을 선택하세요", files)

    # 3. 파일 선택 시 화면에 출력
    if selected_file:
        st.subheader(f"📄 현재 열람 중: {selected_file}")
        
        file_full_path = os.path.join(pdf_path, selected_file)
        with open(file_full_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # PDF 뷰어 화면 크기 조절
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)