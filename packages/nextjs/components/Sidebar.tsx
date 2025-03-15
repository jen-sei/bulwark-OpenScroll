"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface MenuItem {
  icon: string;
  label: string;
  path: string;
}

const menuItems: MenuItem[] = [
  { icon: "/icons/star.svg", label: "Agents", path: "/agents" },
  { icon: "/icons/square.svg", label: "Portfolio", path: "/portfolio" },
  { icon: "/icons/circle.svg", label: "Ask", path: "/ask" },
  { icon: "/icons/triangle.svg", label: "Governance", path: "/governance" },
  { icon: "/icons/chevron-right.svg", label: "Developers", path: "/developers" },
];

const Sidebar = () => {
  const pathname = usePathname();

  return (
    <div className="w-64 border-r border-neutral-800 flex flex-col">
      {/* Logo */}
      <Link href="/" className="p-4 mb-6 mt-2">
        <Image src="/logo.png" alt="BULWARK" width={150} height={40} className="h-auto w-auto dark:invert" priority />
      </Link>

      {/* Search */}
      <div className="px-4 mb-6">
        <div className="relative">
          <input
            type="text"
            placeholder="Search..."
            className="w-full bg-neutral-900/50 text-gray-300 rounded-md py-2 px-4 pr-10 border border-neutral-800 focus:outline-none focus:ring-1 focus:ring-neutral-700"
          />
          <Image
            src="/icons/search.svg"
            alt="Search"
            width={16}
            height={16}
            className="absolute right-3 top-2.5 h-4 w-4 text-gray-500"
          />
        </div>
      </div>

      <div className="px-4 pt-2 pb-6 border-b border-neutral-800">
        <div className="text-xs font-semibold text-neutral-500 mb-4">MENU</div>

        {/* Menu items */}
        <div className="space-y-1">
          {menuItems.map(item => {
            const isActive = pathname === item.path;

            return (
              <Link
                key={item.path}
                href={item.path}
                className={`flex items-center p-3 rounded-md cursor-pointer transition-colors ${
                  isActive
                    ? "bg-gradient-to-r from-orange-600/80 to-orange-500/50 text-white"
                    : "text-neutral-400 hover:bg-neutral-800/50"
                }`}
              >
                <Image
                  src={item.icon}
                  alt={item.label}
                  width={20}
                  height={20}
                  className={`h-5 w-5 mr-3 ${isActive ? "text-white" : ""}`}
                />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
