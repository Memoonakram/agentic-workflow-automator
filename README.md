# ⚡ Agentic Workflow Automator (Batch SaaS Engine)

An end-to-end, AI-powered workflow extraction and batch processing engine. This application allows users to parse unstructured natural language automation prompts, process bulk CSV/TXT files, persist audit logs to a SQLite database, and simulate real-time email execution alerts.

---

## 🌟 Key Features

* **🤖 Natural Language Workflow Parsing:** Automatically identifies and extracts `Trigger` and `Action` elements from unstructured user prompts using regular expressions and AI rules.
* **📁 Bulk File Batch Processing:** Supports direct upload of `.csv` and `.txt` files to process dozens of workflow prompts simultaneously with automatic header filtering.
* **💾 Database Persistence (SQLite):** Real-time execution logging to a relational database, providing a full audit trail with downloadable CSV logs.
* **📊 Interactive Analytics Dashboard:** Displays system metrics, execution counts, and includes one-click database management (Log Clearance).
* **📧 Enterprise Notification Pipeline:** Built-in recipient notification layer designed for SendGrid/SMTP API integration with frictionless execution simulation.

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Data Processing:** [Pandas](https://pandas.pydata.org/)
* **Database:** SQLite3
* **Language:** Python 3.10+

---

## 🚀 Quick Start & Installation

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
