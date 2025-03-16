export default function HealthFactorPanel() {
  return (
    <div className="font-inter">
      <h2 className="text-2xl font-medium mb-6">Health Factor</h2>

      <div className="grid grid-cols-3 gap-4">
        <div className="flex flex-col items-center">
          <span className="text-[#f66435] text-sm mb-2">ANCHOR_1</span>
          <div className="bg-[#121212] rounded-full w-20 h-20 flex items-center justify-center">
            <span className="text-[#f4efca] text-3xl font-bold">1.6</span>
          </div>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-[#f66435] text-sm mb-2">ANCHOR_2</span>
          <div className="bg-[#121212] rounded-full w-20 h-20 flex items-center justify-center">
            <span className="text-[#f4efca] text-3xl font-bold">1.6</span>
          </div>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-[#f66435] text-sm mb-2">WILDCARD</span>
          <div className="bg-[#121212] rounded-full w-20 h-20 flex items-center justify-center">
            <span className="text-[#f4efca] text-3xl font-bold">1.1</span>
          </div>
        </div>
      </div>
    </div>
  );
}
