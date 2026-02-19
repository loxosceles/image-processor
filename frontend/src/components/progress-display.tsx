"use client";

interface ProgressDisplayProps {
  isProcessing: boolean;
  fileCount: number;
}

export function ProgressDisplay({ isProcessing, fileCount }: ProgressDisplayProps) {
  if (!isProcessing) return null;

  return (
    <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
      <div className="flex items-center gap-3">
        <div className="animate-spin h-5 w-5 border-2 border-blue-400 border-t-transparent rounded-full" />
        <div>
          <p className="font-medium text-blue-300">Processing images...</p>
          <p className="text-sm text-blue-400/80">
            {fileCount} image{fileCount !== 1 ? "s" : ""} being processed
          </p>
        </div>
      </div>
    </div>
  );
}
