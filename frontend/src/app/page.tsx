"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { KanbanBoard } from "@/components/KanbanBoard";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (localStorage.getItem("auth") !== "true") {
      router.push("/login");
    }
  }, [router]);

  if (typeof window !== "undefined" && localStorage.getItem("auth") !== "true") {
    return null;
  }

  return <KanbanBoard />;
}
