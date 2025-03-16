"use client";

import { useState } from "react";
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
  { icon: "/icons/arrow.svg", label: "Developers", path: "/developers" },
];

const Sidebar = () => {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      {/* Mobile Menu Button - Only visible on small screens */}
      <div className="md:hidden fixed top-4 left-4 z-30">
        <button
          onClick={toggleMobileMenu}
          className="p-4 rounded-md bg-neutral-900 border border-neutral-800 text-brand-orange-accent"
        >
          <Image
            src={isMobileMenuOpen ? "/icons/close.svg" : "/favicon.png"}
            alt="Menu"
            width={24}
            height={24}
            className="h-6 w-6"
          />
        </button>
      </div>

      {/* Mobile Logo - Only visible on small screens when menu is closed */}
      {/* <div className="md:hidden fixed top-4 left-1/2 transform -translate-x-1/2 z-20">
        {!isMobileMenuOpen && (
          <Link href="/">
            <Image
              src="/logo.png"
              alt="BULWARK"
              width={120}
              height={32}
              className="h-auto w-auto dark:invert"
              priority
            />
          </Link>
        )}
      </div> */}

      {/* Sidebar - Hidden on mobile by default, shown when menu is open */}
      <div
        className={`
          fixed inset-0 z-20 transition-transform duration-300 ease-in-out md:relative md:translate-x-0 md:h-screen
          ${isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        <div className="w-full h-full md:w-64 md:min-h-screen bg-black border-r border-neutral-800 flex flex-col sticky top-0">
          {/* Logo */}
          <div className="flex justify-end md:justify-start p-4 mb-6 mt-2">
            <Link href="/" className="block">
              <Image
                src="/logo.png"
                alt="BULWARK"
                width={150}
                height={40}
                className="h-auto w-auto dark:invert"
                priority
              />
            </Link>

            {/* Close button - Only visible on mobile */}
            {/* <button onClick={toggleMobileMenu} className="md:hidden p-2">
              <Image src="/icons/close.svg" alt="Close" width={24} height={24} className="h-6 w-6" />
            </button> */}
          </div>

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
                    onClick={() => setIsMobileMenuOpen(false)} // Close menu when item is clicked on mobile
                    className={`flex items-center p-3 rounded-md cursor-pointer transition-colors ${
                      isActive
                        ? "bg-gradient-to-r from-[#F66435] to-[#29292B] text-white"
                        : "text-neutral-400 hover:bg-neutral-800/50"
                    }`}
                  >
                    <Image
                      src={item.icon}
                      alt={item.label}
                      width={20}
                      height={20}
                      className={`h-5 w-5 mr-3 text-white`}
                    />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Add a flex-grow div to push content to the top */}
          <div className="flex-grow"></div>
        </div>
      </div>

      {/* Overlay - Only visible on mobile when menu is open */}
      {isMobileMenuOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-10"
          onClick={() => setIsMobileMenuOpen(false)}
        ></div>
      )}
    </>
  );
};

export default Sidebar;
