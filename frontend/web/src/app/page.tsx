'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { generateResearch } from '@/lib/api';
import { ResearchResponse } from '@/lib/types';
import { ResearchForm } from '@/components/research/ResearchForm';
import { ResearchReport } from '@/components/research/ResearchReport';
import { ReportSkeleton } from '@/components/research/ReportSkeleton';

export default function Dashboard() {
  const [currentTopic, setCurrentTopic] = useState('');
  const [data, setData] = useState<ResearchResponse | null>(null);

  const mutation = useMutation({
    mutationFn: (topic: string) => generateResearch({ topic, depth: 'medium' }),
    onSuccess: (res) => {
      setData(res);
    },
  });

  const handleSearch = (topic: string) => {
    setCurrentTopic(topic);
    setData(null);
    mutation.mutate(topic);
  };

  return (
    <main className="min-h-screen bg-slate-50/50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-3">
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            ResearchPilot <span className="text-indigo-600">AI</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Autonomous research agent generating validated, structured insights powered by multi-agent web search.
          </p>
        </div>

        {/* Input Form */}
        <ResearchForm onSubmit={handleSearch} isLoading={mutation.isPending} />

        {/* Error State */}
        {mutation.isError && (
          <div className="max-w-2xl mx-auto p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-center text-sm">
            Research generation failed. Please check your backend service on port 8000.
          </div>
        )}

        {/* Loading State */}
        {mutation.isPending && <ReportSkeleton />}

        {/* Generated Report Display */}
        {data && <ResearchReport report={data.result} topic={currentTopic} />}
      </div>
    </main>
  );
}