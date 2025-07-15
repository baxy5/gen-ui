"use client";
import React, { useState } from "react";
import IframeLoader from "./_components/IframeLoader";
import Chat from "./_components/Chat";

const IframePage = () => {
  const [isSwitched, setSwitched] = useState(false);

  return (
    <main className="bg-white">
      <div className="max-w-[1440px] m-auto h-screen py-4 px-2">
        <div
          className={`h-full flex gap-6 ${
            isSwitched ? "flex-col-reverse" : "flex-col"
          }`}
        >
          <Chat />
          <IframeLoader />
        </div>
      </div>
    </main>
  );
};

export default IframePage;
