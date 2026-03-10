"use client";
import clsx from 'clsx';

interface BudgetSuggestion {
  category: string;
  current_spending: number;
  suggested_budget: number;
}

interface CollectionPanelProps {
  budget: BudgetSuggestion[];
}

export default function CollectionPanel({ budget }: CollectionPanelProps) {
  if (!budget || budget.length === 0) {
    return (
      <section className={clsx('card')}>No budget suggestions yet. Upload transactions to get recommendations.</section>
    );
  }

  return (
    <section className={clsx('card')}>
      <h2 className="text-xl font-semibold mb-4 text-primary">Smart Budget Suggestions</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {budget.map((b) => (
          <div key={b.category} className="p-4 bg-muted rounded-radius">
            <h3 className="font-medium text-foreground mb-1">{b.category}</h3>
            <p className="text-sm text-muted">Current: ${b.current_spending.toLocaleString()}</p>
            <p className="text-sm text-success">Suggested: ${b.suggested_budget.toLocaleString()}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
