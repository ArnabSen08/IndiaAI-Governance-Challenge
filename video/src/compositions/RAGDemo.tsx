import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const RAGDemo: React.FC = () => {
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
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        opacity,
      }}
    >
      <div style={{ fontSize: 80, fontWeight: "bold", color: "white", marginBottom: 20 }}>
        Ready Tensor RAG
      </div>
      <div style={{ fontSize: 48, color: "rgba(255,255,255,0.9)", marginBottom: 40 }}>
        Retrieval-Augmented Generation
      </div>
      <div style={{ fontSize: 36, color: "white", textAlign: "center", maxWidth: "80%" }}>
        • 94% Retrieval Success
        <br />
        • 89% Answer Accuracy
        <br />
        • 1.2s Average Latency
      </div>
    </AbsoluteFill>
  );
};
