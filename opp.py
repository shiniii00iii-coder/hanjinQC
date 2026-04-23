import streamlit as st
import os
import base64

# 웹사이트 제목과 레이아웃 설정
st.set_page_config(page_title="한진QC 규격서 시스템", layout="wide")
st.title("📋 한진QC 규격서 관리 시스템 (test423)")

# PDF 파일들이 저장될 폴더 이름
pdf_path = "pdf_files"

# 만약 폴더가 없으면 에러 방지를 위해 생성
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)

# 폴더 안의 PDF 파일 목록 읽기
files = [f for f in os.listdir(pdf_path) if f.endswith(".pdf")]

# 사이드바 메뉴
st.sidebar.header("📁 규격서 목록")
if not files:
    st.sidebar.info("pdf_files 폴더에 PDF 파일을 올려주세요.")
else:
    selected_file = st.sidebar.selectbox("파일을 선택하세요", files)

    if selected_file:
        st.subheader(f"📄 현재 열람 중: {selected_file}")
        
        # PDF 파일을 웹 화면에 띄우기 위한 처리
        file_full_path = os.path.join(pdf_path, selected_file)
        with open(file_full_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # 웹 브라우저용 PDF 뷰어 삽입
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)