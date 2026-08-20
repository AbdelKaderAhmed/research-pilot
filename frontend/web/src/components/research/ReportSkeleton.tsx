import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

export function ReportSkeleton() {
  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 mt-8 animate-pulse">
      <Card className="border-gray-100 shadow-sm">
        <CardHeader className="space-y-3">
          <Skeleton className="h-8 w-3/4 rounded-md" />
          <Skeleton className="h-4 w-1/4 rounded-md" />
        </CardHeader>
        <CardContent className="space-y-4">
          <Skeleton className="h-20 w-full rounded-md" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
            <Skeleton className="h-32 rounded-lg" />
            <Skeleton className="h-32 rounded-lg" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}