"use client";

import { useState } from "react";
import { FileDropzone } from "@/components/file-dropzone";
import { TaskSelector } from "@/components/task-selector";
import { ProgressDisplay } from "@/components/progress-display";
import { processImages, ProcessResult } from "@/lib/api";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [task, setTask] = useState("resize");
  const [format, setFormat] = useState("webp");
  const [quality, setQuality] = useState(80);
  const [resizeSize, setResizeSize] = useState(128);
  const [aspectRatio, setAspectRatio] = useState("original");
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ProcessResult | null>(null);

  const handleSubmit = async (evt: React.FormEvent) => {
    evt.preventDefault();
    if (files.length === 0) return;

    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      const processResult = await processImages({
        files,
        task,
        format,
        quality: format === "png" ? null : quality,
        resizeSize: task === "resize" ? resizeSize : undefined,
        aspectRatio: task === "resize" ? aspectRatio : undefined,
      });

      const url = URL.createObjectURL(processResult.blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "processed.zip";
      a.click();
      URL.revokeObjectURL(url);

      setFiles([]);
      setResult(processResult);
      setTimeout(() => setResult(null), 5000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Processing failed");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <main className="min-h-screen p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-white">Image Processor</h1>
          <p className="text-gray-400 mt-1">
            Upload images to resize, convert, or apply effects
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-[#171717] border border-[#262626] rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-200 mb-4">
              1. Select Images
            </h2>
            <FileDropzone files={files} onFilesChange={setFiles} />
          </div>

          <div className="bg-[#171717] border border-[#262626] rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-200 mb-4">
              2. Configure Processing
            </h2>
            <TaskSelector
              task={task}
              format={format}
              quality={quality}
              resizeSize={resizeSize}
              aspectRatio={aspectRatio}
              onTaskChange={setTask}
              onFormatChange={setFormat}
              onQualityChange={setQuality}
              onResizeSizeChange={setResizeSize}
              onAspectRatioChange={setAspectRatio}
            />
          </div>

          <ProgressDisplay isProcessing={isProcessing} fileCount={files.length} />

          {result && (
            <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
              <p className="font-medium text-green-300">✓ Processing complete!</p>
              <p className="text-sm text-green-400/80 mt-1">
                {result.processedCount} image{result.processedCount !== 1 ? "s" : ""} processed
                {result.errorCount > 0 && ` (${result.errorCount} failed)`}
              </p>
            </div>
          )}

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <p className="font-medium text-red-400">Processing failed</p>
              <p className="text-red-300/80 text-sm mt-1">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={files.length === 0 || isProcessing}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors"
          >
            {isProcessing ? "Processing..." : `Process ${files.length} Image(s)`}
          </button>
        </form>
      </div>
    </main>
  );
}
