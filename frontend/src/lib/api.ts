if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL environment variable is required");
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export interface ProcessOptions {
  files: File[];
  task: string;
  format: string;
  quality: number | null;
  resizeSize?: number;
}

export interface ProcessResult {
  blob: Blob;
  processedCount: number;
  errorCount: number;
}

export async function processImages(
  options: ProcessOptions
): Promise<ProcessResult> {
  const formData = new FormData();

  options.files.forEach((file) => formData.append("files", file));
  formData.append("task", options.task);
  formData.append("format", options.format);
  if (options.quality !== null) {
    formData.append("quality", options.quality.toString());
  }
  if (options.resizeSize) {
    formData.append("size", options.resizeSize.toString());
  }

  const response = await fetch(`${API_URL}/api/process`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const processedCount = response.headers.get("X-Processed-Count");
  const errorCount = response.headers.get("X-Error-Count");

  if (!processedCount || !errorCount) {
    throw new Error("Missing required response headers from API");
  }

  return {
    blob: await response.blob(),
    processedCount: parseInt(processedCount),
    errorCount: parseInt(errorCount),
  };
}
