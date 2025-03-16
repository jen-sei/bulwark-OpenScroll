import React from "react";
import FeatureCard from "./FeatureCard";

const Features = () => {
  return (
    <div className="flex flex-col mb-32 md:mb-48 max-w-screen-lg">
      <h2 className="font-inter font-bold text-4xl md:text-7xl tracking-[-0.05em] bg-gradient bg-clip-text text-transparent">
        The power of Artificial Intelligence to propel blockchain innovation forward
      </h2>
      <p className="font-inter font-light text-xl md:text-2xl text-brand-gray mb-5 md:mb-10">
        Unleashing AI to transform AiFi, BULWARK&apos;s Agents drive innovation, security, and opportunity to new
        heights.
      </p>

      <div className="flex flex-col gap-4 flex-wrap">
        {/* First row */}
        <div className="flex flex-col md:flex-row gap-4 items-stretch justify-center">
          <FeatureCard
            title="Scroll Mastery"
            description="Navigate the Scroll ecosystem with unparalleled ease and insight, guided by our AI Agents."
            imageSrc="/img/features/1.png"
          />

          <FeatureCard
            title="Health Factors"
            description="Monitor your investment with real-time health factors ensuring smarter decisions and better yield opportunities."
            imageSrc="/img/features/2.png"
          />
        </div>

        {/* Second row */}
        <div className="flex flex-col md:flex-row gap-4">
          <FeatureCard
            title="Profit/Loss Tracking"
            description="Easily track performance with p/l data, giving you a clear picture of your gains and losses over time."
            imageSrc="/img/features/3.png"
          />

          <FeatureCard
            title="Protocol-Specific Indicators"
            description="Access tailored metrics and insights, including key data points unique to each platform."
            imageSrc="/img/features/4.png"
          />

          <FeatureCard
            title="Real-Time Metrics"
            description="Stay updated with live data for your positions, including current APYs, and yield generation."
            imageSrc="/img/features/5.png"
          />
        </div>
      </div>
    </div>
  );
};

export default Features;
