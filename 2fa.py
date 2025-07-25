import pyotp
import qrcode
import getpass
import subprocess

# Simulated user database (username: password)
USER_DB = {
    'manzil': 'secure123'
}

# Generate a TOTP secret for the user (in real applications, store securely)
user_secret = pyotp.random_base32()

def open_qr_image(file_path):
    try:
        # On Linux, xdg-open opens the file with the default app
        subprocess.run(["xdg-open", file_path], check=True)
    except Exception as e:
        print(f"Unable to open QR code automatically. Please open '{file_path}' manually.")

def generate_qr(username, secret):
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="Py2FA App")
    qr_img = qrcode.make(totp_uri)
    file_path = "2fa_qr.png"
    qr_img.save(file_path)
    print(f"✅ QR code saved as '{file_path}'. Attempting to open it now...")
    open_qr_image(file_path)

def login():
    banner = """
\033[1;34m
██████████  █████████   ██████████  ███████████  ███████████  ███     ███  ███    ███  
███         ███         ███    ███  ███     ███  ███████████  ███     ███  ████  ████  
█████████   ███         █████████   ███     ███      ███      ███     ███  ██ ████ ██  
      ███   ███         ███   ███   ███     ███      ███      ███     ███  ██  ██  ██  
      ███   ██████████  ███    ███  ███     ███      ███      ███     ███  ██      ██  
█████████               ███     ███ ███████████      ███      ███████████  ██      ██  
\033[1;31mv1\033[1;34m

  Coded by Scrotum
  github: https://github.com/scrotum11
\033[0m
"""
    print(banner)
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    if username in USER_DB and USER_DB[username] == password:
        print("✅ Password correct.")
        print("🔐 Setting up 2FA...")

        generate_qr(username, user_secret)
        input("Press Enter after scanning the QR code with your authenticator app...")

        totp = pyotp.TOTP(user_secret)
        code = input("Enter the 6-digit 2FA code: ")

        if totp.verify(code):
            print("✅ 2FA verification successful. You are logged in.")
        else:
            print("❌ Invalid 2FA code. Access denied.")
    else:
        print("❌ Invalid username or password.")

if __name__ == "__main__":
    login()
