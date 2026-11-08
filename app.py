import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Pocket Option AI Analyzer", page_icon="📈", layout="centered")

st.title("📈 محلل صفقات بوكت أوبشن الذكي")
st.markdown("قم برفع صورة الشارت الحي، وسيقوم النظام بتحليله فوراً وإعطائك التوصية (شراء/بيع) مع المدة المناسبة.")

api_key = st.text_input("أدخل مفتاح Google Gemini API Key الخاص بك:", type="password")

if api_key:
    genai.configure(api_key=api_key)

uploaded_file = st.file_uploader("اختر صورة الشارت (منصة بوكت أوبشن):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="الشارت المرفوع حالياً", use_column_width=True)
    
    if st.button("🚀 تحليل الشارت واستخراج الصفقة"):
        with st.spinner("⏳ جاري قراءة المؤشرات والزخم..."):
            try:
                # حل نهائي ومضمون: فحص النماذج المتاحة في حسابك واختيار أول نموذج يدعم الصور تلقائياً
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                selected_model_name = None
                for m_name in available_models:
                    if 'flash' in m_name or 'pro' in m_name:
                        selected_model_name = m_name
                        break
                
                if not selected_model_name and available_models:
                    selected_model_name = available_models[0]
                elif not selected_model_name:
                    selected_model_name = 'gemini-1.5-flash'
                
                model = genai.GenerativeModel(selected_model_name)
                
                prompt = (
                    "أنت محلل محترف لمنصة بوكت أوبشن (Pocket Option). "
                    "قم بتحليل صورة الشارت المرفوعة بدقة عالية (تحليل فني، اتجاه، دعوم ومقاومات، مؤشرات). "
                    "أعطني النتيجة بالشكل التالي:\n"
                    "1. التوصية: (CALL / شراء صعوداً أو PUT / بيع هبوطاً)\n"
                    "2. المدة المقترحة للصفقة: (مثلاً دقيقة أو دقيقتان)\n"
                    "3. السبب باختصار شديد ومبسط."
                )
                
                response = model.generate_content([prompt, image])
                
                st.success("✅ تم التحليل بنجاح!")
                st.markdown("### 📊 نتيجة التحليل والتوصية:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالمعالج: {e}")
elif uploaded_file is not None and not api_key:
    st.warning("⚠️ لكي يعمل النظام برمجياً، يرجى إدخال مفتاح الـ API الخاص بك في الأعلى.")
