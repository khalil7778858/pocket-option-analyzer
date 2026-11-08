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
                # استخدام النموذج الافتراضي المدعوم للوسائط المتعددة
                model = genai.GenerativeModel('gemini-1.5-flash')
                
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
