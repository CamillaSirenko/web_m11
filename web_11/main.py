from fastapi import FastAPI
import uvicorn
from src.routes.contacts import router as contacts_router
from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactCreateUpdate, ContactResponse


app = FastAPI()

 
app.include_router(contacts_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
