"use client";
import clsx from 'clsx';

interface Transaction {
  transaction_id: string;
  description: string;
  amount: number;
  category: string;
}

export default function TransactionList({ transactions }: { transactions: Transaction[] }) {
  if (!transactions || transactions.length === 0) {
    return <p className="text-muted">No transactions to display.</p>;
  }

  return (
    <table className={clsx('w-full text-left')}>
      <thead className="bg-muted">
        <tr>
          <th className="p-2">Date</th>
          <th className="p-2">Description</th>
          <th className="p-2">Category</th>
          <th className="p-2">Amount</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-border">
        {transactions.map((t) => (
          <tr key={t.transaction_id} className="hover:bg-muted">
            <td className="p-2">—</td>
            <td className="p-2">{t.description}</td>
            <td className="p-2 capitalize">{t.category}</td>
            <td className="p-2 text-right ${t.amount < 0 ? 'text-warning' : 'text-success'}">
              ${t.amount.toFixed(2)}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
