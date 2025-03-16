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
    <div className="flex min-h-screen bg-brand-background text-white">
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <Header title="Portfolio" subtitle="Overview" />
        {/* Content */}
        <main className="flex-1 p-2 md:p-6 bg-black">
          <div className="min-h-screen text-[#f4efca]">
            <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-4 gap-2 md:gap-6">
              <div className="lg:col-span-3 bg-[#000000]">
                <PerformanceChart />
              </div>

              <AlertsPanel />

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
