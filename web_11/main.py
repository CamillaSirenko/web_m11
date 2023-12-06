from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.database.models import Contact
from src.database.db import get_db
from typing import List
import uvicorn




class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday:datetime
    additional_data: str = None

class ContactCreateUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday:datetime
    additional_data: str = None

app = FastAPI()


# CRUD операції
@app.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return ContactResponse(**db_contact.__dict__)

@app.get("/contacts/", response_model=List[ContactResponse])
def get_all_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactResponse(**contact.__dict__)

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return ContactResponse(**db_contact.__dict__)

@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return ContactResponse(**db_contact.__dict__)

@app.get("/search/", response_model=List[ContactResponse])
def search_contacts(query: str = Query(..., description="Search contacts by name, last name, or email"), db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()
    return [ContactResponse(**contact.__dict__) for contact in contacts]

from sqlalchemy import extract

@app.get("/upcoming_birthdays/", response_model=List[ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    contacts = db.query(Contact).filter(
        extract('month', Contact.birthday) == today.month,
        extract('day', Contact.birthday) >= today.day,
        extract('day', Contact.birthday) <= next_week.day
    ).all()

    return [ContactResponse(**contact.__dict__) for contact in contacts]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

