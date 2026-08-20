'use client';

import { useState } from 'react';
import { Search, Loader2, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface ResearchFormProps {
  onSubmit: (topic: string) => void;
  isLoading: boolean;
}

export function ResearchForm({ onSubmit, isLoading }: ResearchFormProps) {
  const [topic, setTopic] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim() && !isLoading) {
      onSubmit(topic.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto space-y-4">
      <div className="relative flex items-center">
        <Search className="absolute left-4 w-5 h-5 text-gray-400" />
        <Input
          type="text"
          placeholder="Enter research topic (e.g. LLM Reasoning Techniques in 2026)..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          disabled={isLoading}
          className="pl-12 pr-36 h-14 text-base rounded-xl border-gray-200 focus:border-indigo-500 shadow-sm"
        />
        <Button
          type="submit"
          disabled={isLoading || !topic.trim()}
          className="absolute right-2 h-10 px-5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-medium transition-all"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Sparkles className="mr-2 h-4 w-4" />
              Research
            </>
          )}
        </Button>
      </div>
    </form>
  );
}