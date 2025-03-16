import React from "react";
import Image from "next/image";
import { RainbowKitCustomConnectButton } from "./scaffold-eth/RainbowKitCustomConnectButton";

const Description = () => {
  return (
    <div className="flex flex-col my-32 md:my-64 max-w-screen-xl mx-auto">
      <h2 className="text-brand-gray text-3xl md:text-5xl font-inter font-normal text-center">
        BULWARK&apos;s AI-driven strategies fortify DeFi, delivering risk-aware allocations, seamless execution, and
        real-time monitoring with unmatched precision and efficiency.
      </h2>
      <div className="flex flex-col xl:flex-row mt-24 md:mt-48 mb-12 md:mb-24 items-center">
        <div className="flex-shrink-0 w-full md:w-[45%]">
          <Image
            src="/img/aiagents.png"
            alt="AI Agents"
            className="w-full h-auto object-contain"
            width={484}
            height={428}
            priority
          />
        </div>
        <div className="flex flex-col p-4 md:p-12">
          <h2 className="font-inter font-bold text-2xl md:text-5xl tracking-[-0.05em] bg-gradient bg-clip-text text-transparent">
            Intelligent Agents to drive the AiFi Blockchain Revolution
          </h2>
          <p className="font-inter font-light text-xl md:text-2xl text-brand-gray mb-5 md:mb-10">
            Discover BULWARK´s suite of AI Agents designed to empower and simplify your DeFi activities. From maximizing
            trading efficiency with the Automated Trading Agent to ensuring asset security through the External Protocol
            selection, each tool delivers tangible benefits, making your web3 yield journey seamless and profitable.
          </p>
          <RainbowKitCustomConnectButton title="try now" secondary />
          {/* <button
           
            className="self-start bg-brand-darkgray hover:bg-brand-darkgray/80 text-white py-3 px-12 rounded-full text-xl transition-all animate-glow-gray border-2 border-black font-inter font-semibold"
          >
            try now
          </button> */}
        </div>
      </div>
    </div>
  );
};

export default Description;
