import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Читаємо HTML-файл при запиті на головну сторінку
@app.get("/", response_class=HTMLResponse)
async def read_index():
    path = os.path.join("templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    # Налаштування порту для локального тестування
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)