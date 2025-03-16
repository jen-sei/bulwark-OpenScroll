"use client";

// import Link from "next/link";
import type { NextPage } from "next";
// import { useAccount } from "wagmi";
// import { BugAntIcon, MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import Landing from "~~/components/Landing";

// import { Address } from "~~/components/scaffold-eth";

const Home: NextPage = () => {
  // const { address: connectedAddress } = useAccount();

  return (
    <div className="flex items-center flex-col flex-grow pt-10  bg-[url(/img/bg.png)] bg-cover bg-left md:bg-center">
      <Landing />
    </div>
  );
};

export default Home;
