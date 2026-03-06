# Import libs
import cv2
import torch
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from ultralytics import YOLO
from datetime import datetime
import base64
from io import BytesIO
from fpdf import FPDF  # Required: pip install fpdf

# Page config
st.set_page_config(page_title="Embryo AI", layout="wide", page_icon="🧬")

# Init state
if 'history' not in st.session_state:
    st.session_state.history = []

# Top layout
c_title, c_tog = st.columns([8, 2])

# Render title
with c_title:
    st.markdown('<h2 style="margin:0; padding:0; background: -webkit-linear-gradient(45deg, #00C9FF, #8A2BE2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🧬 IVF AI Dashboard</h2>', unsafe_allow_html=True)

# Render toggle
with c_tog:
    st.write("") 
    is_dark = st.toggle("🌙 Dark / ☀️ Light", value=True)

# Theme logic
if is_dark:
    bg_col = "#170e49"
    txt_col = "#ffffff"
    card_bg = "linear-gradient(145deg, #141029, #110e22)"
    shadow = "8px 8px 16px #0b0918, -8px -8px 16px #1b1534"
    plt_bg = "rgba(0,0,0,0)"
    btn_grad = "linear-gradient(90deg, #00C9FF 0%, #8A2BE2 100%)"
    accent_col = "#00C9FF" 
    col_good = "#2ecc71"
    col_mod = "#f1c40f"
    col_bad = "#e74c3c"
    accent_col1 = "#B4B4B4"
else:
    bg_col = "#747db6"
    txt_col = "#000000"
    card_bg = "linear-gradient(145deg, #f2ebff, #cbc6da)"
    shadow = "8px 8px 16px #9A9898, -8px -8px 16px #747db6"
    plt_bg = "rgba(0,0,0,0)"
    btn_grad = "linear-gradient(90deg, #8A2BE2 0%, #00C9FF 100%)"
    accent_col = "#6a0dad" 
    col_good = "#1e8449" 
    col_mod = "#b8860b"  
    col_bad = "#c0392b"
    accent_col1 = "#535353"  

# Helper for segmented image base64
def get_image_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- NEW PDF LOGIC START ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 201, 255)  # Cyan accent
        self.cell(0, 10, 'IVF EMBRYO CLINICAL REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Report Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | AI-Generated Analysis', 0, 0, 'C')

def generate_pdf(data):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 10)
    
    # Table Header Styling
    pdf.set_fill_color(0, 201, 255)
    pdf.set_text_color(255, 255, 255)
    
    cols = list(data.columns)
    # Adjust widths for standard A4
    widths = [35, 75, 40, 40] 
    
    for i, col in enumerate(cols):
        pdf.cell(widths[i], 12, col.upper(), 1, 0, 'C', 1)
    pdf.ln()
    
    # Table Body
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    for index, row in data.iterrows():
        for i, col in enumerate(cols):
            pdf.cell(widths[i], 10, str(row[col]), 1, 0, 'C')
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')
# --- NEW PDF LOGIC END ---

# Inject CSS
st.markdown(f"""
    <style>
    /* Main bg */
    .stApp {{ background-color: {bg_col}; color: {txt_col}; transition: all 0.3s ease; }}
    
    /* 3D Shapes */
    .shape-3d {{
        background: {card_bg};
        border-radius: 20px;
        box-shadow: {shadow};
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        color: {txt_col};
        transition: all 0.3s ease;
        border: 2px solid {accent_col1};
    }}
    
    /* Text styles */
    .metric-title, .metric-title1 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: {txt_col}; }}
    .metric-val {{ font-size: 32px; font-weight: 800; margin-top: 5px; }}
    
    /* Standard Buttons */
    .stButton>button, [data-testid="stDownloadButton"] button {{
        background: {btn_grad} !important;
        color: #ffffff !important;
        border-radius: 30px !important;
        width: 100% !important;
        font-weight: 800 !important;
        border: 1px solid transparent !important;
        padding: 12px !important;
        box-shadow: {shadow} !important;
        transition: all 0.2s ease !important;
    }}

    /* Uploader Container */
    [data-testid="stFileUploader"] {{
        background: {card_bg} !important;
        box-shadow: {shadow} !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 20px !important;
        border: 2px solid {accent_col1} !important;
    }}
    
    /* Dropzone text fix */
    [data-testid="stFileUploadDropzone"] div, 
    [data-testid="stFileUploadDropzone"] span, 
    [data-testid="stFileUploadDropzone"] p,
    [data-testid="stFileUploadDropzone"] small {{
        color: {txt_col} !important;
    }}

    /* Browse Button */
    [data-testid="stFileUploader"] section button {{
        background: {btn_grad} !important;
        color: white !important;
        border-radius: 10px !important;
    }}

    /* Delete (Close) Button Style */
    [data-testid="stFileUploaderDeleteBtn"] {{
        background: {btn_grad} !important;
        border-radius: 8px !important;
        color: white !important;
        padding: 1px 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* White icon inside delete button */
    [data-testid="stFileUploaderDeleteBtn"] svg {{
        fill: white !important;
        color: white !important;
    }}

    /* Standard Image Container */
    [data-testid="stImage"] {{
        background: {card_bg} !important;
        border: 2px solid {accent_col} !important;
        border-radius: 20px !important;
        padding: 10px !important;
        box-shadow: {shadow} !important;
        overflow: hidden !important; 
    }}
    [data-testid="stImage"] img {{
        max-width: 100% !important;
        height: auto !important;
        border-radius: 15px !important;
    }}

    /* SEPARATE HTML/CSS FOR SEGMENTED IMAGE */
    .seg-container {{
        background: {card_bg};
        border: 2px solid {accent_col};
        border-radius: 20px;
        padding: 10px; 
        box-shadow: {shadow};
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }}
    .seg-container img {{
        max-width: 100%;
        height: auto;
        border-radius: 12px;
        display: block;
    }}
    
    /* Charts and Tables */
    [data-testid="stPlotlyChart"] {{
        background: {card_bg} !important;
        border: 2px solid {accent_col} !important;
        border-radius: 20px !important;
        padding: 10px !important;
        margin-left: -30px !important;
        box-shadow: {shadow} !important;
    }}
    table.dataframe {{
        width: 100%;
        border-collapse: collapse;
        color: {txt_col};
        background: {card_bg};
        border-radius: 10px;
        overflow: hidden;
    }}
    </style>
    """, unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return YOLO('best1.pt')

model = load_model()

def grade_embryo(img_array):
    res = model(img_array)
    if res[0].masks is None:
        return "No masks", 0.0, res[0]
        
    masks = res[0].masks.data
    classes = res[0].boxes.cls
    emb_mask = torch.zeros_like(masks[0])
    frag_mask = torch.zeros_like(masks[0])
    
    for m, c in zip(masks, classes):
        if int(c) == 0:
            emb_mask = torch.logical_or(emb_mask, m)
        elif int(c) == 1:
            frag_mask = torch.logical_or(frag_mask, m)
            
    frag_area = frag_mask.sum().item()
    total_mask = torch.logical_or(emb_mask, frag_mask)
    total_area = total_mask.sum().item()
            
    if total_area == 0:
        return "No embryo", 0.0, res[0]
        
    pct = (frag_area / total_area) * 100
    grade = "Good" if pct < 10 else "Moderate" if pct <= 25 else "Bad"
    return grade, pct, res[0]

def draw_meter(pct):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = pct,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Clinical Score", 'font': {'size': 20, 'color': txt_col}},
        number = {'suffix': "%", 'font': {'size': 45, 'color': accent_col}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': txt_col},
            'bar': {'color': "rgba(0,0,0,0)"}, 
            'bgcolor': "rgba(0,0,0,0)",
            'bordercolor': txt_col,
            'steps': [
                {'range': [0, 10], 'color': col_good},
                {'range': [10, 25], 'color': col_mod},
                {'range': [25, 100], 'color': col_bad}
            ],
            'threshold': {'line': {'color': txt_col, 'width': 6}, 'value': pct}
        }
    ))
    fig.update_layout(paper_bgcolor=plt_bg, font={'color': txt_col}, height=320, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# UI
c_left, c_right = st.columns([1, 1.5], gap="large")

with c_left:
    st.markdown('<div class="shape-3d"><div class="metric-title">📁 Image Input</div></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Select embryo image", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")
    if uploaded_file:
        image = Image.open(uploaded_file).convert('RGB')
        img_array = np.array(image)
        st.image(image, use_container_width=True)

with c_right:
    st.markdown('<div class="shape-3d"><div class="metric-title">⚡ Live Analysis</div></div>', unsafe_allow_html=True)
    if uploaded_file:
        if st.button("🚀 Analyze Now"):
            with st.spinner('Analyzing...'):
                grade, pct, result = grade_embryo(img_array)
                st.session_state.history.append({"Time": datetime.now().strftime("%H:%M:%S"), "File": uploaded_file.name, "Fragmentation": f"{pct:.2f}%", "Grade": grade})
                
                k1, k2 = st.columns(2)
                with k1:
                    st.markdown(f'<div class="shape-3d"><div class="metric-title">Fragmentation</div><div class="metric-val" style="color:{accent_col};">{pct:.2f}%</div></div>', unsafe_allow_html=True)
                with k2:
                    g_col = col_good if grade == "Good" else col_mod if grade == "Moderate" else col_bad
                    st.markdown(f'<div class="shape-3d"><div class="metric-title">Clinical Grade</div><div class="metric-val" style="color:{g_col};">{grade}</div></div>', unsafe_allow_html=True)
                
                b1, b2 = st.columns(2)
                with b1: st.plotly_chart(draw_meter(pct), use_container_width=True)
                with b2:
                    # CUSTOM HTML/CSS RENDER FOR SEGMENTED IMAGE
                    annotated_img_cv = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(annotated_img_cv)
                    img_base64 = get_image_base64(pil_img)
                    
                    st.markdown(f"""
                        <div class="seg-container">
                            <img src="data:image/png;base64,{img_base64}" />
                        </div>
                        <p style="text-align:center; color:{txt_col}; margin-top:5px; font-size:12px;">AI Segmentation</p>
                    """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="shape-3d"><div class="metric-title1">Awaiting image upload...</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="shape-3d"><div class="metric-title">📋 Session Records</div></div>', unsafe_allow_html=True)
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.markdown(f'<div class="shape-3d" style="padding:0;">{df.to_html(classes="dataframe", index=False)}</div>', unsafe_allow_html=True)
    
    # NEW DOWNLOAD ACTIONS
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button("📥 Download CSV", df.to_csv(index=False).encode('utf-8'), "report.csv", "text/csv")
    with d_col2:
        pdf_bytes = generate_pdf(df)
        st.download_button("📄 Download PDF Report", pdf_bytes, "embryo_clinical_report.pdf", "application/pdf")
