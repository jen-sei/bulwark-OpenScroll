"use client";

import { useState } from "react";
import { NextPage } from "next";
import Header from "~~/components/Header";
import Sidebar from "~~/components/Sidebar";
import BalancesDisplay from "~~/components/agents/BalancesDisplay";
import StrategySelector from "~~/components/agents/StrategySelector";

const Agents: NextPage = () => {
  return (
    <div className="flex min-h-screen bg-black text-white">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <Header title="Agents" subtitle="Overview" />

        <main className="flex-grow p-6 bg-black flex flex-col">
          <BalancesDisplay />
          <StrategySelector />
        </main>
      </div>
    </div>
  );
};

export default Agents;
