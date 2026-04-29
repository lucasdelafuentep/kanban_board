"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { KanbanBoard } from "@/components/KanbanBoard";

export default function Home() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuth = () => {
      const auth = localStorage.getItem("auth");
      if (!auth) {
        router.push("/login");
        return;
      }
      
      // Only proceed if we're on the correct port (8000) or localhost
      const isLocalhost = window.location.hostname === "localhost";
      const correctPort = window.location.port === "8000" || !window.location.port;
      
      if (isLocalhost && !correctPort) {
        // If served through backend on different port, force redirect to correct URL
        router.replace(`http://localhost:3000${window.location.pathname}`);
        return;
      }
      
      setIsAuthenticated(auth === "true");
    };
    
    checkAuth();
    
    // Listen for auth changes
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === "auth") {
        setIsAuthenticated(e.newValue === "true");
        if (e.newValue !== "true") {
           router.push("/login");
        }
      }
    };
    
    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, [router]);

  // Don't render anything until we've confirmed authentication
  if (isAuthenticated !== true) {
    return null;
  }

  return <KanbanBoard />;
}
