"use client";
interface StatePanelProps {
  loading: boolean;
  error?: string;
  children: React.ReactNode;
}
export default function StatePanel({ loading, error, children }: StatePanelProps) {
  if (loading) {
    return <p className="text-muted">Loading…</p>;
  }
  if (error) {
    return <p className="text-warning">Error: {error}</p>;
  }
  return <>{children}</>;
}
