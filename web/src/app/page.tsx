"use client";
import { useEffect, useState } from "react";
import Hero from '@/components/Hero';
import StatsStrip from '@/components/StatsStrip';
import InsightPanel from '@/components/InsightPanel';
import CollectionPanel from '@/components/CollectionPanel';
import { fetchCategorizedTransactions, fetchBudgetSuggestions } from '@/lib/api';

interface Transaction {
  transaction_id: string;
  description: string;
  amount: number;
  category: string;
}

interface BudgetSuggestion {
  category: string;
  current_spending: number;
  suggested_budget: number;
}

export default function HomePage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [budget, setBudget] = useState<BudgetSuggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [txRes, budRes] = await Promise.all([
          fetchCategorizedTransactions(),
          fetchBudgetSuggestions()
        ]);
        setTransactions(txRes);
        setBudget(budRes);
        setError(null);
      } catch (e) {
        setError('Failed to load data.');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <main className="flex flex-col gap-8 p-6 max-w-6xl mx-auto">
      <Hero />
      <StatsStrip />
      <InsightPanel
        loading={loading}
        error={error}
        transactions={transactions}
        budget={budget}
      />
      <CollectionPanel budget={budget} />
    </main>
  );
}
