## ℹ️ Overview

This is a weather api, used to pull data from visual crossing.

Built to practice:
- FastAPI endpoint design
- Working with API keys 
- Redis caching with a configurable TTL


## 🚀 Usage

Run the server locally:

```bash
uvicorn app.main:app --reload
```
You can use the built in swagger ui by just adding a /docs to the end of the url
http://127.0.0.1:8000/docs



## ⬇️ Installation

To install the dependencies:
make sure you have the virtual enviornment activated

```bash
python -m venv .venv
source .venv/bin/activate
```

Dependencies:
```bash
pip install -r requirements.txt
```
For the .env include:
- VISUAL_CROSSING_API_KEY=your_api_key_here
- REDIS_URL=redis://localhost:6379/0
- CACHE_SECONDS=3600