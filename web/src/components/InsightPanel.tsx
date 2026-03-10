"use client";
import { useEffect, useState } from "react";
import { detectAnomalies } from '@/lib/api';
import clsx from 'clsx';

interface Anomaly {
  transaction_id: string;
  amount: number;
  anomaly_score: number;
}

interface InsightPanelProps {
  loading: boolean;
  error: string | null;
  transactions: any[]; // not displayed directly here
  budget: any[]; // not displayed directly here
}

export default function InsightPanel({ loading, error }: InsightPanelProps) {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loadingAnomalies, setLoadingAnomalies] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await detectAnomalies();
        setAnomalies(data);
      } catch {
        setAnomalies([]);
      } finally {
        setLoadingAnomalies(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <section className={clsx('card')}>Loading insights...</section>
    );
  }

  if (error) {
    return (
      <section className={clsx('card text-warning')}>Error: {error}</section>
    );
  }

  return (
    <section className={clsx('card')}>
      <h2 className="text-xl font-semibold mb-4 text-primary">AI Insights</h2>
      {loadingAnomalies ? (
        <p>Analyzing for anomalies…</p>
      ) : anomalies.length > 0 ? (
        <div className="space-y-2">
          {anomalies.slice(0, 3).map((a) => (
            <div key={a.transaction_id} className="p-2 bg-muted rounded-radius">
              <p className="font-medium">⚠️ Transaction ${a.amount.toFixed(2)} flagged (score {a.anomaly_score.toFixed(2)})</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-success">No unusual activity detected.</p>
      )}
    </section>
  );
}
