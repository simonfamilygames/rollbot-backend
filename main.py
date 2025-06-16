from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🎉 RollBot 后端已启动成功！"}



# === 以下为 Bitget 子账户资产接口 ===
import base64
from fastapi import HTTPException

bitget_api_key = "bg_0d0cc8972fd591eae6cfe38b53b1fedd"
bitget_secret = "711da70af63df1a65dcc7dc06fc99d71111c5c2860d0c51e5d96104d1124e5d4"
bitget_passphrase = "seven2025"
bitget_uid = "1197204595"
bitget_base_url = "https://api.bitget.com"

def sign_bitget(ts, method, path, query=""):
    prehash = ts + method + path + query
    return base64.b64encode(hmac.new(bitget_secret.encode(), prehash.encode(), hashlib.sha256).digest()).decode()

@app.get("/subassets")
def subassets():
    ts = str(int(time.time()*1000))
    path = "/api/v2/broker/account/subaccount-spot-assets"
    query = f"?subUid={bitget_uid}"
    signature = sign_bitget(ts, "GET", path, query)
    resp = requests.get(bitget_base_url + path, params={"subUid": bitget_uid}, headers={
        "ACCESS-KEY": bitget_api_key,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": ts,
        "ACCESS-PASSPHRASE": bitget_passphrase,
        "Content-Type": "application/json"
    })
    data = resp.json()
    if data.get("code") != "00000":
        raise HTTPException(status_code=400, detail=data)
    return data["data"]