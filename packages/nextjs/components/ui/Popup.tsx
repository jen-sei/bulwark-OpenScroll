"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";

interface PopupProps {
  isOpen: boolean;
  onClose: () => void;
}

const socialLinks = [
  { icon: "/social/1.svg", url: "https://twitter.com/bulwark_defi", name: "Twitter" },
  { icon: "/social/2.svg", url: "https://discord.gg/bulwark", name: "Discord" },
  { icon: "/social/3.svg", url: "https://t.me/bulwark_defi", name: "Telegram" },
  { icon: "/social/4.svg", url: "mailto:info@bulwark.finance", name: "Email" },
];

const Popup: React.FC<PopupProps> = ({ isOpen, onClose }) => {
  const popupRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === "Escape" && isOpen) {
        onClose();
      }
    };

    document.addEventListener("keydown", handleEscKey);
    return () => {
      document.removeEventListener("keydown", handleEscKey);
    };
  }, [isOpen, onClose]);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (popupRef.current && !popupRef.current.contains(event.target as Node) && isOpen) {
        onClose();
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const title = "Your Agent is Deployed!";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        ref={popupRef}
        className="relative rounded-xl p-6 max-w-md w-full mx-4 z-10 shadow-xl animate-fadeIn overflow-hidden px-10 py-16"
        style={{
          // backgroundColor: "rgba(255, 255, 255, 0.1)",
          backdropFilter: "blur(71.5px)", // Blur only what's behind this div
          WebkitBackdropFilter: "blur(71.5px)",
        }}
      >
        <div
          className="absolute inset-0 bg-cover bg-center opacity-20 z-0"
          style={{ backgroundImage: 'url("/img/confirmation_bg.png")' }}
        />

        <div className="relative z-10 flex flex-col items-center">
          <h2 className="text-5xl md:text-7xl text-brand-gray/80 font-sztos border-b-2 border-brand-gray/50 pb-4 text-center">
            Your Agent is <br />
            Deployed!
          </h2>

          <button
            onClick={onClose}
            className="mt-8 inline-block bg-brand-darkgray hover:bg-brand-darkgray/80 text-white py-1 px-12 rounded-full text-xl transition-all animate-glow-gray border-2 border-black font-inter font-semibold"
          >
            done
          </button>

          <p className="text-black font-inter font-light text-xl mt-8">Let your friends know!</p>
          <div className="flex justify-center space-x-4 mb-6">
            {socialLinks.map((social, index) => (
              <a
                key={index}
                href={social.url}
                target="_blank"
                rel="noopener noreferrer"
                className="transition-transform hover:scale-110"
                title={social.name}
              >
                <Image src={social.icon} alt={social.name} width={32} height={32} />
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Popup;
