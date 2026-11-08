import streamlit as st
from PIL import Image
import google.generativeai as genai

# إعداد الصفحة وتصميمها
st.set_page_config(page_title="Pocket Option AI Analyzer", page_icon="📈", layout="centered")

st.title("📊 محلل صفقات بوكت أوبشن الذكي")
st.markdown("قم برفع صورة الشارت الحي، وسيقوم النظام بتحليله فوراً وإعطائك التوصية (شراء/بيع) مع المدة المناسبة.")

# إدخال مفتاح الـ API الخاص بك
api_key = st.text_input("أدخل مفتاح Google Gemini API Key الخاص بك:", type="password")

# زر لرفع الصورة
uploaded_file = st.file_uploader("اختر صورة الشارت (منصة بوكت أوبشن):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and api_key:
    # عرض الصورة على التطبيق
    image = Image.open(uploaded_file)
    st.image(image, caption="الشارت المرفوع حالياً", use_column_width=True)
    
    if st.button("🚀 تحليل الشارت واستخراج الصفقة"):
        with st.spinner("جاري قراءة الشموع وتحليل المؤشرات والزخم..."):
            try:
                # إعداد الاتصال بالنموذج
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # صياغة الطلب للذكاء الاصطناعي
                prompt = """
                أنت خبير محترف في التداول وتحليل السعر (Price Action) والخيارات الثنائية على منصة Pocket Option.
                قم بتحليل صورة الشارت المرفوعة بدقة، وانظر إلى:
                1. زوج العملات والإطار الزمني (إن وجد).
                2. اتجاه الشموع الأخيرة وأحجامها والزيول (Wicks).
                3. نسبة معنويات السوق (النسبة المئوية للشراء والبيع الظاهرة).
                4. مؤشرات المتوسط المتحرك أو مؤشرات التشبع إن ظهرت.
                
                بناءً على ذلك، أعطني:
                - **التوصية الحاسمة:** (شراء CALL أو بيع PUT).
                - **مدة الصفقة المقترحة:** (مثلاً 5 دقائق بناءً على إطار الشمعة).
                - **السبب الفني:** شرح مختصر جداً وسريع لسبب هذه التوصية (تشبع، كسر، ارتداد، أو سيطرة بائعين/مشترين).
                """
                
                response = model.generate_content([prompt, image])
                
                st.success("تم التحليل بنجاح! إليك القرار الفني:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالمعالج: {e}")
elif not api_key:
    st.warning("يرجى إدخال مفتاح الـ API لكي يعمل النظام برمجياً بكفاءة.")
