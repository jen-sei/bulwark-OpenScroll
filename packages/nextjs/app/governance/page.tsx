"use client";

import { NextPage } from "next";
import Header from "~~/components/Header";
import Sidebar from "~~/components/Sidebar";

const Governance: NextPage = () => {
  return (
    <div className="flex min-h-screen bg-black text-white">
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <Header title="Governance" subtitle="Overview" />
        {/* Content */}
        <main className="flex-1 p-6 bg-neutral-900">portfolio</main>
      </div>
    </div>
  );
};

export default Governance;
