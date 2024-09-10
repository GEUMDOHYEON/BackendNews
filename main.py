from fastapi import FastAPI
from routers import users, news

app = FastAPI()

app.include_router(users.router)
app.include_router(news.router)

@app.get("/")
def helloWorld():
  return {"HELLO WORLD"}

@app.get("/test")
def test():
  return {"test"}