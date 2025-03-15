"use client";

import Image from "next/image";
import { NextPage } from "next";
import Sidebar from "~~/components/Sidebar";

const Agents: NextPage = () => {
  return (
    <div className="flex h-screen bg-black text-white">
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="h-[84px] border-b border-neutral-800 flex items-center justify-between px-6">
          <div className="flex items-center text-gray-400 text-lg">
            <Image src="/icons/star.svg" alt="Star" width={20} height={20} className="h-5 w-5 mr-2 text-neutral-500" />
            <span className="text-neutral-500">Agents /</span>
            <span className="ml-2 text-white">Overview</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="relative">
              <Image src="/icons/bell.png" alt="Bell" width={20} height={20} className="h-5 w-5 text-neutral-400" />
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-orange-500 rounded-full flex items-center justify-center text-[10px]">
                1
              </span>
            </div>
            <div className="flex items-center gap-2 bg-neutral-800/80 rounded-md px-3 py-1.5">
              <div className="w-8 h-8 rounded-md overflow-hidden">
                <Image
                  src="/placeholder.svg?height=32&width=32"
                  alt="Avatar"
                  width={32}
                  height={32}
                  className="h-full w-full object-cover"
                />
              </div>
              <span className="text-sm font-mono">0x12a3...6d4d</span>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 p-6 bg-neutral-900">
          <div className="grid grid-cols-3 gap-6 mt-6">
            {/* Anchor Card */}
            <div className="bg-gradient-to-b from-[#1e2c48] to-[#101b31] rounded-2xl overflow-hidden border border-[#2a3a56]">
              <div className="p-6 pb-0 h-full flex flex-col">
                <h2 className="text-4xl font-semibold text-orange-400 mb-1">Anchor</h2>
                <p className="text-xl text-gray-300 mb-6">Steady growth over time</p>

                <ul className="mb-6 space-y-1">
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Aave
                  </li>
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Compound
                  </li>
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Rho markets
                  </li>
                </ul>

                <div className="text-5xl font-bold text-gray-300 italic mb-2">6.8% APY</div>

                <div className="mt-auto mb-0 w-full flex justify-center">
                  <Image
                    src="/placeholder.svg?height=150&width=150"
                    alt="Coin"
                    width={150}
                    height={150}
                    className="h-auto w-auto"
                  />
                </div>
              </div>
            </div>

            {/* Wildcard Card */}
            <div className="bg-gradient-to-b from-[#3a2d2c] to-[#261c1a] rounded-2xl overflow-hidden border border-[#4a3b39]">
              <div className="p-6 pb-0 h-full flex flex-col">
                <h2 className="text-4xl font-semibold text-orange-400 mb-1">Wildcard</h2>
                <p className="text-xl text-gray-300 mb-6">For risk-takers & degens</p>

                <ul className="mb-6 space-y-1">
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Nuri
                  </li>
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Tempest
                  </li>
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    SyncSwap
                  </li>
                </ul>

                <div className="text-5xl font-bold text-gray-300 italic mb-2">39% APY</div>

                <div className="mt-auto mb-0 w-full flex justify-center">
                  <Image
                    src="/placeholder.svg?height=150&width=150"
                    alt="Dice"
                    width={150}
                    height={150}
                    className="h-auto w-auto"
                  />
                </div>
              </div>
            </div>

            {/* Zenith Card */}
            <div className="bg-gradient-to-b from-[#2c3a26] to-[#1c2619] rounded-2xl overflow-hidden border border-[#3b4a39]">
              <div className="p-6 pb-0 h-full flex flex-col">
                <h2 className="text-4xl font-semibold text-orange-400 mb-1">Zenith</h2>
                <p className="text-xl text-gray-300 mb-6">Balanced performance</p>

                <ul className="mb-6 space-y-1">
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Mitosis
                  </li>
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Ambient
                  </li>
                  <li className="flex items-center text-gray-300 text-lg">
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
                    Aave
                  </li>
                </ul>

                <div className="text-5xl font-bold text-gray-300 italic mb-2">4.5% APY</div>

                <div className="mt-auto mb-0 w-full flex justify-center">
                  <Image
                    src="/placeholder.svg?height=150&width=150"
                    alt="Gear"
                    width={150}
                    height={150}
                    className="h-auto w-auto"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Input Controls */}
          <div className="mt-8 flex gap-4">
            <input
              type="text"
              placeholder="Amount..."
              className="flex-1 bg-neutral-900 border border-neutral-700 rounded-md p-3 text-white focus:outline-none focus:ring-1 focus:ring-neutral-600"
            />
            <input
              type="text"
              placeholder="token"
              className="w-60 bg-neutral-900 border border-neutral-700 rounded-md p-3 text-white focus:outline-none focus:ring-1 focus:ring-neutral-600"
            />
            <button className="w-48 bg-[#fff9e8] text-black font-medium rounded-md p-3 hover:bg-[#fff0c4] transition-colors">
              deploy
            </button>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Agents;
