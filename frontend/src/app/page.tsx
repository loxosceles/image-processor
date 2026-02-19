"use client";

import { useState } from "react";
import { FileDropzone } from "@/components/file-dropzone";
import { TaskSelector } from "@/components/task-selector";
import { processImages } from "@/lib/api";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [task, setTask] = useState("grayscale");
  const [format, setFormat] = useState("webp");
  const [quality, setQuality] = useState(80);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (files.length === 0) return;

    setIsProcessing(true);
    setError(null);

    try {
      const result = await processImages({
        files,
        task,
        format,
        quality: format === "png" ? null : quality,
      });

      const url = URL.createObjectURL(result.blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "processed.zip";
      a.click();
      URL.revokeObjectURL(url);

      setFiles([]);
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
              onTaskChange={setTask}
              onFormatChange={setFormat}
              onQualityChange={setQuality}
            />
          </div>

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
