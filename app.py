import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Pocket Option AI Analyzer", page_icon="📈", layout="centered")

st.title("📈 محلل صفقات بوكت أوبشن الذكي")
st.markdown("قم برفع صورة الشارت الحي، وسيقوم النظام بتحليله فوراً وإعطائك التوصية الدقيقة.")

api_key = st.text_input("أدخل مفتاح Google Gemini API Key الخاص بك:", type="password")

if api_key:
    genai.configure(api_key=api_key)

uploaded_file = st.file_uploader("اختر صورة الشارت من منصة بوكت أوبشن:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="الشارت المرفوع حالياً", use_column_width=True)
    
    if st.button("🚀 تحليل الشارت واستخراج الصفقة"):
        with st.spinner("⏳ جاري تحليل الشارت وقراءة الشمعات والاتجاه..."):
            try:
                # استخدام النموذج المستقر المدعوم للرؤية وتحليل الصور
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = (
                    "أنت خبير محترف في التحليل الفني وثنائيات الخيارات (Pocket Option). "
                    "قم بتحليل صورة الشارت المرفوعة بدقة (الاتجاه، الدعوم، المقاومة، وحركة الشمعات الأخيرة). "
                    "أعطني النتيجة بالصيغة التالية بدقة واختصار:\n"
                    "1. التوصية: (CALL لشراء صعوداً 🟢 أو PUT لبيع هبوطاً 🔴)\n"
                    "2. المدة المقترحة للصفقة: (مثلاً: دقيقة واحدة أو دقيقتان)\n"
                    "3. السبب الفني باختصار شديد ومبسط."
                )
                
                response = model.generate_content([prompt, image])
                
                st.success("✅ تم التحليل بنجاح!")
                st.markdown("### 📊 نتيجة التوصية:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")
elif uploaded_file is not None and not api_key:
    st.warning("⚠️ يرجى إدخال مفتاح الـ API في الحقل بالأعلى لكي يعمل التحليل.")
