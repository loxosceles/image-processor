"use client";

interface TaskSelectorProps {
  task: string;
  format: string;
  quality: number;
  resizeSize: number;
  onTaskChange: (task: string) => void;
  onFormatChange: (format: string) => void;
  onQualityChange: (quality: number) => void;
  onResizeSizeChange: (size: number) => void;
}

const TASKS = [
  { value: "resize", label: "Resize" },
  { value: "grayscale", label: "Grayscale" },
  { value: "blur", label: "Blur" },
  { value: "rotate", label: "Auto-Rotate (EXIF)" },
];

const RESIZE_SIZES = [
  { value: 64, label: "64×64 (Favicon)" },
  { value: 128, label: "128×128 (Thumbnail)" },
  { value: 256, label: "256×256 (Small)" },
  { value: 512, label: "512×512 (Medium)" },
  { value: 1024, label: "1024×1024 (Large)" },
  { value: 2048, label: "2048×2048 (HD)" },
];

const FORMATS = [
  { value: "webp", label: "WebP", defaultQuality: 80 },
  { value: "jpeg", label: "JPEG", defaultQuality: 85 },
  { value: "png", label: "PNG (lossless)", defaultQuality: null },
];

export function TaskSelector({
  task,
  format,
  quality,
  resizeSize,
  onTaskChange,
  onFormatChange,
  onQualityChange,
  onResizeSizeChange,
}: TaskSelectorProps) {
  const selectedFormat = FORMATS.find((f) => f.value === format);
  const isPng = format === "png";

  const selectClasses =
    "w-full rounded-md border border-[#404040] bg-[#1f1f1f] px-3 py-2 text-gray-200 focus:border-blue-500 focus:outline-none";

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Task
        </label>
        <select
          value={task}
          onChange={(evt) => onTaskChange(evt.target.value)}
          className={selectClasses}
        >
          {TASKS.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </div>

      {task === "resize" && (
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Size
          </label>
          <select
            value={resizeSize}
            onChange={(evt) => onResizeSizeChange(Number(evt.target.value))}
            className={selectClasses}
          >
            {RESIZE_SIZES.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Output Format
        </label>
        <select
          value={format}
          onChange={(evt) => {
            const newFormat = evt.target.value;
            onFormatChange(newFormat);
            const fmt = FORMATS.find((f) => f.value === newFormat);
            if (fmt?.defaultQuality) {
              onQualityChange(fmt.defaultQuality);
            }
          }}
          className={selectClasses}
        >
          {FORMATS.map((f) => (
            <option key={f.value} value={f.value}>
              {f.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Quality: {isPng ? "N/A" : `${quality}%`}
        </label>
        <input
          type="range"
          min="10"
          max="100"
          value={quality}
          onChange={(evt) => onQualityChange(Number(evt.target.value))}
          disabled={isPng}
          className="w-full accent-blue-500 disabled:opacity-50"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>Smaller file</span>
          <span>
            {selectedFormat?.defaultQuality &&
              `Default: ${selectedFormat.defaultQuality}%`}
          </span>
          <span>Higher quality</span>
        </div>
      </div>
    </div>
  );
}
