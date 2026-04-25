import joblib
import tkinter as tk
from gmail_scan import get_latest_emails

# 1. Load the ML files
try:
    model = joblib.load('phishing_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
except Exception as e:
    print(f"Error loading models: {e}")
    # Placeholder if files are missing just to let GUI open
    model = None
    vectorizer = None

def scan_inbox():
    # Clear the terminal-style output before a new scan
    output.delete("1.0", tk.END)
    output.insert(tk.END, "Scanning your Gmail inbox... Please wait.\n\n", "secure")
    root.update()

    try:
        # 2. Call the scan function
        emails = get_latest_emails(model, vectorizer)
        
        output.delete("1.0", tk.END) # Clear the "Scanning..." message

        for mail in emails:
            sender = mail["sender"]
            subject = mail["subject"]
            status = mail["result"]

            # 3. Insert and Color text
            output.insert(tk.END, f"Sender: {sender}\n")
            output.insert(tk.END, f"Subject: {subject}\n")
            
            if status == "Phishing":
                output.insert(tk.END, f"Result: 🚩 {status}\n", "danger")
                output.insert(tk.END, "-"*60 + "\n")
            else:
                output.insert(tk.END, f"Result: ✅ {status}\n", "secure")
                output.insert(tk.END, "-"*60 + "\n")
                
    except Exception as e:
        output.insert(tk.END, f"\n[!] Error during scan: {e}", "danger")

# --- GUI Setup ---
root = tk.Tk()
root.title("Phishing Detector V4")
root.geometry("900x700")
root.config(bg="#0a0a0a") # Deep black

# Header
tk.Label(
    root,
    text="PHISHING EMAIL DETECTOR V4",
    fg="cyan",
    bg="#0a0a0a",
    font=("Courier", 24, "bold")
).pack(pady=20)

# Scan Button
tk.Button(
    root,
    text="RUN GMAIL SCAN",
    command=scan_inbox,
    bg="#1db954", # Spotify Green
    fg="white",
    font=("Courier", 12, "bold"),
    width=25,
    relief="flat",
    cursor="hand2"
).pack(pady=10)

# Terminal Output Box
output = tk.Text(
    root, 
    width=100, 
    height=30, 
    bg="#121212", 
    fg="lime", 
    font=("Courier New", 10),
    padx=15,
    pady=15,
    borderwidth=0
)
output.pack(pady=10)

# Color Tags
output.tag_config("danger", foreground="#ff3333", font=("Courier New", 10, "bold"))
output.tag_config("secure", foreground="#00ff41")

root.mainloop()