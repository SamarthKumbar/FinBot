import requests

API_BASE = "http://localhost:8003"  # or your deployed URL

def login_user(email, password):
    response = requests.post(
        f"{API_BASE}/auth/login",
        json={"email": email, "password": password}  # ✅ use correct field names
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def register_user(email, full_name, password, role):
    payload = {
        "email": email,
        "full_name": full_name,
        "role": role,
        "password": password
    }
    print("Payload:", payload)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(f"{API_BASE}/auth/signup", json=payload, headers=headers)
    return response



def upload_pdf(file, token):
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": file}
    response = requests.post(f"{API_BASE}/rag/upload-pdf", files=files, headers=headers)
    return response.json()

def ask_question(question, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE}/rag/ask", json={"query": question}, headers=headers)
    return response.json()
