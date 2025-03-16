import React from "react";
import Image from "next/image";
import { RainbowKitCustomConnectButton } from "./scaffold-eth";

const Hero = () => {
  return (
    <div className="flex flex-col items-center">
      <div className="text-center my-2">
        <h1 className="flex items-center justify-center text-6xl md:text-7xl font-light text-brand-cream mb-0">
          <Image src="/bulwark.svg" alt="BULWARK" width={160} height={41} className="h-auto w-auto" priority />
        </h1>
        <p className="text-brand-cream text-3xl md:text-6xl font-light tracking-wider font-post-no-bills my-0">
          smarter defi. safer yields.
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 mt-3 mb-2">
        <RainbowKitCustomConnectButton title="launch" />
        <a
          href="https://github.com/MihRazvan/bulwark_scroll"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block bg-brand-darkgray hover:bg-brand-darkgray/80 text-white py-1 px-12 rounded-full text-xl transition-all animate-glow-gray border-2 border-black font-inter font-semibold"
        >
          learn
        </a>
      </div>

      <div className="flex flex-col items-center -mb-16">
        <p className="text-brand-cream text-xl mb-2 font-inter font-light">Partners & Technology</p>
        <a
          href="https://scroll.io/"
          target="_blank"
          rel="noopener noreferrer"
          className="transition-transform hover:scale-105"
        >
          <Image src="/img/scroll.png" alt="Scroll" width={58} height={58} className="h-auto w-auto" />
        </a>
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

      <div className="w-screen relative">
        <Image src="/img/splitter.png" alt="Splitter" width={1920} height={50} className="w-full h-auto object-cover" />
      </div>
    </div>
  );
};

export default Hero;
