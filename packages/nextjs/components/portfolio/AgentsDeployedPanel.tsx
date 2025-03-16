export default function AgentsDeployedPanel() {
  return (
    <div>
      <h2 className="text-2xl font-medium mb-6">Agents Deployed</h2>

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="bg-gradient-to-br from-[#1e3a8a] to-[#3b82f6] rounded-xl p-4 flex items-center justify-center">
          <span className="text-[#f4efca] text-4xl font-bold">A1</span>
        </div>

        <div className="bg-gradient-to-br from-[#1e3a8a] to-[#3b82f6] rounded-xl p-4 flex items-center justify-center">
          <span className="text-[#f4efca] text-4xl font-bold">A2</span>
        </div>

        <div className="bg-gradient-to-br from-[#7c2d12] to-[#c2410c] rounded-xl p-4 flex items-center justify-center">
          <span className="text-[#f4efca] text-4xl font-bold">W</span>
        </div>
      </div>

      <div className="flex items-center text-sm text-[#c9c7ba]">
        <span>exit vault:</span>
        <div className="flex gap-2 ml-2">
          <button className="text-[#f4efca] underline">A1</button>
          <button className="text-[#f4efca]">A2</button>
          <button className="text-[#f4efca]">A3</button>
        </div>
      </div>
    </div>
  );
}
