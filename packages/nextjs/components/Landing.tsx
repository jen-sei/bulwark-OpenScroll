import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Background abstract design - simplified version */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-0 w-1/3 h-full bg-gradient-to-br from-orange-accent/20 to-transparent transform -rotate-12"></div>
        <div className="absolute top-0 right-0 w-1/3 h-full bg-gradient-to-bl from-orange-accent/20 to-transparent transform rotate-12"></div>
      </div>

      <div className="container mx-auto px-4 py-12 relative z-10 flex flex-col items-center">
        {/* Logo and Tagline */}
        <div className="text-center mb-12">
          <h1 className="flex items-center justify-center text-6xl md:text-7xl font-light text-brand-cream mb-4">
            <Image src="/bulwark.svg" alt="BULWARK" width={160} height={41} className="h-auto w-auto" priority />
          </h1>
          <p className="text-brand-cream text-2xl md:text-3xl font-light tracking-wider font-post-no-bills">
            smarter defi. safer yields.
          </p>
        </div>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mb-16">
          <button
            onClick={() => {
              /* your click handler here */
            }}
            className="bg-brand-orange-accent hover:bg-brand-orange-accent/80 text-white font-medium py-3 px-12 rounded-full text-xl transition-all border-2 border-[#D3673A] animate-glow-orange"
          >
            launch
          </button>
          <button
            onClick={() => {
              /* your click handler here */
            }}
            className="bg-brand-darkgray hover:bg-brand-darkgray/80 text-white font-medium py-3 px-12 rounded-full text-xl transition-all  animate-glow-gray border-2 border-black"
          >
            learn
          </button>
        </div>

        {/* Partners & Technology */}
        <div className="text-center mb-8">
          <p className="text-brand-cream text-xl mb-2">Partners & Technology</p>
          Scroll img
        </div>

        {/* Phone Mockups */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-5xl">
          {/* Anchor */}
          <div className="relative mx-auto">
            <div className="bg-black rounded-[40px] p-3 border-4 border-dark-gray overflow-hidden w-[280px] h-[560px]">
              <div className="bg-background h-full rounded-[30px] p-6 flex flex-col">
                <h2 className="text-orange-accent text-4xl font-medium mb-2">Anchor</h2>
                <p className="text-brand-cream text-xl leading-tight">
                  Steady
                  <br />
                  growth
                  <br />
                  over
                  <br />
                  time
                </p>
                <div className="flex-grow flex items-center justify-center">
                  <div className="relative w-40 h-40 rounded-full bg-black flex items-center justify-center border-4 border-white/20">
                    <span className="text-white text-5xl font-bold">$</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Wildcard */}
          <div className="relative mx-auto mt-12 md:mt-24">
            <div className="bg-black rounded-[40px] p-3 border-4 border-dark-gray overflow-hidden w-[280px] h-[560px]">
              <div className="bg-background h-full rounded-[30px] p-6 flex flex-col">
                <h2 className="text-orange-accent text-4xl font-medium mb-2">Wildcard</h2>
                <p className="text-brand-cream text-xl leading-tight">
                  Risk
                  <br />
                  takes
                  <br />
                  and
                  <br />
                  degens
                </p>
                <div className="flex-grow flex items-center justify-center">
                  <div className="relative w-40 h-40">
                    <Image
                      src="/placeholder.svg?height=160&width=160"
                      alt="Dice"
                      width={160}
                      height={160}
                      className="object-contain"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Zenith */}
          <div className="relative mx-auto">
            <div className="bg-black rounded-[40px] p-3 border-4 border-dark-gray overflow-hidden w-[280px] h-[560px]">
              <div className="bg-background h-full rounded-[30px] p-6 flex flex-col">
                <h2 className="text-orange-accent text-4xl font-medium mb-2">Zenith</h2>
                <p className="text-brand-cream text-xl leading-tight">
                  Optimised
                  <br />
                  risk-
                  <br />
                  reward
                  <br />
                  balance
                </p>
                <div className="flex-grow flex items-center justify-center">
                  <div className="relative w-40 h-40">
                    <Image
                      src="/placeholder.svg?height=160&width=160"
                      alt="Gear"
                      width={160}
                      height={160}
                      className="object-contain"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
