from dotenv import load_dotenv
from fastapi import FastAPI
import modules.bars as bars

load_dotenv()

app = FastAPI()
app.include_router(bars.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
