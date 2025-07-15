"use client";

import React, { useEffect } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  iframeUrl: string;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, iframeUrl }) => {
  // Close modal on Escape key press
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      // Prevent body scroll when modal is open
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/80 transition-opacity duration-300 ease-in-out"
        onClick={onClose}
      />

      <div className="relative z-10 w-[90vw] h-[80vh] max-w-6xl mx-4 transform transition-all duration-300 ease-in-out animate-in fade-in-0 zoom-in-95">
        <button
          onClick={onClose}
          className="absolute -top-12 right-0 text-white hover:text-gray-300 transition-colors duration-200 z-20 bg-black bg-opacity-50 rounded-full w-10 h-10 flex items-center justify-center cursor-pointer"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>

        <div className="w-full h-full bg-white rounded-lg shadow-2xl overflow-hidden">
          <iframe
            src={iframeUrl}
            title="Generated Component - Expanded View"
            sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms"
            width="100%"
            height="100%"
            loading="eager"
            className="w-full h-full border-none"
            style={{
              colorScheme: "normal",
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default Modal;
