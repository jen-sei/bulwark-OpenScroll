"use client";

import { useState } from "react";
import { NextPage } from "next";
import Header from "~~/components/Header";
import Sidebar from "~~/components/Sidebar";
import StrategyCard from "~~/components/StrategyCard";
import strategiesData from "~~/services/example-strategies-json.json";
import { Strategy } from "~~/types/strategy";

const Agents: NextPage = () => {
  const [selectedStrategy, setSelectedStrategy] = useState<number | null>(null);
  const selectedStrategies = [
    strategiesData.strategies[0],
    strategiesData.strategies[2],
    strategiesData.strategies[4],
  ] as unknown as Strategy[];

  const [isExecuting, setIsExecuting] = useState(false);

  const handleExecuteStrategy = () => {
    setIsExecuting(true);
    console.log("Executing strategy...", selectedStrategy);
    setTimeout(() => {
      setIsExecuting(false);
    }, 3000);
  };

  return (
    <div className="flex min-h-screen bg-black text-white">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <Header title="Agents" subtitle="Overview" />

        <main className="flex-1 p-6 bg-neutral-900 flex flex-col">
          <div className="flex flex-col md:flex-row gap-4 flex-grow">
            {selectedStrategies.map((strategy, index) => {
              return (
                <div className="flex-grow flex flex-col" key={`strategy-${index}`}>
                  <StrategyCard
                    riskLevel={strategy.risk_level}
                    steps={strategy.steps}
                    apy={`${strategy.total_expected_apy.toFixed(1)}%`}
                    explanation={strategy.explanation}
                    onClick={() => {
                      setSelectedStrategy(strategy.risk_level);
                    }}
                    isSelected={selectedStrategy === strategy.risk_level}
                  />
                  <div className="h-[80px] w-full flex justify-center items-center">
                    {selectedStrategy === strategy.risk_level && (
                      <button
                        className="w-48 bg-[#fff9e8] text-black font-medium rounded-md p-3 hover:bg-[#fff0c4] transition-colors"
                        onClick={handleExecuteStrategy}
                        disabled={isExecuting}
                      >
                        {isExecuting ? "Executing..." : "Execute"}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Agents;
