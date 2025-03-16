import Image from "next/image";

export default function AlertsPanel() {
  return (
    <div>
      <h2 className="text-2xl font-medium mb-6">Alerts</h2>

      <div className="space-y-6">
        <div>
          <h3 className="text-[#f66435] font-medium mb-3">ANCHOR</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[#f4efca]">Ai Actions</span>
              <div className="w-6 h-6 rounded-full border-2 border-[#f4efca]"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[#f4efca]">Liquidations</span>
              <div className="w-6 h-6 rounded-full bg-[#f66435]"></div>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-[#f66435] font-medium mb-3">WILDCARD</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[#f4efca]">Ai Actions</span>
              <div className="w-6 h-6 rounded-full bg-[#f66435]"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[#f4efca]">Liquidations</span>
              <div className="w-6 h-6 rounded-full bg-[#f66435]"></div>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-[#f66435] font-medium mb-3">ZENITH</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[#f4efca]">Ai Actions</span>
              <div className="w-6 h-6 rounded-full border-2 border-[#f4efca]"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[#f4efca]">Liquidations</span>
              <div className="w-6 h-6 rounded-full border-2 border-[#f4efca]"></div>
            </div>
          </div>
        </div>

        <div className="mt-6 relative">
          <input
            type="email"
            placeholder="E-mail..."
            className="w-full bg-transparent border-2 border-[#f4efca] rounded-lg py-2 px-3 text-[#f4efca] placeholder-[#c9c7ba]"
          />
          <div className="relative">
            <Image
              src="/icons/bell.png"
              alt="Notifications"
              width={20}
              height={20}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
