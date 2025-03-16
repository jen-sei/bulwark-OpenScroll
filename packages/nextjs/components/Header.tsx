"use client";

import React, { useEffect } from "react";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import { RainbowKitCustomConnectButton } from "./scaffold-eth/RainbowKitCustomConnectButton";
import { useAccount } from "wagmi";

interface HeaderProps {
  title: string;
  subtitle: string;
}

const Header: React.FC<HeaderProps> = ({ title, subtitle }) => {
  const router = useRouter();
  const pathname = usePathname();
  const { isConnected, isDisconnected } = useAccount();

  useEffect(() => {
    if (!isConnected) {
      console.log("Wallet disconnected, redirecting to home page");
      router.push("/");
    }
  }, [isConnected, router]);

  // Map routes to their corresponding icons
  const routeIcons: Record<string, string> = {
    "/agents": "/icons/star.svg",
    "/portfolio": "/icons/square.svg",
    "/ask": "/icons/circle.svg",
    "/governance": "/icons/triangle.svg",
    "/developers": "/icons/arrow.svg",
    // Add fallback for unknown routes
    default: "/icons/star.svg",
  };

  // Get the icon for the current route, or use default if not found
  const currentIcon = routeIcons[pathname] || routeIcons.default;

  return (
    <header className=" border-b border-neutral-800 flex flex-col md:flex-row items-center justify-end md:justify-between px-2 md:px-6 py-6">
      <div className="flex items-center text-gray-400 text-lg pb-8 md:pb-0">
        <Image src={currentIcon} alt={title} width={20} height={20} className="h-5 w-5 mr-2 text-neutral-500" />
        <div className="flex flex-row">
          <span className="text-neutral">{title} </span>
          <span className="text-neutral mx-2"> / </span>
          <span className="text-neutral-400">{subtitle}</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative">
          <Image src="/icons/bell.png" alt="Bell" width={20} height={20} className="h-5 w-5 text-neutral-400" />
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-orange-500 rounded-full flex items-center justify-center text-[10px]">
            1
          </span>
        </div>
        <RainbowKitCustomConnectButton title="connect wallet" full />
      </div>
    </header>
  );
};

export default Header;
