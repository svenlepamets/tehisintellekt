"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import { TrashIcon } from "@heroicons/react/24/outline";
import { SettingsModal } from "@/app/components/SettingsModal";
import { QA } from "@/app/types";
import { postQuestion } from "@/app/api";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<QA[]>([]);
  const [error, setError] = useState("");
  const [settingsOpen, setSettingsOpen] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const saved = localStorage.getItem("chat_history");
    if (saved) setHistory(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem("chat_history", JSON.stringify(history));
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  function getTimestamp(base: number) {
    const now = new Date(base*1000);

    const time = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    const date = now.toLocaleDateString([], {
      year: "numeric",
      month: "short", // "Nov"
      day: "numeric",
    });

    return `${date} • ${time}`;
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setTimeout(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 10)
    setError("");

    try {
      const domain = localStorage.getItem("settings.domain") || ""
      const service = localStorage.getItem("settings.service") || ""
      const answer = await postQuestion(question, domain, service)

      const newEntry: QA = {
        question,
        answer: answer
      };

      setHistory((prev) => [...prev, newEntry]);
      setQuestion("");
    } catch (err: any) {
      setError(err.message ?? "Unknown error");
    }

    setLoading(false);
    setTimeout(() => inputRef.current?.focus(), 10);
  }

  function clearHistory() {
    if (confirm("Are you sure you want to clear the chat history?")) {
      setHistory([]);
      localStorage.removeItem("chat_history");
      setTimeout(() => inputRef.current?.focus(), 10);
    }
  }

  const Thinking = () => (
    <motion.div
      initial={{ opacity: 0.3 }}
      animate={{ opacity: [0.3, 1, 0.3] }}
      transition={{ repeat: Infinity, duration: 1.5 }}
      className="text-gray-500 text-sm italic"
    >
      AI is thinking…
    </motion.div>
  );

  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <div className="w-full max-w-3xl flex flex-col bg-white shadow-lg rounded-lg h-[90vh]">
        {/* Header */}
        <div className="p-4 border-b bg-blue-600 text-white rounded-t-lg flex items-center justify-between">
          <h1 className="text-lg font-semibold">Questions & answers with AI 🤖</h1>

          <button
            onClick={() => setSettingsOpen(true)}
            className="p-2 rounded-md hover:bg-blue-700 transition"
            aria-label="Open Settings"
          >
            <Cog6ToothIcon className="h-6 w-6 text-white" />
          </button>
        </div>
        
        {/* Chat history */}
        <div className="flex-1 p-4 space-y-4 overflow-y-auto">
          {history.length === 0 && (
            <p className="text-gray-500 text-center mt-4">
              No messages yet. Start by asking a question!
            </p>
          )}
          <AnimatePresence>
            {history.map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -40 }}
                transition={{ duration: 0.8 }}
                className="flex flex-col bg-gray-50 border rounded-xl p-4 shadow-sm space-y-2"
              >
                <div className="bg-blue-600 text-white p-3 rounded-lg max-w-full">
                  {item.question}
                </div>
                <div className="bg-gray-200 text-gray-800 p-3 rounded-lg max-w-full">
                  <pre className="whitespace-pre-wrap">{item.answer.answer}</pre>
                </div>
                <div className="text-xs text-gray-500 text-right">{getTimestamp(item.answer.timestamp)} / {item.answer.source} / {item.answer.domain} </div>
              </motion.div>
            ))}
          </AnimatePresence>
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 p-3 rounded-lg max-w-full">
                <Thinking />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input area + Clear History */}
        <div className="flex border-t border-gray-200 bg-gray-50 p-4 gap-2">
          <form onSubmit={onSubmit} className="flex flex-1 gap-2">
            <input
              ref={inputRef}
              type="text"
              placeholder="Type your question..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring focus:ring-blue-200 outline-none"
              disabled={loading}
              maxLength={120}
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "..." : "Send"}
            </button>
          </form>
          <button
            onClick={clearHistory}
            disabled={loading}
            className="p-3 rounded-md bg-red-500 hover:bg-red-600 disabled:opacity-50 transition"
            aria-label="Clear History"
          >
            <TrashIcon className="h-6 w-6 text-white" />
          </button>

        </div>

        {/* Error message */}
        {error && (
          <div className="p-3 bg-red-100 text-red-800 text-center">
            ⚠️ {error}
          </div>
        )}
      </div>
      <SettingsModal open={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </main>
  );
}
