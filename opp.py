import streamlit as st
import os
import base64

# 페이지 설정 (넓게 보기)
st.set_page_config(page_title="한진QC 규격서 시스템", layout="wide")

# 제목 및 스타일
st.title("📋 한진QC 규격서 관리 시스템 (test423)")
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    stDownloadButton {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

pdf_path = "pdf_files"

# 폴더 체크
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)

# 파일 목록
files = [f for f in os.listdir(pdf_path) if f.endswith(".pdf")]

# 사이드바
st.sidebar.header("📁 규격서 목록")
if not files:
    st.sidebar.info("pdf_files 폴더에 PDF 파일을 올려주세요.")
else:
    selected_file = st.sidebar.selectbox("파일을 선택하세요", files)

    if selected_file:
        st.subheader(f"📄 현재 열람 중: {selected_file}")
        
        file_full_path = os.path.join(pdf_path, selected_file)
        
        with open(file_full_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # PDF를 직접 브라우저에 임베딩 (가장 표준적인 방법)
            # height를 1000으로 늘려서 시원하게 보이게 함
            pdf_display = f'''
                <div style="border: 1px solid #ccc; border-radius: 5px;">
                    <embed
                        src="data:application/pdf;base64,{base64_pdf}"
                        width="100%"
                        height="1000"
                        type="application/pdf"
                    >
                </div>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)

            # 혹시 모를 상황을 대비해 아래쪽에 작게 다운로드 버튼 유지
            st.divider()
            st.download_button("📥 파일이 안 보이나요? 직접 다운로드", f.read(), file_name=selected_file)