"use client";
export default function EmptyState({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center py-12">
      <p className="text-muted text-lg">{message}</p>
    </div>
  );
}
