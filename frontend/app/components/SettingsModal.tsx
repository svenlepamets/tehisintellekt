import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { fetchSettings } from "@/app/api";
import { Service } from "@/app/types";

interface SettingsModalProps {
  open: boolean;
  onClose: () => void;
}

export const SettingsModal = ({ open, onClose }: SettingsModalProps) => {
  const [options, setOptions] = useState<Service[]>([]);
  const [optionsLoading, setOptionsLoading] = useState(true);
  const [selectedOption, setSelectedOption] = useState("");
  const [customText, setCustomText] = useState("tehisintellekt.ee");

  // Simulate fetching options from backend
  useEffect(() => {
    if (open) {
      setOptionsLoading(true);
      fetchSettings().then((settings) => {
        setOptions(settings.services)
      } ).finally(() => setOptionsLoading(false));
    }
  }, [open]);

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedOption = localStorage.getItem("settings.service");
    const savedText = localStorage.getItem("settings.domain");

    if (savedOption) setSelectedOption(savedOption);
    if (savedText) setCustomText(savedText);
  }, []);

  const saveSettings = () => {
    localStorage.setItem("settings.service", selectedOption);
    localStorage.setItem("settings.domain", customText);
    onClose();
  };

  const cancelSettings = () => {
    const savedOption = localStorage.getItem("settings.service");
    const savedText = localStorage.getItem("settings.domain");

    setSelectedOption(savedOption || "");
    setCustomText(savedText || "");

    onClose();
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 bg-black/10 backdrop-blur-sm flex justify-center items-center z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="bg-white p-6 rounded-lg shadow-lg w-96"
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            layout // <- smooth layout transitions
          >
            {/* Header */}
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Settings</h2>
              <button
                onClick={onClose}
                className="text-gray-500 hover:text-gray-800 text-xl leading-none"
              >
                ×
              </button>
            </div>

            {/* Content */}
            <div className="text-gray-600 text-sm space-y-4">
              {/* Dropdown */}
              <div className="flex flex-col">
                <label className="text-sm font-medium mb-1 font-semibold">
                  Select an AI service & model
                </label>

                <div className="relative">
                  {/* Loading overlay */}
                  <div
                    className={`absolute inset-0 flex items-center px-2 text-gray-500 text-sm italic bg-white/70 backdrop-blur-sm rounded-md pointer-events-none transition-opacity ${
                      optionsLoading ? "opacity-100" : "opacity-0"
                    }`}
                  >
                    Loading…
                  </div>

                  <select
                    disabled={optionsLoading}
                    value={selectedOption}
                    onChange={(e) => setSelectedOption(e.target.value)}
                    className="border rounded-md p-2 w-full bg-white appearance-none"
                  >
                    <option value="" disabled>-- Choose --</option>
                    {options.map((opt) => (
                      <option key={opt.service} value={opt.service}>
                        {opt.name}
                      </option>
                    ))}
                  </select>

                  {/* Optional custom arrow */}
                  <div className="pointer-events-none absolute top-0 right-0 h-full flex items-center pr-2">
                    <svg
                      className="w-4 h-4 text-gray-500"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Text Input */}
              <div className="flex flex-col">
                <label className="text-sm font-medium mb-1 font-semibold">Define a domain</label>
                <input
                  type="text"
                  value={customText}
                  onChange={(e) => setCustomText(e.target.value)}
                  className="border rounded-md p-2"
                  placeholder="Enter something…"
                />
              </div>

              {/* Buttons */}
              <div className="flex justify-end gap-3 mt-4">
                <button
                  onClick={cancelSettings}
                  className="px-4 py-2 rounded-md bg-gray-300 hover:bg-gray-400 transition"
                >
                  Cancel
                </button>

                <button
                  onClick={saveSettings}
                  className="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition"
                >
                  Save
                </button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
