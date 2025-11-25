from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, update, delete
from database import get_db, create_db_tables
from sqlalchemy.orm import Session
import models
import schemas

create_db_tables()
app = FastAPI()

@app.get('/')
def root():
    return 'Expense Tracker API'

@app.get('/expense', response_model=list[schemas.Expense])
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()

@app.get('/expense/filter/{category}', response_model=list[schemas.Expense])
def get_by_category(category: schemas.CATEGORY, db: Session = Depends(get_db)):
    return db.scalars(
        select(models.Expense).where(models.Expense.category == category)
        ).all()

@app.get('/expense/{id}', response_model=schemas.Expense)
def get_by_id(id: int, db: Session = Depends(get_db)):
    expense = db.get(models.Expense, id)

    if expense:
        return expense
    raise HTTPException(404, 'not found')

@app.post('/expense', response_model=schemas.Expense)
def new(request: schemas.ExpenseBase, db: Session = Depends(get_db)):
    new_expense = models.Expense(amount=request.amount, category=request.category, description=request.description, expense_date=request.expense_date)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.put('/expense/{id}', response_model=schemas.Expense)
def correct(id:int, request: schemas.ExpenseBase, db: Session = Depends(get_db)):
    expense = db.get(models.Expense, id)

    if expense:
        stmt = update(models.Expense).where(models.Expense.id == id).values(amount=request.amount, category=request.category, description=request.description, expense_date=request.expense_date)
        db.execute(stmt)
        db.commit()
        db.refresh(expense)
        return expense
    else:
        raise HTTPException(404, 'not found')

@app.delete('/expense/{id}', response_model=schemas.Expense)
def delete(id:int, db: Session = Depends(get_db)):
    expense = db.get(models.Expense, id)

    if expense:
        db.delete(expense)
        db.commit()
        return expense
    else:
        raise HTTPException(404, 'not found')