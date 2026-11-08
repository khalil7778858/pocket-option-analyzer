import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Pocket Option AI Analyzer", page_icon="📈")
st.title("📈 محلل صفقات بوكت أوبشن الذكي")

api_key = st.text_input("أدخل مفتاح Google Gemini API Key:", type="password")
uploaded_file = st.file_uploader("اختر صورة الشارت:", type=["jpg", "jpeg", "png"])

if api_key and uploaded_file:
    genai.configure(api_key=api_key)
    image = Image.open(uploaded_file)
    st.image(image, caption="الشارت المرفوع", use_column_width=True)
    
    if st.button("🚀 تحليل الشارت"):
        with st.spinner("جاري التحليل..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([
                    "أنت محلل محترف لمنصة بوكت أوبشن. حلل الشارت وأعطني: 1. التوصية (CALL أو PUT). 2. المدة. 3. السبب باختصار.",
                    image
                ])
                st.success("✅ تم التحليل:")
                st.write(response.text)
            except Exception as e:
                st.error(f"خطأ: {e}")
