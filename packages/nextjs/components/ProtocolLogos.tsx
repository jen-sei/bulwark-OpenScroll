"use client";

import Image from "next/image";

interface Protocol {
  name: string;
  logo: string;
  url: string;
}

interface ProtocolLogosProps {
  className?: string;
  imageSize?: number;
}

const ProtocolLogos: React.FC<ProtocolLogosProps> = ({ className = "", imageSize = 40 }) => {
  const protocols: Protocol[] = [
    { name: "Scroll", logo: "/protocols/scroll.png", url: "https://scroll.io/" },
    { name: "Quill", logo: "/protocols/quill.png", url: "https://quillprotocol.com/" },
    { name: "Ambient", logo: "/protocols/ambient.webp", url: "https://ambient.finance/" },
    { name: "Aave", logo: "/protocols/aave.svg", url: "https://aave.com/" },
    { name: "USDC", logo: "/protocols/usdc.svg", url: "https://www.circle.com/en/usdc" },
    { name: "Safe", logo: "/protocols/safe.webp", url: "https://safe.global/" },
  ];

  return (
    <div className={`flex flex-row flex-wrap items-center justify-center gap-4 md:gap-8 mb-2 md:mb-6 ${className}`}>
      {protocols.map(protocol => (
        <a
          key={protocol.name}
          href={protocol.url}
          target="_blank"
          rel="noopener noreferrer"
          className="transition-transform hover:scale-110"
          title={protocol.name}
        >
          <div className="bg-transparent rounded-full">
            <Image
              src={protocol.logo}
              alt={protocol.name}
              width={imageSize}
              height={imageSize}
              className="h-10 w-auto object-contain"
            />
          </div>
        </a>
      ))}
    </div>
  );
};

export default ProtocolLogos;
