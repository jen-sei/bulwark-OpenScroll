"use client";

import React, { useEffect } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { RainbowKitCustomConnectButton } from "./scaffold-eth/RainbowKitCustomConnectButton";
import { useAccount } from "wagmi";

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

const Header: React.FC<HeaderProps> = ({ title = "Overview", subtitle = "Agents" }) => {
  const router = useRouter();
  const { isConnected, isDisconnected } = useAccount();

  console.log("isConnected", isConnected);
  console.log("isDisconnected", isDisconnected);

  useEffect(() => {
    if (!isConnected) {
      console.log("Wallet disconnected, redirecting to home page");
      router.push("/");
    }
  }, [isConnected, router]);

  return (
    <header className="h-[84px] border-b border-neutral-800 flex items-center justify-between px-6">
      <div className="flex items-center text-gray-400 text-lg">
        <Image src="/icons/star.svg" alt="Star" width={20} height={20} className="h-5 w-5 mr-2 text-neutral-500" />
        <span className="text-neutral-500">{subtitle} /</span>
        <span className="ml-2 text-white">{title}</span>
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
