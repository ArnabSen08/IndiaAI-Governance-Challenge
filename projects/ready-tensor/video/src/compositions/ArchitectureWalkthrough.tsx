import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const ArchitectureWalkthrough: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const fadeIn = interpolate(frame, [0, 30], [0, 1], { extrapolateLeft: "clamp" });
  const fadeOut = interpolate(frame, [durationInFrames - 30, durationInFrames], [1, 0], {
    extrapolateRight: "clamp",
  });
  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        opacity,
        padding: 40,
        color: "white",
      }}
    >
      <div style={{ fontSize: 64, fontWeight: "bold", marginBottom: 40 }}>
        System Architecture
      </div>
      <div style={{ fontSize: 32, marginBottom: 20 }}>
        1️⃣ User Query
      </div>
      <div style={{ fontSize: 40, color: "#667eea", margin: "20px 0" }}>
        ⬇
      </div>
      <div style={{ fontSize: 32, marginBottom: 20 }}>
        2️⃣ Vector Search & Retrieval
      </div>
      <div style={{ fontSize: 40, color: "#667eea", margin: "20px 0" }}>
        ⬇
      </div>
      <div style={{ fontSize: 32, marginBottom: 20 }}>
        3️⃣ Context Assembly
      </div>
      <div style={{ fontSize: 40, color: "#667eea", margin: "20px 0" }}>
        ⬇
      </div>
      <div style={{ fontSize: 32, marginBottom: 20 }}>
        4️⃣ LLM Response
      </div>
      <div style={{ fontSize: 40, color: "#667eea", margin: "20px 0" }}>
        ⬇
      </div>
      <div style={{ fontSize: 32, color: "#4ade80", fontWeight: "bold" }}>
        ✅ Accurate Answer
      </div>
      <div style={{ marginTop: 60, padding: 30, background: "rgba(102, 126, 234, 0.1)", fontSize: 20 }}>
        • 1,234ms end-to-end latency
        <br />
        • 94% retrieval success
        <br />
        • 89% answer accuracy
      </div>
    </AbsoluteFill>
  );
};
