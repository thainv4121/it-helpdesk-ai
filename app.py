import streamlit as st
from groq import Groq

st.set_page_config(page_title="VMT Helpdesk AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    /* Ẩn các thành phần thừa */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}

    /* Khung chat */
    .block-container {
        padding: 1.2rem 1rem 0.5rem 1rem !important;
        max-width: 100% !important;
    }

    /* Tiêu đề */
    h1 {
        font-size: 1.2rem !important;
        color: #1e293b !important;
        font-weight: 700 !important;
        margin-bottom: 0 !important;
    }

    /* Caption */
    .stCaptionContainer p {
        font-size: 12px !important;
        color: #64748b !important;
    }

    /* Tin nhắn user */
    [data-testid="stChatMessageContent"] {
        font-size: 13px !important;
        line-height: 1.55 !important;
    }

    /* Input chat */
    [data-testid="stChatInput"] textarea {
        font-size: 13px !important;
        border-radius: 12px !important;
        background: white !important;
    }

    /* Nền tin nhắn bot */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 8px !important;
        margin-bottom: 4px !important;
    }

    /* Nền tin nhắn user */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #eff6ff !important;
        border-radius: 12px !important;
        padding: 8px !important;
        margin-bottom: 4px !important;
    }

    /* Disclaimer box */
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

st.caption("Xin chào! Tôi có thể giúp gì cho bạn về IT Helpdesk?")
st.info("""
⚠️ **Lưu ý:** Các thông tin được cung cấp bởi AI mang tính tham khảo. 
Vui lòng kiểm tra lại trước khi thực hiện. 
Chúng tôi không chịu trách nhiệm về bất kỳ sự cố nào phát sinh từ việc áp dụng thông tin này.
""")

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
