import os
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

start_time = time.time()

def get_uptime():
    seconds = int(time.time() - start_time)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence standard HTTP access logging to keep stdout clean
        pass

    def do_GET(self):
        if self.path in ['/health', '/ping', '/status']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response = '{"status":"ok","bot":"running","uptime":"' + get_uptime() + '"}'
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            uptime_str = get_uptime()
            port_val = os.getenv("PORT", "8080")
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Bot Status - Active</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0b0f19;
            color: #f3f4f6;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow-x: hidden;
        }}
        .bg-glow {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, rgba(147, 51, 234, 0.08) 50%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }}
        .card {{
            position: relative;
            z-index: 1;
            background: rgba(17, 24, 39, 0.7);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
        }}
        .icon-container {{
            width: 80px;
            height: 80px;
            margin: 0 auto 24px;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(147, 51, 234, 0.2));
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 0 15px rgba(59, 130, 246, 0.2);
        }}
        .icon-container svg {{
            width: 42px;
            height: 42px;
            fill: #3b82f6;
        }}
        h1 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
            letter-spacing: -0.025em;
        }}
        p.subtitle {{
            font-size: 0.9rem;
            color: #9ca3af;
            margin-bottom: 28px;
        }}
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #10b981;
            padding: 8px 18px;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 32px;
        }}
        .pulse {{
            width: 10px;
            height: 10px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse-animation 2s infinite;
        }}
        @keyframes pulse-animation {{
            0% {{
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }}
            70% {{
                box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
            }}
            100% {{
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }}
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            background: rgba(31, 41, 55, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 18px;
            border-radius: 16px;
            margin-bottom: 24px;
        }}
        .stat-item {{
            text-align: left;
        }}
        .stat-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #6b7280;
            margin-bottom: 4px;
        }}
        .stat-value {{
            font-size: 0.95rem;
            font-weight: 600;
            color: #e5e7eb;
        }}
        .footer {{
            font-size: 0.8rem;
            color: #6b7280;
        }}
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="card">
        <div class="icon-container">
            <svg viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.12.02-1.96 1.25-5.54 3.69-.52.36-1 .53-1.42.52-.47-.01-1.37-.26-2.03-.48-.82-.27-1.47-.42-1.42-.88.03-.25.38-.51 1.07-.78 4.18-1.82 6.97-3.02 8.37-3.61 3.98-1.66 4.81-1.95 5.35-1.96.12 0 .38.03.55.17.14.12.18.28.2.45-.01.07.01.24 0 .38z"/>
            </svg>
        </div>
        <h1>Telegram Bot</h1>
        <p class="subtitle">Clever Cloud Container Status</p>
        
        <div class="badge">
            <span class="pulse"></span>
            <span>SYSTEM ONLINE</span>
        </div>
        
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Uptime</div>
                <div class="stat-value">{uptime_str}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Port</div>
                <div class="stat-value">{port_val}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Health Probe</div>
                <div class="stat-value">/health</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Environment</div>
                <div class="stat-value">Clever Cloud</div>
            </div>
        </div>
        
        <div class="footer">
            Bot is running 24/7 on Pyrogram &amp; Clever Cloud
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))

def start_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logging.info(f"Web health check server started on 0.0.0.0:{port}")
    return server

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    srv = start_web_server()
    print(f"Server listening on port {os.getenv('PORT', 8080)}... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server.")
