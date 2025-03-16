"use client";

// @refresh reset
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Balance } from "../Balance";
import { AddressInfoDropdown } from "./AddressInfoDropdown";
import { AddressQRCodeModal } from "./AddressQRCodeModal";
import { WrongNetworkDropdown } from "./WrongNetworkDropdown";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import { Address } from "viem";
import { useAccount } from "wagmi";
import { useTargetNetwork } from "~~/hooks/scaffold-eth/useTargetNetwork";
import { getBlockExplorerAddressLink } from "~~/utils/scaffold-eth/networks";

/**
 * Custom Wagmi Connect Button (watch balance + custom design)
 */
export const RainbowKitCustomConnectButton = ({
  title,
  secondary = false,
  full = false,
  networkColor = "#000000",
}: {
  title: string;
  secondary?: boolean;
  full?: boolean;
  networkColor?: string;
}) => {
  // const networkColor = useNetworkColor();
  const { targetNetwork } = useTargetNetwork();
  const router = useRouter();
  const { address, chain } = useAccount();

  // Use refs to track previous state
  // Track if a user action has been taken
  const [userActionTaken, setUserActionTaken] = useState(false);
  const prevAddressRef = useRef<string | undefined>(undefined);
  const prevChainIdRef = useRef<number | undefined>(undefined);

  // Handle connect modal opening
  const handleConnectClick = () => {
    setUserActionTaken(true);
  };

  useEffect(() => {
    // Store previous values for comparison
    const prevAddress = prevAddressRef.current;
    // const prevChainId = prevChainIdRef.current;

    // Update refs with current values for next comparison
    prevAddressRef.current = address;
    prevChainIdRef.current = chain?.id;

    // Only proceed if user has taken an action and we have both address and chain
    if (userActionTaken && address && chain) {
      console.log("userActionTaken", userActionTaken);
      const isCorrectNetwork = chain.id === targetNetwork.id;
      // const wasIncorrectNetwork = prevChainId !== undefined && prevChainId !== targetNetwork.id;
      const addressChanged = prevAddress !== address;

      // Navigate only if:
      // 1. Network changed from incorrect to correct, OR
      // 2. Address changed (new connection) and network is correct
      if (isCorrectNetwork || (addressChanged && isCorrectNetwork && prevAddress === undefined)) {
        console.log("Wallet connection changed to correct network after user action, navigating to agents page");
        router.push("/agents");
        // Reset the user action flag after navigation
        setUserActionTaken(false);
      }
    }
  }, [address, chain, targetNetwork.id, router, userActionTaken]);

  const goToApp = () => {
    router.push("/agents");
  };

  const classNameBase =
    "self-start text-white py-3 px-12 rounded-full text-xl transition-all border-2 font-inter font-semibold";
  const className = secondary
    ? `${classNameBase} bg-brand-darkgray hover:bg-brand-darkgray/80 animate-glow-gray border-black`
    : `${classNameBase} bg-brand-orange-accent hover:bg-brand-orange-accent/80 animate-glow-orange border-[#D3673A]`;

  return (
    <ConnectButton.Custom>
      {({ account, chain, openConnectModal, mounted }) => {
        const connected = mounted && account && chain;
        const blockExplorerAddressLink = account
          ? getBlockExplorerAddressLink(targetNetwork, account.address)
          : "https://etherscan.io/address/";

        return (
          <>
            {(() => {
              if (!connected) {
                return (
                  <button
                    onClick={() => {
                      handleConnectClick();
                      openConnectModal();
                    }}
                    type="button"
                    className={className}
                  >
                    {title}
                  </button>
                );
              }

              if (chain.unsupported || chain.id !== targetNetwork.id) {
                if (!userActionTaken) {
                  setUserActionTaken(true);
                }
                return <WrongNetworkDropdown />;
              }

              return (
                <>
                  {full ? (
                    <>
                      <div className="flex flex-col items-center mr-1">
                        <Balance address={account.address as Address} className="min-h-0 h-auto" />
                        <span className="text-xs text-white">{chain.name}</span>
                      </div>
                      <AddressInfoDropdown
                        address={account.address as Address}
                        displayName={account.displayName}
                        ensAvatar={account.ensAvatar}
                        blockExplorerAddressLink={blockExplorerAddressLink}
                      />
                      <AddressQRCodeModal address={account.address as Address} modalId="qrcode-modal" />
                    </>
                  ) : (
                    <button onClick={goToApp} className={className}>
                      {title}
                    </button>
                  )}
                </>
              );
            })()}
          </>
        );
      }}
    </ConnectButton.Custom>
  );
};
