import streamlit as st
import os
import urllib.parse

st.set_page_config(page_title="한진QC 규격서 시스템", layout="wide")
st.title("📋 한진QC 규격서 관리 시스템 (test423)")

# 1. 깃허브 주소 설정 (네 계정 정보에 맞춰서 수정했어)
# 이 주소는 깃허브에 올라간 실제 PDF 파일의 '생' 주소를 가져오기 위함이야.
GITHUB_RAW_URL = "https://raw.githubusercontent.com/shiniii00iii-coder/hanjinQC/main/pdf_files/"

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
        
        # 파일명을 인터넷 주소 형식으로 변환
        encoded_file_name = urllib.parse.quote(selected_file)
        file_url = f"{GITHUB_RAW_URL}{encoded_file_name}"
        
        # 2. 구글 문서 뷰어를 사용하여 PDF 바로 띄우기
        # 이 방식은 브라우저 보안을 우회해서 화면에 바로 보여주는 가장 확실한 방법이야.
        google_view_url = f"https://docs.google.com/viewer?url={file_url}&embedded=true"
        
        st.markdown(
            f'<iframe src="{google_view_url}" width="100%" height="1000" style="border: none;"></iframe>',
            unsafe_allow_html=True
        )
        
        # 혹시 몰라서 하단에 링크 하나만 더 달아둘게
        st.caption(f"[화면이 안 나오면 클릭해서 직접 보기]({file_url})")