import streamlit as st
from groq import Groq

st.set_page_config(page_title="VMT Helpdesk AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}

    .contact-box {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        padding: 12px 16px;
        margin-top: 8px;
        font-size: 14px;
        color: #1e40af;
    }
    .contact-box p {
        margin: 0 0 8px 0;
        font-weight: 500;
    }
    .contact-btn {
        display: inline-block;
        background: #2563eb;
        color: white !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none !important;
        font-size: 13px;
        font-weight: 600;
        transition: background 0.2s;
    }
    .contact-btn:hover {
        background: #1d4ed8;
        color: white !important;
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
