"use client";

import { ReactNode, useEffect, useState } from "react";
import { CloudIcon } from "@heroicons/react/24/outline";
import { motion, AnimatePresence } from "framer-motion";
import { checkHealth } from "@/app/api";

interface InitLoaderProps {
  children: ReactNode;
}

// Loader configuration
const MIN_LOADING_TIME = 500;  // ms loader must be visible

export default function InitLoader({ children }: InitLoaderProps) {
  const [apiReady, setApiReady] = useState<boolean>(false);
  const [showLoader, setShowLoader] = useState<boolean>(true);

  useEffect(() => {
    const startTime = Date.now();

    const checkApi = async () => {
      for (let i = 0; i < 5; i++) {
        try {
          const res = await checkHealth();
          if (res.status) {
              // Ensure loader stays visible for MIN_LOADING_TIME
              const elapsed = Date.now() - startTime;
              const remaining = MIN_LOADING_TIME - elapsed;
              if (remaining > 0) await new Promise(r => setTimeout(r, remaining));

              setApiReady(true);
              setShowLoader(false);
              break;
          }
        } catch {}
        await new Promise(r => setTimeout(r, 3000));
      }
    };

    checkApi();
  }, []);

  return (
    <>
      <AnimatePresence>
        {showLoader && !apiReady && (
          <motion.div
            className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-gray-900 bg-opacity-80 text-white"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <motion.div
              className="text-6xl mb-4"
              animate={{ y: [0, -20, 0] }}
              transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut" }}
            >
              🤖
            </motion.div>

            <motion.p
              className="text-lg font-semibold"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              Starting the app...
            </motion.p>

            <motion.p
              className="mt-2 text-sm text-gray-300"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              This may take a few seconds.
            </motion.p>
          </motion.div>
        )}
      </AnimatePresence>

      {apiReady && children}
    </>
  );
}
