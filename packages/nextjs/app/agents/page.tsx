"use client";

import Image from "next/image";
import { NextPage } from "next";
// import { useAccount } from "wagmi";
import Header from "~~/components/Header";
import Sidebar from "~~/components/Sidebar";

const Agents: NextPage = () => {
  // const { isConnected, isDisconnected, isConnecting } = useAccount();

  return (
    <div className="flex h-screen bg-black text-white">
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <Header title="Agents" subtitle="Overview" />

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
