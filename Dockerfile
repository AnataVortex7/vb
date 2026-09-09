FROM debian:bookworm-slim

WORKDIR /app

# 1. Install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tigervnc-standalone-server \
    chromium \
    novnc \
    websockify \
    python3 \
    matchbox-window-manager \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup VNC Password (AKSHAY)
RUN mkdir -p /root/.vnc && \
    echo "AKSHAY" | vncpasswd -f > /root/.vnc/passwd && \
    chmod 600 /root/.vnc/passwd

# 3. Setup Web Directories
RUN mkdir -p /app/webroot/vb && \
    cp -r /usr/share/novnc/* /app/webroot/vb/

# 4. Route '/' for Uptime Robot (Lightweight)
RUN echo "<html><body><h1>Uptime OK - Server Active</h1></body></html>" > /app/webroot/index.html

# 5. Route '/vb' for Browser
RUN echo "<html><head><meta http-equiv='refresh' content='0; url=vnc.html?autoconnect=true&resize=remote' /></head><body>Loading Browser...</body></html>" > /app/webroot/vb/index.html

# 6. Copy App Script
COPY app.py /app/app.py
RUN chmod +x /app/app.py

EXPOSE 8080

CMD ["python3", "/app/app.py"]
