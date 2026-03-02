import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="IT Helpdesk AI",
    page_icon="🖥️",
    layout="centered"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("🖥️ IT Helpdesk AI")
st.caption("Xin chào! Tôi có thể giúp gì cho bạn về IT hôm nay?")

SYSTEM_PROMPT = """Bạn là chuyên gia IT Helpdesk với 10 năm kinh nghiệm.
Hỗ trợ người dùng về:
- Lỗi máy tính, Windows/Mac/Linux
- Mạng, WiFi, VPN, không kết nối được internet
- Email, Office 365, Google Workspace
- Bảo mật, virus, malware
- Máy in, thiết bị ngoại vi
- Tài khoản, mật khẩu, phân quyền
- Phần mềm văn phòng thông dụng

Trả lời bằng tiếng Việt, ngắn gọn, rõ ràng, theo từng bước đánh số nếu cần."""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Nhập câu hỏi IT của bạn..."):
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

    st.session_state.messages.append({"role": "assistant", "content": answer})
```

---

### File `requirements.txt`
```
streamlit
groq
