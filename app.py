import os
import subprocess
import time

def start_virtual_browser():
    print("🚀 Virtual Browser (vb) सुरू करत आहे...")

    # १. लपलेला डिस्प्ले (VNC Server) पासवर्ड सोबत चालू करणे
    print("➡️ [1/4] VNC Server (Password Protected) चालू करत आहे...")
    vnc_cmd = "Xvnc :0 -geometry 1024x768 -depth 16 -SecurityTypes VncAuth -PasswordFile /root/.vnc/passwd -BlacklistTimeout 0 -BlacklistThreshold 0 -localhost"
    subprocess.Popen(vnc_cmd, shell=True)
    time.sleep(2) # डिस्प्ले तयार होण्यासाठी २ सेकंद थांबणे

    # २. Window Manager चालू करणे (Mobile Rotation / Resize साठी)
    print("➡️ [2/4] Window Manager चालू करत आहे...")
    os.environ["DISPLAY"] = ":0"
    wm_cmd = "matchbox-window-manager -use_titlebar no"
    subprocess.Popen(wm_cmd, shell=True)
    time.sleep(1)

    # ३. डेस्कटॉपशिवाय थेट क्रोमियम (Chromium) चालू करणे
    print("➡️ [3/4] Chromium ब्राउझर चालू करत आहे...")
    os.environ["DISPLAY"] = ":0"
    chrome_cmd = (
        "chromium --no-sandbox "
        "--disable-dev-shm-usage "
        "--window-position=0,0 "
        "--window-size=1024,768 "
        "--start-maximized "
        "--user-data-dir=/tmp/chrome_profile"
    )
    subprocess.Popen(chrome_cmd, shell=True)

    # ४. वेब सर्व्हर चालू करणे (पोर्ट 8080 वर)
    print("➡️ [4/4] Web Server चालू करत आहे (Port: 8080)...")
    # हे /app/webroot मधील फाईल्स सर्व्ह करेल आणि VNC ला जोडेल
    websockify_cmd = "websockify --web /app/webroot 0.0.0.0:8080 127.0.0.1:5900"
    
    # स्क्रिप्ट चालू ठेवण्यासाठी websockify ला मुख्य प्रोसेस म्हणून रन करणे
    subprocess.run(websockify_cmd, shell=True)

if __name__ == "__main__":
    start_virtual_browser()
