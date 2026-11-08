import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="Pocket Option Pro Signal", page_icon="🎯", layout="centered")

st.markdown("<h1 style='text-align: center; color: #00CC66;'>🎯 محلل صفقات بوكت أوبشن الاحترافي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>برنامج جديد ومستقر لتحليل الشارت واستخراج التوصيات بدقة</p>", unsafe_allow_html=True)

# إدخال مفتاح الـ API
api_key = st.text_input("🔑 أدخل مفتاح Google Gemini API Key الخاص بك:", type="password")

# رفع صورة الشارت
uploaded_file = st.file_uploader("📂 اختر صورة الشارت (منصة بوكت أوبشن):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الشارت المرفوع", use_column_width=True)

if st.button("🚀 ابدأ تحليل الصفقة الآن", type="primary"):
    if not api_key:
        st.error("⚠️ الرجاء إدخال مفتاح الـ API أولاً.")
    elif not uploaded_file:
        st.error("⚠️ الرجاء رفع صورة الشارت أولاً.")
    else:
        with st.spinner("🔄 جاري إرسال الشارت ومعالجة التحليل الفني..."):
            try:
                # تحويل الصورة إلى صيغة Base64 للإرسال المباشر
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                
                # استخدام رابط الاتصال المباشر المحدث والمدعوم رسمياً من جوجل
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                
                payload = {
                    "contents": [{
                        "parts": [
                            {
                                "text": (
                                    "أنت خبير محترف ومحلل مالي لمنصة بوكت أوبشن (Pocket Option). "
                                    "قم بتحليل الشارت المرفق بدقة متناهية. أعطني النتيجة بالتنسيق التالي:\n"
                                    "1. التوصية: (CALL لشراء صعوداً 🟢 أو PUT لبيع هبوطاً 🔴)\n"
                                    "2. مدة الصفقة المناسبة: (مثلاً: دقيقة أو دقيقتان)\n"
                                    "3. السبب الفني باختصار شديد ومبسط."
                                )
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": img_str
                                }
                            }
                        ]
                    }]
                }
                
                response = requests.post(url, json=payload, headers=headers)
                result = response.json()
                
                if response.status_code == 200:
                    try:
                        ai_text = result['candidates'][0]['content']['parts'][0]['text']
                        st.success("✅ تمت عملية التحليل بنجاح!")
                        st.markdown("---")
                        st.markdown("### 📊 نتيجة التوصية:")
                        st.markdown(ai_text)
                    except Exception as parse_err:
                        st.error(f"خطأ في قراءة رد الخادم: {parse_err} | الرد الكامل: {result}")
                else:
                    error_message = result.get('error', {}).get('message', 'خطأ غير معروف')
                    st.error(f"❌ خطأ من الخادم (رمز {response.status_code}): {error_message}")
                    
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال بالشبكة: {e}")
