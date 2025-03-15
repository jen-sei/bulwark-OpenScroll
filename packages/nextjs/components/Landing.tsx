import Image from "next/image";
import FeatureCard from "./FeatureCard";

export default function Home() {
  return (
    <div className="min-h-screen">
      <div className="container mx-auto px-4 py-12 relative z-10 flex flex-col items-center">
        <div className="text-center my-2">
          <h1 className="flex items-center justify-center text-6xl md:text-7xl font-light text-brand-cream mb-0">
            <Image src="/bulwark.svg" alt="BULWARK" width={160} height={41} className="h-auto w-auto" priority />
          </h1>
          <p className="text-brand-cream text-3xl md:text-6xl font-light tracking-wider font-post-no-bills my-0">
            smarter defi. safer yields.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 mt-3 mb-2">
          <button
            onClick={() => {
              /* your click handler here */
            }}
            className="bg-brand-orange-accent hover:bg-brand-orange-accent/80 text-white py-3 px-12 rounded-full text-xl transition-all border-2 border-[#D3673A] animate-glow-orange font-inter font-semibold"
          >
            launch
          </button>
          <button
            onClick={() => {
              /* your click handler here */
            }}
            className="bg-brand-darkgray hover:bg-brand-darkgray/80 text-white py-3 px-12 rounded-full text-xl transition-all  animate-glow-gray border-2 border-black font-inter font-semibold"
          >
            learn
          </button>
        </div>

        <div className="flex flex-col items-center -mb-16">
          <p className="text-brand-cream text-xl mb-2 font-inter font-light">Partners & Technology</p>
          <Image src="/img/scroll.png" alt="Scroll" width={58} height={58} className="h-auto w-auto" />
        </div>

        <div className="mt-12 w-full max-w-5xl">
          <Image
            src="/img/hero.png"
            alt="Bulwark Trading Strategies"
            width={1920}
            height={800}
            className="w-full h-auto"
            priority
          />
        </div>

        <div className="flex flex-col my-32 md:my-96">
          <h2 className="text-brand-gray text-3xl md:text-6xl font-inter font-normal text-center">
            BULWARK&apos;s AI-driven strategies fortify DeFi, delivering risk-aware allocations, seamless execution, and
            real-time monitoring with unmatched precision and efficiency.
          </h2>
          <div className="flex flex-col md:flex-row mt-24 md:mt-48 mb-12 md:mb-24">
            <Image
              src="/img/aiagents.png"
              alt="AI Agents"
              className="min-w-[45%] w-auto h-auto"
              width={484}
              height={428}
            />
            <div className="flex flex-col p-4 md:p-12">
              <h2 className="font-inter font-bold text-2xl md:text-5xl tracking-[-0.05em] bg-gradient bg-clip-text text-transparent">
                Intelligent Agents to drive the AiFi Blockchain Revolution
              </h2>
              <p className="font-inter font-light text-xl md:text-2xl text-brand-gray mb-5 md:mb-10">
                Discover BULWARK´s suite of AI Agents designed to empower and simplify your DeFi activities. From
                maximizing trading efficiency with the Automated Trading Agent to ensuring asset security through the
                External Protocol selection, each tool delivers tangible benefits, making your web3 yield journey
                seamless and profitable.
              </p>
              <button
                onClick={() => {
                  /* your click handler here */
                }}
                className="self-start bg-brand-darkgray hover:bg-brand-darkgray/80 text-white py-3 px-12 rounded-full text-xl transition-all  animate-glow-gray border-2 border-black font-inter font-semibold"
              >
                try now
              </button>
            </div>
          </div>
        </div>

        <div className="flex flex-col mb-48 md:mb-96 max-w-screen-lg">
          <h2 className="font-inter font-bold text-4xl md:text-7xl tracking-[-0.05em] bg-gradient bg-clip-text text-transparent">
            The power of Artificial Intelligence to propel blockchain innovation forward
          </h2>
          <p className="font-inter font-light text-xl md:text-2xl text-brand-gray mb-5 md:mb-10">
            Unleashing AI to transform AiFi, BULWARK’s Agents drive innovation, security, and opportunity to new
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
      </div>
    </div>
  );
}
