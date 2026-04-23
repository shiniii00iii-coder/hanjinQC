import streamlit as st
import os
import base64

st.set_page_config(page_title="한진QC 규격서 시스템", layout="wide")
st.title("📋 한진QC 규격서 관리 시스템 (test423)")

pdf_path = "pdf_files"

if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)

files = [f for f in os.listdir(pdf_path) if f.endswith(".pdf")]

st.sidebar.header("📁 규격서 목록")
if not files:
    st.sidebar.info("pdf_files 폴더에 PDF 파일을 올려주세요.")
else:
    selected_file = st.sidebar.selectbox("파일을 선택하세요", files)

    if selected_file:
        st.subheader(f"📄 현재 열람 중: {selected_file}")
        
        file_full_path = os.path.join(pdf_path, selected_file)
        
        with open(file_full_path, "rb") as f:
            pdf_bytes = f.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            
            # 1. 다운로드 버튼 추가 (가장 확실한 방법)
            st.download_button(
                label="📥 이 규격서 다운로드 / 전체화면 보기",
                data=pdf_bytes,
                file_name=selected_file,
                mime="application/pdf"
            )
            
            # 2. 화면에 직접 띄우기 (iframe 방식 보완)
            # 브라우저에 따라 차단될 수 있으니 높이를 충분히 줌
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)