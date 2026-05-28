import streamlit as st
import subprocess
import time
import json
import os

# -------------------------------------------------------------------
# 🎨 تهيئة الصفحة وإعدادات الهوية البصرية الفاخرة المخصصة (Custom CSS)
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Kamo AI Ultra - Web Client",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق نمط الـ UI المظلم والسيان المشابه تماماً لتطبيق customtkinter السابق
# تطبيق نمط الـ UI المظلم والسيان المشابه تماماً لتطبيق customtkinter السابق
st.markdown("""
    <style>
        /* الخلفية العامة للتطبيق */
        .stApp {
            background-color: #0E0E12 !important;
            color: #E2E8F0 !important;
        }
        /* القائمة الجانبية Custom Sidebar */
        [data-testid="stSidebar"] {
            background-color: #111116 !important;
            border-right: 1px solid #1E1E28;
        }
        /* أزرار الإدخال والتحكم */
        .stButton>button {
            background-color: #1E1E2E !important;
            color: #00F0FF !important;
            border: 1px solid #2D2D3F !important;
            border-radius: 8px !important;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2D2D3F !important;
            color: #00C8D6 !important;
            border-color: #00F0FF !important;
        }
        /* صناديق الرسائل الشات */
        .user-msg {
            background-color: #16161F;
            border-left: 4px solid #00F0FF;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .ai-msg {
            background-color: #0F172A;
            border-left: 4px solid #8A2BE2;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .system-event {
            background-color: #2A1215;
            border-left: 4px solid #FF4A4A;
            padding: 12px;
            border-radius: 8px;
            color: #FF8F8F;
        }
    </style>
""", unsafe_allow_html=True) # تم تعديل هذا السطر هنا لتصحيح الخطأ المطبعي

# -------------------------------------------------------------------
# 💾 إدارة الجلسات والذاكرة المؤقتة للمتصفح (Session State)
# -------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = ["جلسة محادثة جديدة #1"]

AVAILABLE_MODELS = [
    "opencode/deepseek-v4-flash-free",
    "opencode/gemini-3-flash",
    "opencode/gpt-5.4-mini",
    "opencode/gpt-5.1-codex-mini",
    "opencode/mimo-v2.5-free",
    "opencode/nemotron-3-super-free"
]

MODELS_INFO_DATA = {
    "opencode/deepseek-v4-flash-free": "🚀 الأفضل في: السرعة الفائقة، الإجابات المختصرة، وحل المشاكل البرمجية السريعة والذكية.",
    "opencode/gemini-3-flash": "🧠 الأفضل في: معالجة النصوص الطويلة، تحليل المستندات، والردود السريعة والذكية جداً.",
    "opencode/gpt-5.4-mini": "⚡ الأفضل في: المحادثات العامة المتقدمة، المساعدة الذكية اليومية، وتنسيق الأفكار بكفاءة ممتازة.",
    "opencode/gpt-5.1-codex-mini": "💻 الأفضل في: كتابة وتدقيق الأكواد البرمجية، حل ثغرات البرمجة المعقدة، وفهم بنية المشاريع.",
    "opencode/mimo-v2.5-free": "🎨 الأفضل في: الكتابة الإبداعية، صناعة المحتوى، وتوليد الأفكار التسويقية المبتكرة.",
    "opencode/nemotron-3-super-free": "🛡️ الأفضل في: معالجة البيانات الضخمة، حل مسائل الرياضيات المعقدة، والاستدلال المنطقي."
}

# -------------------------------------------------------------------
# 1. القائمة الجانبية للمتصفح (Web Sidebar)
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#FFFFFF; font-family:Segoe UI Nova;'>● KAMO AI STUDIO</h2>", unsafe_allow_html=True)
    st.markdown("<span style='background-color:#1E1E28; color:#8A2BE2; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:bold;'>WEB ULTRA v2.5 PRO</span>", unsafe_allow_html=True)
    st.write("")
    
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.write("")
    st.markdown("<p style='color:#555565; font-size:12px; font-weight:bold;'>RECENT SESSIONS</p>", unsafe_allow_html=True)
    for chat_title in st.session_state.history:
        st.markdown(f"<p style='color:#A0A0AA; font-size:14px; cursor:pointer;'>💬 {chat_title}</p>", unsafe_allow_html=True)
        
    st.write("")    # صندوق توثيق المطور
    st.markdown("""
        <div style='background-color:#16161F; padding:12px; border-radius:12px; border:1px solid #222230;'>
            <p style='margin:0; font-size:13px; font-weight:bold; color:#00F0FF;'>👑 Instagram: dio_sama100</p>
        </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 2. منطقة الشات العلوية والخيارات (Main Stage)
# -------------------------------------------------------------------
col_nav1, col_nav2 = st.columns([3, 1])
with col_nav1:
    selected_model = st.selectbox("ACTIVE AI MODEL:", AVAILABLE_MODELS)

with col_nav2:
    # بديل زر الثلاث شرط السينمائي في الويب عبر الـ Expander
    with st.expander("☰ Menu Options"):
        if st.button("📊 Models Info", use_container_width=True):
            st.toast("تم فتح دليل الموديلات بالأسفل!", icon="📊")
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("النظام يعمل بأعلى كفاءة. النمط الداكن مقفل افتراضياً لراحة العين.")

# عرض نافذة المعلومات في حال أراد المستخدم قراءتها
with st.container():
    if st.checkbox("Show Model Matrix Directory 📊"):
        st.markdown("### 📊 SYSTEM MODELS SPECS DIRECTORY")
        for name, capability in MODELS_INFO_DATA.items():
            st.markdown(f"**`{name}`**\n*{capability}*\n---")

st.write("---")

# -------------------------------------------------------------------
# 3. عرض سيرة المحادثة المستمرة (Chat Viewport)
# -------------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "USER":
        st.markdown(f"<div class='user-msg'><b>👤 YOU:</b><br>{msg['text']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "AI":
        st.markdown(f"<div class='ai-msg'><b>🤖 KAMO AI ({msg['model']}):</b><br>{msg['text']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "SYSTEM":
        st.markdown(f"<div class='system-event'><b>⚡ System Event:</b><br>{msg['text']}</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 4. معالجة البيانات والحل الذكي التلقائي (Auto-Fallback Backend)
# -------------------------------------------------------------------
def execute_web_matrix(prompt, target_model):
    stdout, stderr = "", ""
    success = False
    max_retries = 2
    
    # محاولة الاستدعاء مع التكرار الآلي
    for attempt in range(max_retries):
        try:
            full_command = f'opencode run "{prompt}" -m {target_model}'
            process = subprocess.Popen(
                full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding='utf-8'
            )
            stdout, stderr = process.communicate()
            
            if stdout.strip() and "UnknownError" not in stdout and "Error:" not in stdout:
                success = True
                break
            time.sleep(1)
        except:
            time.sleep(1)
            
    # الحل التلقائي السريع والتحويل إلى Deepseek المستقر والمضمون
    if not success:
        fallback_model = "opencode/deepseek-v4-flash-free"
        if target_model != fallback_model:
            st.warning(f"⚠️ الموديل الحالي لم يستجب. جاري الانتقال الآلي لإحضار الإجابة عبر {fallback_model.split('/')[-1]}...")
            try:
                full_command = f'opencode run "{prompt}" -m {fallback_model}'
                process = subprocess.Popen(
                    full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, encoding='utf-8'
                )
                stdout, stderr = process.communicate()
                target_model = fallback_model
                if stdout.strip():
                    success = True
            except Exception as e:
                stderr = str(e)
                
    if success and stdout.strip():
        return stdout.strip(), target_model
    else:
        return None, stderr.strip() if stderr.strip() else "حدث خطأ غير متوقع في خادم الموديلات."

# -------------------------------------------------------------------
# 5. صندوق المدخلات العائم أسفل الموقع
# -------------------------------------------------------------------
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Message Kamo AI...", placeholder="Type your query and press Transmit...")
    submit_button = st.form_submit_button(label="✦ TRANSMIT")
if submit_button and user_input.strip():
    prompt = user_input.strip()
    
    # إضافة سؤال المستخدم فوراً للواجهة
    st.session_state.messages.append({"role": "USER", "text": prompt})
    
    with st.spinner("🤖 Thinking and analyzing context..."):
        ai_response, final_model = execute_web_matrix(prompt, selected_model)
        
        if ai_response:
            st.session_state.messages.append({"role": "AI", "text": ai_response, "model": final_model.split('/')[-1]})
        else:
            st.session_state.messages.append({"role": "SYSTEM", "text": final_model})
            
    st.rerun()