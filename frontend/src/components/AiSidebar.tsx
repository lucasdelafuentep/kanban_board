"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, X, Sparkles } from "lucide-react";
import clsx from "clsx";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type AiSidebarProps = {
  isOpen: boolean;
  onClose: () => void;
  onBoardUpdate: () => void;
};

export const AiSidebar = ({ isOpen, onClose, onBoardUpdate }: AiSidebarProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    const newMessages: Message[] = [...messages, { role: "user", content: userMessage }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const response = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: newMessages }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages((prev) => [...prev, { role: "assistant", content: data.message }]);
        
        // If the AI performed actions, notify the parent to refresh the board
        if (data.actions && data.actions.length > 0) {
          onBoardUpdate();
        }
      } else {
        setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I encountered an error. Please try again." }]);
      }
    } catch (error) {
      console.error("AI chat error:", error);
      setMessages((prev) => [...prev, { role: "assistant", content: "Connection error. Is the backend running?" }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 right-0 z-50 w-[400px] transform border-l border-[var(--stroke)] bg-white shadow-2xl transition-transform duration-300 ease-in-out",
        isOpen ? "translate-x-0" : "translate-x-full"
      )}
    >
      <div className="flex h-full flex-col">
        <header className="flex items-center justify-between border-b border-[var(--stroke)] p-4 bg-[var(--surface)]">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-[var(--accent-yellow)]" />
            <h2 className="font-display text-lg font-bold text-[var(--navy-dark)]">AI Assistant</h2>
          </div>
          <button
            onClick={onClose}
            data-testid="close-sidebar"
            className="rounded-full p-2 hover:bg-[var(--stroke)] transition"
          >
            <X className="h-5 w-5 text-[var(--gray-text)]" />
          </button>
        </header>

        <div
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-4 space-y-4"
        >
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-4 px-6">
              <div className="h-16 w-16 rounded-full bg-[var(--surface)] flex items-center justify-center">
                <Bot className="h-8 w-8 text-[var(--primary-blue)]" />
              </div>
              <div>
                <p className="font-semibold text-[var(--navy-dark)]">How can I help today?</p>
                <p className="text-sm text-[var(--gray-text)] mt-1">
                  You can ask me to add cards, move them around, or rename columns.
                </p>
              </div>
            </div>
          )}
          {messages.map((msg, i) => (
            <div
              key={i}
              className={clsx(
                "flex gap-3",
                msg.role === "user" ? "flex-row-reverse" : "flex-row"
              )}
            >
              <div className={clsx(
                "h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0",
                msg.role === "user" ? "bg-[var(--secondary-purple)]" : "bg-[var(--primary-blue)]"
              )}>
                {msg.role === "user" ? <User className="h-5 w-5 text-white" /> : <Bot className="h-5 w-5 text-white" />}
              </div>
              <div className={clsx(
                "max-w-[80%] rounded-2xl px-4 py-2 text-sm",
                msg.role === "user" ? "bg-[var(--secondary-purple)] text-white" : "bg-[var(--surface)] text-[var(--navy-dark)]"
              )}>
                {msg.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-3">
              <div className="h-8 w-8 rounded-full bg-[var(--primary-blue)] flex items-center justify-center">
                <Bot className="h-5 w-5 text-white" />
              </div>
              <div className="bg-[var(--surface)] rounded-2xl px-4 py-2 text-sm text-[var(--gray-text)] animate-pulse">
                Thinking...
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSend} className="p-4 border-t border-[var(--stroke)] bg-[var(--surface)]">
          <div className="relative">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a command..."
              data-testid="ai-input"
              className="w-full rounded-full border border-[var(--stroke)] bg-white pl-4 pr-12 py-3 text-sm focus:border-[var(--primary-blue)] outline-none transition shadow-sm"
              disabled={isLoading}
            />
            <button
              type="submit"
              data-testid="ai-send"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 top-1.5 rounded-full bg-[var(--secondary-purple)] p-2 text-white disabled:opacity-50 transition hover:brightness-110"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </form>
      </div>
    </aside>
  );
};
