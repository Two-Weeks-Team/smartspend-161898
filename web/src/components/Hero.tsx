"use client";
import { useState } from "react";
import { CloudArrowUpIcon } from '@heroicons/react/24/outline';
import clsx from 'clsx';

export default function Hero() {
  const [fileName, setFileName] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFileName(e.target.files[0].name);
      // In a real app, you would upload the file here.
    }
  };

  return (
    <section className="text-center py-12">
      <h1 className="text-4xl md:text-5xl font-bold mb-4 text-primary">
        SmartSpend
      </h1>
      <p className="text-lg md:text-xl text-muted mb-6">
        Your Intelligent Financial Guide.
      </p>
      <div className="flex flex-col items-center gap-4">
        <label
          htmlFor="file-upload"
          className={clsx(
            "cursor-pointer flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-radius hover:bg-primary/90"
          )}
        >
          <CloudArrowUpIcon className="w-5 h-5" />
          {fileName ? `Selected: ${fileName}` : 'Upload CSV'}
          <input
            id="file-upload"
            type="file"
            accept=".csv"
            className="hidden"
            onChange={handleFileChange}
          />
        </label>
        <p className="text-sm text-muted">
          Securely import transactions from your bank or a CSV file.
        </p>
      </div>
    </section>
  );
}
