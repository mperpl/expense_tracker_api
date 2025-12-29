from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select
from database import DB_ASYNC_SESSION, async_create_db_tables, async_engine
import models
import schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    await async_create_db_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return "Expense Tracker API"


@app.get("/expense", response_model=list[schemas.Expense], status_code=status.HTTP_200_OK)
async def get_all(db: DB_ASYNC_SESSION):
    result = await db.execute(select(models.Expense))
    return result.scalars().all()


@app.get("/expense/filter/{category}", response_model=list[schemas.Expense], status_code=status.HTTP_200_OK)
async def get_by_category(category: schemas.CATEGORY, db: DB_ASYNC_SESSION):
    result = await db.execute(
        select(models.Expense).where(models.Expense.category == category)
    )
    return result.scalars().all()


@app.get("/expense/{id}", response_model=schemas.Expense, status_code=status.HTTP_200_OK)
async def get_by_id(id: int, db: DB_ASYNC_SESSION):
    expense = await db.get(models.Expense, id)
    if expense:
        return expense
    raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")

@app.post('/expense', response_model=schemas.Expense, status_code=status.HTTP_201_CREATED)
async def new(request: schemas.ExpenseBase, db: DB_ASYNC_SESSION):
    new_expense = models.Expense(amount=request.amount, category=request.category, description=request.description, expense_date=request.expense_date)
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense

@app.put("/expense/{id}", response_model=schemas.Expense, status_code=status.HTTP_200_OK)
async def correct(id: int, request: schemas.ExpenseBase, db: DB_ASYNC_SESSION):
    expense = await db.get(models.Expense, id)
    if not expense:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")

    expense.amount = request.amount
    expense.category = request.category
    expense.description = request.description
    expense.expense_date = request.expense_date

    await db.commit()
    await db.refresh(expense)
    return expense


@app.delete("/expense/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: DB_ASYNC_SESSION):
    expense = await db.get(models.Expense, id)
    if not expense:
        raise HTTPException(404, "not found")

    await db.delete(expense)
    await db.commit()