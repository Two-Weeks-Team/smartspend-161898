export async function fetchCategorizedTransactions() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || ''}/api/transactions/categorize`);
  if (!res.ok) {
    throw new Error('Failed to fetch transactions');
  }
  return res.json();
}

export async function fetchBudgetSuggestions() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || ''}/api/budget/suggestions`);
  if (!res.ok) {
    throw new Error('Failed to fetch budget suggestions');
  }
  return res.json();
}

export async function detectAnomalies() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || ''}/api/anomalies`);
  if (!res.ok) {
    throw new Error('Failed to fetch anomalies');
  }
  return res.json();
}
