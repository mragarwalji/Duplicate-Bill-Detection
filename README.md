# 📄 Duplicate Bill Detection (HTML + Python Flask)

A simple and effective system to automatically detect **duplicate bill submissions** using file hashing.  
This project helps prevent repeated uploads caused by mistakes, fraud, or clerical errors.

---

## 🚀 Overview
Duplicate invoices create major issues in finance departments, such as:
- Extra payments  
- Fraud attempts  
- Manual verification workload  
- Confusion in billing records  

This project provides an automated solution using Flask. When a user uploads a bill, the system checks whether the **same file was uploaded before** and alerts the user instantly.

---

## 🧠 How It Works
This project uses **file hashing (SHA256)** to detect duplicates.

Workflow:
1. User uploads a bill file (.jpg, .png, .pdf, etc.)
2. Flask backend generates a **unique hash** of the file.
3. System checks the hash against stored records.
4. If the hash already exists → ❗ **Duplicate Bill Detected**  
5. If not → ✔ **Bill Saved Successfully**

---

## 🛠 Tech Stack
### **Frontend**
- HTML  
- CSS  
- JavaScript (optional)

### **Backend**
- Python  
- Flask Framework  
- SHA256 Hashing

---

## 📁 Project Structure
Duplicate-Bill-Detection/
│── app.py
│── static/
│ └── index.html
│── uploads/
│── README.md
---

## ▶️ Installation & Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/Duplicate-Bill-Detection.git
cd Duplicate-Bill-Detection

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

python app.py

### 1️⃣ Install Dependencies
```bash
pip install flask
