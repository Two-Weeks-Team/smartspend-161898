from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from models import SessionLocal, Transaction, Category, User, Budget
from ai_service import call_inference

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# AI‑Powered expense categorization
# ---------------------------------------------------------------------------

@router.get("/api/transactions/categorize")
async def categorize_transactions(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    # Fetch a small batch of uncategorized transactions for demo purposes
    uncategorized = (
        db.query(Transaction)
        .filter(Transaction.category_id.is_(None))
        .limit(10)
        .all()
    )

    # If nothing needs categorization, just return existing data
    if not uncategorized:
        all_tx = db.query(Transaction).all()
        return [
            {
                "transaction_id": str(tx.id),
                "description": tx.description,
                "amount": float(tx.amount),
                "category": tx.category.name if tx.category else None,
            }
            for tx in all_tx
        ]

    # Prepare a prompt for the LLM – keep it short for the demo
    descriptions = [tx.description or "" for tx in uncategorized]
    prompt = (
        "Assign a concise category name to each of the following transaction descriptions. "
        "Return a JSON array where each object has 'description' and 'category'.\n"
        + "\n".join(f"- {d}" for d in descriptions)
    )
    messages = [{"role": "user", "content": prompt}]

    # Call the AI service (fallback handled inside the helper)
    ai_response = await call_inference(messages)

    # Expecting a list of {"description": ..., "category": ...}
    if isinstance(ai_response, list):
        for item in ai_response:
            descr = item.get("description")
            cat_name = item.get("category")
            if not descr or not cat_name:
                continue
            # Find the matching transaction object
            tx = next((t for t in uncategorized if (t.description or "") == descr), None)
            if not tx:
                continue
            # Find or create the Category
            cat = db.query(Category).filter(Category.name == cat_name).first()
            if not cat:
                cat = Category(name=cat_name, type="expense", is_custom=True)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            tx.category_id = cat.id
        db.commit()

    # Return full list after (re)categorization
    all_tx = db.query(Transaction).all()
    return [
        {
            "transaction_id": str(tx.id),
            "description": tx.description,
            "amount": float(tx.amount),
            "category": tx.category.name if tx.category else None,
        }
        for tx in all_tx
    ]

# ---------------------------------------------------------------------------
# Smart budget suggestions (AI‑driven)
# ---------------------------------------------------------------------------

@router.get("/api/budget/suggestions")
async def budget_suggestions(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    # Simple aggregation: total spending per category (negative amounts are expenses)
    from sqlalchemy import func

    aggregates = (
        db.query(Category.name, func.sum(Transaction.amount).label("total"))
        .join(Transaction, Transaction.category_id == Category.id)
        .group_by(Category.name)
        .all()
    )

    suggestions = []
    for cat_name, total in aggregates:
        current_spending = float(total) if total else 0.0
        # Very naive suggestion – give a 10% larger budget for positive cash flow
        suggested_budget = round(abs(current_spending) * 1.10, 2)
        suggestions.append(
            {
                "category": cat_name,
                "current_spending": current_spending,
                "suggested_budget": suggested_budget,
            }
        )
    return suggestions

# ---------------------------------------------------------------------------
# Anomaly detection (AI‑powered placeholder)
# ---------------------------------------------------------------------------

@router.get("/api/anomalies")
async def detect_anomalies(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    # For demo we mark any transaction > $1000 as anomalous – real logic would call AI
    anomalies = (
        db.query(Transaction)
        .filter(Transaction.amount > 1000)
        .all()
    )
    result = []
    for tx in anomalies:
        result.append(
            {
                "transaction_id": str(tx.id),
                "amount": float(tx.amount),
                "anomaly_score": 0.95,
            }
        )
    return result
