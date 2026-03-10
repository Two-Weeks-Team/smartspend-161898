"use client";
import { useEffect, useState } from "react";
import { fetchBudgetSuggestions } from '@/lib/api';
import clsx from 'clsx';

interface BudgetSuggestion {
  category: string;
  current_spending: number;
  suggested_budget: number;
}

export default function StatsStrip() {
  const [totalSpend, setTotalSpend] = useState(0);
  const [suggestedSavings, setSuggestedSavings] = useState(0);

  useEffect(() => {
    async function load() {
      try {
        const budget: BudgetSuggestion[] = await fetchBudgetSuggestions();
        const spend = budget.reduce((sum, b) => sum + b.current_spending, 0);
        const suggested = budget.reduce((sum, b) => sum + (b.suggested_budget - b.current_spending), 0);
        setTotalSpend(spend);
        setSuggestedSavings(suggested > 0 ? suggested : 0);
      } catch {
        // ignore for demo
      }
    }
    load();
  }, []);

  return (
    <div className="flex gap-4 justify-center">
      <div className={clsx('card w-48 text-center')}>
        <h3 className="text-sm font-medium text-muted mb-1">Total Spend</h3>
        <p className="text-2xl font-bold text-primary">${totalSpend.toLocaleString()}</p>
      </div>
      <div className={clsx('card w-48 text-center')}>
        <h3 className="text-sm font-medium text-muted mb-1">Potential Savings</h3>
        <p className="text-2xl font-bold text-success">${suggestedSavings.toLocaleString()}</p>
      </div>
      <div className={clsx('card w-48 text-center')}>
        <h3 className="text-sm font-medium text-muted mb-1">Financial Health</h3>
        <p className="text-2xl font-bold text-accent">Good</p>
      </div>
    </div>
  );
}
