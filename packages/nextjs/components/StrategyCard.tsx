import React from "react";
import { StrategyStep } from "~~/types/strategy";
import formatAction from "~~/utils/formatAction";
import { formattedAmount } from "~~/utils/formattedAmount";

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
      return `url("/img/strategies/anchor_img.png")`;
    case 3:
      return `url("/img/strategies/zenith_img.png")`;
    case 5:
      return `url("/img/strategies/wildcard_img.png")`;
  }
};

const getBgImgSrc = (riskLevel: number) => {
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
  const className = `flex-1 h-full relative rounded-xl bg-cover bg-left md:bg-center border-4 hover:cursor-pointer
   ${getBgImgSrc(riskLevel)} ${isSelected ? "border-brand-cream" : "border-black"}
   transition-all duration-300 hover:transform hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(246,100,53,0.5)]`;

  return (
    <div className={className} onClick={onClick}>
      <div className="absolute inset-0 bg-brand-background/50 rounded-xl transition-opacity duration-300 hover:bg-brand-background/40"></div>

      <div
        className="absolute bottom-0 left-0 right-0 h-1/3 bg-contain bg-bottom bg-no-repeat rounded-b-xl opacity-100 transition-opacity duration-300 hover:opacity-80"
        style={{
          backgroundImage: getImgSrc(riskLevel),
          maskImage: "linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0))",
        }}
      ></div>

      <div className="relative p-6 pb-0 h-full flex flex-col">
        <h2 className="font-inter font-bold text-2xl md:text-4xl tracking-[-0.05em] bg-gradient bg-clip-text text-transparent">
          {getTitle(riskLevel)}
        </h2>

        <p className="text-xl text-gray-300 mb-6 font-inter font-light">{getDescription(riskLevel)}</p>

        <ul className="mb-6 space-y-1">
          {steps.map((step, index) => (
            <li key={index} className="flex items-center text-gray-300 text-sm">
              <span className="h-1.5 w-1.5 rounded-full bg-gray-300 mr-3"></span>
              {formatAction(step.action)} {formattedAmount(step.amount)} {step.token} on {step.protocol}
            </li>
          ))}
        </ul>

        <p className="text-sm text-gray-300 mb-9 font-inter font-bold flex-grow">{explanation}</p>

        <div className="text-5xl font-bold text-white italic mb-36 text-center font-sztos">{apy} APY</div>
      </div>
    </div>
  );
};

export default StrategyCard;
