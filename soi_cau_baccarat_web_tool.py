
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tool Soi Cầu Baccarat", layout="centered")

st.title("🔍 Tool Soi Cầu Baccarat")

# Giới thiệu
st.markdown("Nhập kết quả các ván Baccarat (P = Player, B = Banker) để phân tích soi cầu.")

# Nhập dữ liệu
results_input = st.text_area("Nhập kết quả (cách nhau bằng dấu phẩy hoặc xuống dòng)", 
                             placeholder="Ví dụ: P, B, P, P, B, B...")

if results_input:
    # Xử lý dữ liệu đầu vào
    raw_results = [x.strip().upper() for x in results_input.replace("\n", ",").split(",") if x.strip().upper() in ["P", "B"]]

    if raw_results:
        df = pd.DataFrame({
            'Ván': range(1, len(raw_results) + 1),
            'Kết quả': raw_results
        })

        # Phân tích chuỗi soi cầu
        df['Chuỗi'] = (df['Kết quả'] != df['Kết quả'].shift()).cumsum()
        df['Lặp lại'] = df.groupby('Chuỗi').cumcount() + 1

        st.subheader("📋 Bảng Kết Quả Phân Tích")
        st.dataframe(df, use_container_width=True)

        # Gợi ý cược đơn giản
        last_row = df.iloc[-1]
        if last_row['Lặp lại'] >= 3:
            suggestion = f"🔥 Cầu bệt {last_row['Kết quả']} đang chạy ({last_row['Lặp lại']} lần) → Có thể tiếp tục theo!"
        elif last_row['Lặp lại'] == 1 and df.iloc[-2]['Lặp lại'] == 1:
            suggestion = "🔁 Cầu 1-1 đang xuất hiện → Cược xen kẽ!"
        else:
            suggestion = "🤔 Không có cầu rõ ràng → Cân nhắc dừng hoặc chờ thêm kết quả."

        st.subheader("🧠 Gợi ý cược")
        st.info(suggestion)
    else:
        st.warning("Không có kết quả hợp lệ để phân tích.")
