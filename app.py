import streamlit as st
import pandas as pd
from agent import extract_workflow_data_ai, send_actual_email
from database import init_db, save_log, get_all_logs, clear_all_logs

# Database Initialize
init_db()

st.set_page_config(page_title="Agentic Workflow Automator", page_icon="⚡", layout="wide")

st.title("⚡ Agentic Workflow Automator (Batch SaaS Engine)")
st.caption("AI-Powered Workflow Extraction, Bulk Data Processing & Database Persistence")

st.divider()

# Input Options Tab
st.subheader("1. Input Workflow Prompts")
input_option = st.radio("Choose Input Method:", ["✍️ Single Prompt Text", "📁 Upload Batch File (CSV/TXT)"],
                        horizontal=True)

prompts_to_process = []

if input_option == "✍️ Single Prompt Text":
    user_prompt = st.text_area(
        "Describe your workflow step:",
        placeholder="When a customer places an order, send a confirmation email and log transaction to database.",
        height=100
    )
    if user_prompt.strip():
        prompts_to_process.append(user_prompt.strip())

else:
    uploaded_file = st.file_uploader("Upload CSV or TXT file containing prompts", type=["csv", "txt"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df_file = pd.read_csv(uploaded_file)
            st.write("📋 Preview of uploaded data:")
            st.dataframe(df_file.head(3), use_container_width=True)
            text_col = st.selectbox("Select the column containing prompts:", df_file.columns)

            raw_list = df_file[text_col].dropna().astype(str).tolist()

            prompts_to_process = [
                item.strip() for item in raw_list
                if item.strip().lower() not in ["workflow_prompt", "prompt", "text", "prompts", text_col.lower()]
            ]
        else:
            content = uploaded_file.read().decode("utf-8")
            raw_lines = [line.strip() for line in content.split("\n") if line.strip()]

            prompts_to_process = [
                line for line in raw_lines
                if line.lower() not in ["workflow_prompt", "prompt", "text", "prompts"]
            ]

        st.info(f"📋 Found **{len(prompts_to_process)}** clean prompts to process (Header skipped).")

st.markdown("---")
st.subheader("2. Notification Settings")
recipient_email = st.text_input(
    "📧 Notification Email:",
    value="user@example.com",
    help="Enter the recipient email address where real-time execution alerts and batch summaries are routed."
)

if st.button("🚀 Process & Execute Pipeline", type="primary"):
    if prompts_to_process:
        st.subheader("🔄 Live Execution Pipeline")
        total_items = len(prompts_to_process)
        progress_bar = st.progress(0)

        processed_results = []

        for idx, prompt_text in enumerate(prompts_to_process):
            st.write(f"⚙️ **Processing Item {idx + 1}/{total_items}:** *\"{prompt_text[:50]}...\"*")

            # AI Extraction
            result = extract_workflow_data_ai(prompt_text)

            # Save to Database
            save_log(
                result["raw_text"],
                result["extracted_trigger"],
                result["extracted_action"],
                result["status"]
            )

            processed_results.append(result)
            progress_bar.progress(int((idx + 1) / total_items * 100))

        # Email Notification Execution Summary
        st.write("📧 **Dispatching Backend Execution Summary Alert...**")
        email_success, email_msg = send_actual_email(
            "system@airise.com", "", recipient_email,
            f"Batch Processed ({total_items} items)",
            "Logged all tasks to Database"
        )

        st.success(f"✅ Successfully processed {total_items} workflow prompt(s)!")
        st.toast(email_msg, icon="📧")
        st.info(email_msg)

        # Display Summary Table
        st.markdown("### 📋 Processed Output Summary")
        summary_df = pd.DataFrame(processed_results)
        st.dataframe(summary_df[["extracted_trigger", "extracted_action", "status"]], use_container_width=True)

    else:
        st.warning("Please provide a prompt or upload a file first.")

st.divider()

# Analytics Dashboard & Database Records
st.subheader("📊 Execution Logs & Analytics Dashboard")
df_logs = get_all_logs()

if not df_logs.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Executions Logged", len(df_logs))
    m2.metric("Database Storage", "SQLite Active")
    m3.metric("System Health", "100% Operational")

    st.dataframe(df_logs, use_container_width=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        csv_export = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Database Logs (CSV)",
            data=csv_export,
            file_name="workflow_execution_logs.csv",
            mime="text/csv"
        )

    with col2:
        if st.button("🗑️ Clear Database Logs", type="secondary"):
            clear_all_logs()
            st.success("Database logs cleared successfully!")
            st.rerun()
else:
    st.info("No logs found. Run your first pipeline above!")