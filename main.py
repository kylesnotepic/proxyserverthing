from flask import Flask, request, Response
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def is_browser_request():
    ua = request.headers.get("User-Agent", "").lower()
    return any(x in ua for x in ["mozilla", "chrome", "safari", "edge", "opera", "firefox"])

@app.route("/proxy")
def proxy():
    # block browser visits
    # if is_browser_request():
    #     return "browser access not allowed", 403
    username = request.args.get("username")
    job_id = request.args.get("job_id")

    if not username or not job_id:
        return "Missing username param", 400
    try:
        r = requests.post(
            url=os.getenv("WEBHOOK_URL"),
            headers={k: v for k, v in request.headers if k.lower() not in ["host", "user-agent"]},
            data={"content": f"{username} is calling for a mod in https://www.roblox.com/games/start?placeId=113067621040677&jobId={job_id}."},
            stream=True,
            timeout=15
        )
        excluded = ['content-encoding','transfer-encoding','connection']
        headers = [(n,v) for (n,v) in r.raw.headers.items() if n.lower() not in excluded]
        return Response(r.raw, status=r.status_code, headers=headers)
    except Exception as e:
        return f"proxy error {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
