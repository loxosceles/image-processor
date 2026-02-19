"use client";

import { useState } from "react";

const SUPPORTED_TYPES = ["image/jpeg", "image/png", "image/webp"];

interface FileDropzoneProps {
  files: File[];
  onFilesChange: (files: File[]) => void;
}

export function FileDropzone({ files, onFilesChange }: FileDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files).filter((f) =>
      SUPPORTED_TYPES.includes(f.type)
    );
    onFilesChange([...files, ...droppedFiles]);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files).filter((f) =>
        SUPPORTED_TYPES.includes(f.type)
      );
      onFilesChange([...files, ...selectedFiles]);
    }
  };

  const removeFile = (index: number) => {
    onFilesChange(files.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? "border-blue-500 bg-blue-500/10"
            : "border-[#404040] hover:border-[#525252]"
        }`}
      >
        <input
          type="file"
          multiple
          accept={SUPPORTED_TYPES.join(",")}
          onChange={handleFileInput}
          className="hidden"
          id="file-input"
        />
        <label htmlFor="file-input" className="cursor-pointer">
          <p className="font-medium text-gray-300">
            Drop images here or click to upload
          </p>
          <p className="text-sm text-gray-500 mt-1">Supports JPEG, PNG, WebP</p>
        </label>
      </div>

      {files.length > 0 && (
        <ul className="space-y-2">
          {files.map((file, index) => (
            <li
              key={`${file.name}-${index}`}
              className="flex items-center justify-between bg-[#1f1f1f] border border-[#303030] rounded px-3 py-2"
            >
              <span className="text-sm text-gray-300 truncate">{file.name}</span>
              <button
                type="button"
                onClick={() => removeFile(index)}
                className="text-gray-500 hover:text-red-400 ml-2"
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
