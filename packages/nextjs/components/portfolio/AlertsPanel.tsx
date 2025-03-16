import { useState } from "react";
import Image from "next/image";

export default function AlertsPanel() {
  const [anchorAiActions, setAnchorAiActions] = useState(false);
  const [anchorLiquidations, setAnchorLiquidations] = useState(true);
  const [wildcardAiActions, setWildcardAiActions] = useState(true);
  const [wildcardLiquidations, setWildcardLiquidations] = useState(true);
  const [zenithAiActions, setZenithAiActions] = useState(false);
  const [zenithLiquidations, setZenithLiquidations] = useState(false);

  interface CheckboxProps {
    checked: boolean;
    onChange: (checked: boolean) => void;
    label: string;
  }

  const CustomCheckbox = ({ checked, onChange, label }: CheckboxProps) => (
    <div className="flex items-center justify-between">
      <span className="text-brand-cream">{label}</span>
      <button
        onClick={() => onChange(!checked)}
        className="w-6 h-6 rounded-full border-2 border-brand-cream p-0.5"
        aria-checked={checked}
        role="checkbox"
      >
        {checked && <div className="w-full h-full rounded-full bg-brand-orange-accent"></div>}
      </button>
    </div>
  );

  return (
    <div className="border border-brand-cream rounded-xl p-2 px-4 md:p-4 border-opacity-20 bg-brand-background font-inter">
      <h2 className="text-2xl font-medium mb-6">Alerts</h2>

      <div className="space-y-6">
        <div>
          <h3 className="text-[#f66435] font-medium mb-3">ANCHOR</h3>
          <div className="space-y-3">
            <CustomCheckbox checked={anchorAiActions} onChange={setAnchorAiActions} label="Ai Actions" />
            <CustomCheckbox checked={anchorLiquidations} onChange={setAnchorLiquidations} label="Liquidations" />
          </div>
        </div>

        <div>
          <h3 className="text-[#f66435] font-medium mb-3">WILDCARD</h3>
          <div className="space-y-3">
            <CustomCheckbox checked={wildcardAiActions} onChange={setWildcardAiActions} label="Ai Actions" />
            <CustomCheckbox checked={wildcardLiquidations} onChange={setWildcardLiquidations} label="Liquidations" />
          </div>
        </div>

        <div>
          <h3 className="text-[#f66435] font-medium mb-3">ZENITH</h3>
          <div className="space-y-3">
            <CustomCheckbox checked={zenithAiActions} onChange={setZenithAiActions} label="Ai Actions" />
            <CustomCheckbox checked={zenithLiquidations} onChange={setZenithLiquidations} label="Liquidations" />
          </div>
        </div>
      </div>
      <div className="mt-6 relative m-auto md:-mb-2 md:-mx-2">
        <input
          type="email"
          placeholder="E-mail..."
          className="w-full bg-transparent border border-brand-cream rounded-xl p-2 px-3 text-brand-cream placeholder-brand-gray placeholder-opacity-20 border-opacity-20"
        />
        <Image
          src="/icons/bell.png"
          alt="Notifications"
          width={20}
          height={20}
          className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5"
        />
      </div>
    </div>
  );
}
