"use client";

import React, { Fragment, useRef, useState } from "react";
import Modal from "./Modal";

const IframeLoader = () => {
  const IFRAME_HEIGHT = 650;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedIframeUrl, setSelectedIframeUrl] = useState("");

  const urls = useRef<string[]>([
    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev/artifact-202507140913-5b30/index.html",
    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev/artifact-202507140913-9f45/index.html",
    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev/artifact-202507140913-e5e2/index.html",
  ]);

  const handleIframeClick = (url: string) => {
    setSelectedIframeUrl(url);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedIframeUrl("");
  };

  return (
    <>
      <div className="h-2/3 grid">
        <div className="grid grid-cols-3 items-center gap-6">
          {urls &&
            urls.current.map((url: string) => (
              <Fragment key={url}>
                <div className="flex flex-col gap-2">
                  <h1 className="text-2xl font-semibold text-gray-800">
                    KPI-Driven Financial Overview Dashboard
                  </h1>
                  <figure
                    className="relative aspect-[16/9] overflow-hidden rounded-lg border border-gray-500 shadow-sm cursor-pointer transition-all duration-300 hover:shadow-xl  hover:border-gray-400 hover:-translate-y-1"
                    onClick={() => handleIframeClick(url)}
                  >
                    <iframe
                      src={url}
                      title="Generated Component"
                      sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms"
                      width="1200px"
                      height={IFRAME_HEIGHT}
                      loading="eager"
                      className="absolute left-0 top-0 origin-top-left pointer-events-none"
                      style={{
                        colorScheme: "normal",
                        border: "none",
                        transform: "scale(0.615)",
                      }}
                    />

                    <div className="absolute inset-0 bg-black/50 transition-all duration-300 flex items-center justify-center opacity-0 hover:opacity-100">
                      <p className="text-white font-bold text-2xl">
                        Click for preview
                      </p>
                    </div>
                  </figure>

                  <div className="w-full flex items-center justify-center mt-12">
                    <button className="text-gray-500 font-semibold bg-gray-300 border border-gray-500 rounded-lg px-4 py-1 shadow-md cursor-pointer hover:bg-white hover:shadow-xl transition-all duration-150 ease-in-out">
                      Choose
                    </button>
                  </div>
                </div>
              </Fragment>
            ))}
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        iframeUrl={selectedIframeUrl}
      />
    </>
  );
};

export default IframeLoader;
