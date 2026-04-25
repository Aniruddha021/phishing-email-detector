import re

def detect_phishing(email_text, sender):

    score = 0
    reasons = []

    suspicious_words = [
        "urgent", "verify", "click now",
        "winner", "prize", "free money",
        "password reset", "limited time"
    ]

    for word in suspicious_words:
        if word.lower() in email_text.lower():
            score += 1
            reasons.append(f"Suspicious phrase found: {word}")

    links = re.findall(r'https?://\S+|www\.\S+', email_text)
    if links:
        score += 2
        reasons.append("Contains clickable link(s)")

    if sum(1 for c in email_text if c.isupper()) > 15:
        score += 1
        reasons.append("Too many capital letters")

    suspicious_domains = ["paypa1.com", "amaz0n.com"]

    for domain in suspicious_domains:
        if domain in sender.lower():
            score += 3
            reasons.append("Fake sender domain detected")

    if score >= 5:
        result = "Likely Phishing 🚨"
    elif score >= 3:
        result = "Suspicious ⚠️"
    else:
        result = "Safe ✅"

    return result, reasons


sender = input("Enter sender email: ")
email_text = input("Paste email message:\n")

result, reasons = detect_phishing(email_text, sender)

print("\nResult:", result)

for r in reasons:
    print("-", r)
