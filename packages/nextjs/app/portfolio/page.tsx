"use client";

import { NextPage } from "next";
import Header from "~~/components/Header";
import Sidebar from "~~/components/Sidebar";
import AgentsDeployedPanel from "~~/components/portfolio/AgentsDeployedPanel";
import AlertsPanel from "~~/components/portfolio/AlertsPanel";
import HealthFactorPanel from "~~/components/portfolio/HealthFactorPanel";
import PerformanceChart from "~~/components/portfolio/PerformanceChart";
import TotalValueLockedPanel from "~~/components/portfolio/TotalValueLockedPanel";

const Agents: NextPage = () => {
  return (
    <div className="flex min-h-screen bg-black text-white">
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <Header title="Portfolio" subtitle="Overview" />
        {/* Content */}
        <main className="flex-1 p-6 bg-neutral-900">
          <div className="min-h-screen bg-[#121212] text-[#f4efca] p-6">
            <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-3 bg-[#000000] rounded-2xl p-6 shadow-lg">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-medium">Overall Performance</h2>
                  {/* <button className="flex items-center gap-1 bg-[#121212] px-3 py-1 rounded-lg">
                    All <ChevronDown className="h-4 w-4" />
                  </button> */}
                </div>
                <PerformanceChart />
              </div>

              <div className="bg-[#000000] rounded-2xl p-6 shadow-lg">
                <AlertsPanel />
              </div>

              <div className="lg:col-span-1 bg-[#000000] rounded-2xl p-6 shadow-lg">
                <HealthFactorPanel />
              </div>

              <div className="lg:col-span-1 bg-[#000000] rounded-2xl p-6 shadow-lg">
                <AgentsDeployedPanel />
              </div>

              <div className="lg:col-span-1 bg-[#000000] rounded-2xl p-6 shadow-lg">
                <TotalValueLockedPanel />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Agents;
