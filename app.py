import streamlit as st
from groq import Groq

st.set_page_config(page_title="VMT Helpdesk AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}

    .stApp {
        background-color: #f8fafc !important;
    }

    .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
        color: #1e293b !important;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #1e293b !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 8px !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #eff6ff !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }

    [data-testid="stChatMessageContent"] p {
        color: #1e293b !important;
        font-size: 13px !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: white !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }

    [data-testid="stChatInput"] button {
        background-color: #2563eb !important;
        border-radius: 8px !important;
    }

    /* Vùng nền input phía dưới */
    .stChatInput,
    .stChatInput > div,
    .stChatInput > div > div,
    section[data-testid="stBottom"],
    section[data-testid="stBottom"] > div,
    section[data-testid="stBottom"] > div > div {
        background-color: white !important;
        background: white !important;
    }

    .contact-box {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 10px 12px;
        margin-top: 6px;
        font-size: 12px;
        color: #1e40af;
    }
    .contact-box p {
        margin: 0 0 8px 0 !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        color: #1e40af !important;
    }
    .contact-btn {
        display: inline-block;
        background: #2563eb;
        color: white !important;
        padding: 6px 14px;
        border-radius: 8px;
        text-decoration: none !important;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---- URL trang liên hệ----
CONTACT_URL = "https://kmt.com.vn/lien-he/"

CONTACT_HTML = f"""
<div class="contact-box">
    <p>💬 Vẫn chưa giải quyết được? Đội ngũ IT của chúng tôi luôn sẵn sàng hỗ trợ bạn!</p>
    <a href="{CONTACT_URL}" target="_blank" class="contact-btn"> Liên hệ hỗ trợ ngay</a>
</div>
"""

st.markdown("""
<div style="background:#fefce8; border:1px solid #fcd34d; border-radius:8px; 
padding:6px 10px; font-size:11px; color:#92400e; line-height:1.4;">
⚠️ LƯU Ý: Các thông tin được cung cấp bởi AI mang tính tham khảo.
Chúng tôi không chịu trách nhiệm về bất kỳ sự cố nào phát sinh.
</div>
""", unsafe_allow_html=True)

st.write("#### Xin chào! Tôi có thể giúp gì cho bạn về IT Helpdesk?")

SYSTEM_PROMPT = """Bạn là chuyên gia IT Helpdesk với 10 năm kinh nghiệm.
Hỗ trợ người dùng về: lỗi máy tính, Windows/Mac/Linux, mạng WiFi/VPN,
email/Office 365, bảo mật/virus, máy in, tài khoản/mật khẩu, phần mềm văn phòng.
Trả lời bằng tiếng Việt, ngắn gọn, rõ ràng, theo từng bước đánh số nếu cần.
Cuối mỗi câu trả lời, thêm dòng in nghiêng: '_Lưu ý: Kiểm tra lại thông tin hoặc liên hệ hỗ trợ trước khi thực hiện._"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Hiển thị nút liên hệ sau mỗi câu trả lời của bot
        if msg["role"] == "assistant":
            st.markdown(CONTACT_HTML, unsafe_allow_html=True)

if prompt := st.chat_input("Bạn cần hỗ trợ gì về vấn đề IT?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages]
                ],
                max_tokens=1024
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.markdown(CONTACT_HTML, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer})
