"use client";

import type { NextPage } from "next";
import Landing from "~~/components/Landing";

const Home: NextPage = () => {
  return (
    <div className="flex items-center flex-col flex-grow pt-10  bg-[url(/img/bg.png)] bg-cover bg-left md:bg-center">
      <Landing />
    </div>
  );
};

export default Home;
