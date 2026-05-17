import os
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Ендпоінт-проксі для отримання даних з API НБУ без помилок CORS у браузері
@app.get("/api/nbu-rates")
async def get_nbu_rates():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://bank.gov.ua/NBUStatService/v1/statist/exchange?json',
                timeout=5.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"НБУ повернув статус {response.status_code}", "fallback": True}
    except Exception as e:
        return {"error": str(e), "fallback": True}

# Додаємо підтримку методів GET та HEAD для кореневого маршруту (виправляє помилку 405 на Render)
@app.get("/", response_class=HTMLResponse)
@app.head("/", response_class=HTMLResponse)
async def read_index():
    path = os.path.join("templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)