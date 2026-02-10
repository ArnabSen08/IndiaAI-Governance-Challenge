import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const DeploymentGuide: React.FC = () => {
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
        background: "linear-gradient(135deg, #0f3460 0%, #1a5f7a 100%)",
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
        Deployment Guide
      </div>

      <div style={{ fontSize: 32, marginBottom: 20 }}>
        Step 1: Clone Repository
      </div>
      <div
        style={{
          fontSize: 24,
          color: "#4ade80",
          background: "rgba(0,0,0,0.3)",
          padding: "15px 25px",
          borderRadius: 8,
          marginBottom: 30,
        }}
      >
        git clone https://github.com/ArnabSen08/ready-tensor.git
      </div>

      <div style={{ fontSize: 32, marginBottom: 20 }}>
        Step 2: Docker Deployment
      </div>
      <div
        style={{
          fontSize: 24,
          color: "#4ade80",
          background: "rgba(0,0,0,0.3)",
          padding: "15px 25px",
          borderRadius: 8,
          marginBottom: 30,
        }}
      >
        docker-compose up -d
      </div>

      <div style={{ fontSize: 32, marginBottom: 20 }}>
        Step 3: Configure & Run
      </div>
      <div
        style={{
          fontSize: 24,
          color: "#4ade80",
          background: "rgba(0,0,0,0.3)",
          padding: "15px 25px",
          borderRadius: 8,
          marginBottom: 30,
        }}
      >
        python src/rag_assistant.py
      </div>

      <div
        style={{
          marginTop: 40,
          padding: 30,
          background: "rgba(74, 222, 128, 0.1)",
          borderLeft: "4px solid #4ade80",
          fontSize: 20,
        }}
      >
        ☁️ Deploy to: Local • AWS • Google Cloud • Azure
      </div>
    </AbsoluteFill>
  );
};
