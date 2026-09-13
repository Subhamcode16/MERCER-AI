"use client";

import React from "react";
import { VyrenRoomView } from "@/components/room/VyrenRoomView";

export default function HomePage() {
  return (
    <div className="h-full min-h-0 flex-1 flex flex-col overflow-hidden">
      <VyrenRoomView />
    </div>
  );
}
