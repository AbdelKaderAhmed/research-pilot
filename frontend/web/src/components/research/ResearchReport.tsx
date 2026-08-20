import { ResearchReportSchema } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, TrendingUp, BookOpen } from 'lucide-react';

interface ResearchReportProps {
  report: ResearchReportSchema;
  topic: string;
}

export function ResearchReport({ report, topic }: ResearchReportProps) {
  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 mt-8">
      {/* Header */}
      <div className="space-y-2 text-left">
        <Badge variant="outline" className="border-indigo-200 text-indigo-700 bg-indigo-50/50">
          Completed Research
        </Badge>
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">{report.title}</h1>
        <p className="text-sm text-gray-500">Topic: {topic}</p>
      </div>

      {/* Executive Summary */}
      <Card className="border-gray-200 shadow-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg font-semibold flex items-center gap-2 text-indigo-600">
            <BookOpen className="w-5 h-5" /> Executive Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 leading-relaxed">{report.executive_summary}</p>
        </CardContent>
      </Card>

      {/* Key Findings */}
      <div className="space-y-3">
        <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-600" /> Key Findings
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {report.key_findings.map((finding, idx) => (
            <Card key={idx} className="border-gray-200 hover:border-indigo-200 transition-colors shadow-sm">
              <CardHeader className="pb-2">
                <CardTitle className="text-md font-semibold text-gray-800">
                  {finding.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 leading-normal">{finding.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Strategic Outlook */}
      <Card className="border-indigo-100  from-indigo-50/30 to-white shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold flex items-center gap-2 text-indigo-900">
            <TrendingUp className="w-5 h-5 text-indigo-600" /> Strategic Outlook
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-700 leading-relaxed">{report.summary_outlook}</p>
        </CardContent>
      </Card>
    </div>
  );
}