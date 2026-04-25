import tkinter as tk
from gmail_scan import get_latest_emails


def scan_inbox():

    output.delete("1.0", tk.END)

    emails = get_latest_emails()

    for mail in emails:

        sender = mail["sender"]
        subject = mail["subject"]

        score = 0

        if "verify" in subject.lower():
            score += 2

        if "urgent" in subject.lower():
            score += 2

        if "bank" in subject.lower():
            score += 2

        if score >= 3:
            status = "⚠️ Suspicious"
        else:
            status = "Safe ✅"

        output.insert(
            tk.END,
            f"Sender: {sender}\nSubject: {subject}\nResult: {status}\n\n"
        )


root = tk.Tk()
root.title("Phishing Detector V4 Gmail Scanner")
root.geometry("900x700")
root.config(bg="black")

tk.Label(
    root,
    text="Phishing Email Detector V4",
    fg="cyan",
    bg="black",
    font=("Arial", 20, "bold")
).pack(pady=10)

tk.Button(
    root,
    text="Scan Gmail Inbox",
    command=scan_inbox,
    bg="green",
    fg="white",
    width=20
).pack(pady=10)

output = tk.Text(root, width=110, height=35, bg="black", fg="lime")
output.pack()

root.mainloop()
