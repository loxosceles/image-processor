export default function Home() {
  return (
    <main className="min-h-screen p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-white">Image Processor</h1>
          <p className="text-gray-400 mt-1">
            Upload images to resize, convert, or apply effects
          </p>
        </header>

        <div className="bg-[#171717] border border-[#262626] rounded-lg p-6">
          <p className="text-gray-500">Upload component goes here</p>
        </div>
      </div>
    </main>
  );
}
