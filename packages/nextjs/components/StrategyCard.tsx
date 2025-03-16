import React from "react";
import Image from "next/image";
import { StrategyStep } from "~~/types/strategy";

interface StrategyCardProps {
  riskLevel: number;
  steps: StrategyStep[];
  apy: string;
  explanation: string;
  onClick: () => void;
  isSelected: boolean;
}

const getTitle = (riskLevel: number) => {
  switch (riskLevel) {
    case 1:
      return "Anchor";
    case 3:
      return "Zenith";
    case 5:
      return "Wildcard";
  }
};

const getImgSrc = (riskLevel: number) => {
  switch (riskLevel) {
    case 1:
      return "bg-[url(/img/strategies/anchor.png)]";
    case 3:
      return "bg-[url(/img/strategies/zenith.png)]";
    case 5:
      return "bg-[url(/img/strategies/wildcard.png)]";
  }
};

const getDescription = (riskLevel: number) => {
  switch (riskLevel) {
    case 1:
      return "Steady growth over time";
    case 3:
      return "Balanced performance";
    case 5:
      return "For risk-takers & degens";
  }
};

const StrategyCard: React.FC<StrategyCardProps> = ({ riskLevel, steps, apy, explanation, onClick, isSelected }) => {
  const className = `flex-grow relative rounded-xl bg-cover bg-left md:bg-center ${getImgSrc(riskLevel)} ${isSelected ? "border-4 border-brand-cream" : ""}`;
  return (
    <div className={className} onClick={onClick}>
      <div className="absolute inset-0 bg-black/50 rounded-xl"></div>

      <div className="relative p-6 pb-0 h-full flex flex-col">
        <h2 className="font-inter font-bold text-2xl md:text-4xl tracking-[-0.05em] bg-gradient bg-clip-text text-transparent">
          {getTitle(riskLevel)}
        </h2>

        <p className="text-xl text-gray-300 mb-6 font-inter font-light">{getDescription(riskLevel)}</p>

        <ul className="mb-6 space-y-1">
          {steps.map((step, index) => (
            <li key={index} className="flex items-center text-gray-300 text-lg">
              <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
              {step.action} {step.amount} {step.token} on {step.protocol}
            </li>
          ))}
        </ul>

        <p className="text-xl text-gray-300 mb-6 font-inter font-bold flex-grow">{explanation}</p>

        <div className="text-5xl font-bold text-white italic mb-2 text-center">{apy} APY</div>
      </div>
    </div>
  );
};

export default StrategyCard;
