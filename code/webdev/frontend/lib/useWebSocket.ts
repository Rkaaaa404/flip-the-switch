// frontend/lib/useWebSocket.ts
"use client";

import { useEffect, useState } from "react";
import { InspectionResult } from "@/types";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/events";

export function useInspectionWebSocket(onNewInspection?: (data: InspectionResult) => void) {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    let ws: WebSocket | null = null;
    let timer: NodeJS.Timeout | null = null;

    function connect() {
      try {
        ws = new WebSocket(WS_URL);

        ws.onopen = () => {
          setIsConnected(true);
        };

        ws.onmessage = (event) => {
          try {
            const payload = JSON.parse(event.data);
            if (payload.event === "NEW_INSPECTION" && onNewInspection) {
              onNewInspection(payload.data);
            }
          } catch (e) {
            console.error("Failed to parse WebSocket message", e);
          }
        };

        ws.onclose = () => {
          setIsConnected(false);
          timer = setTimeout(connect, 3000); // Reconnect automatically
        };
      } catch (err) {
        setIsConnected(false);
      }
    }

    connect();

    return () => {
      if (timer) clearTimeout(timer);
      if (ws) ws.close();
    };
  }, [onNewInspection]);

  return { isConnected };
}