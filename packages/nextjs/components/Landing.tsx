import Description from "./Description";
import Features from "./Features";
import Hero from "./Hero";

export default function Home() {
  return (
    <div className="min-h-screen container mx-auto px-4 pt-12 pb-1 relative z-10 flex flex-col items-center">
      <Hero />
      <Description />
      <Features />
      <p className="text-brand-cream text-xs md:text-sm text-center font-inter font-light px-2 py-0 mb-1">
        Built in public with ♥ during Open Scroll Hackathon 2025
      </p>
    </div>
  );
}
