import React from "react";

const ANGLE_EMOJIS = { straight: "😐", left: "👈", right: "👉", up: "☝️", down: "👇" };

export default function RegisterScreen({ subtitle, status, captureInfo, onIdle }) {
  return (
    <div style={{
      width: "100vw", height: "100vh",
      background: "linear-gradient(160deg, #0b1622 0%, #0e2240 40%, #091830 100%)",
      display: "flex", flexDirection: "column",
      fontFamily: "'Inter', sans-serif"
    }}>
      <div style={{ height: 5, background: "linear-gradient(90deg, #c8a84b, #f0d060, #c8a84b)" }} />

      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "16px 48px", borderBottom: "1px solid rgba(200,168,75,0.15)"
      }}>
        <div style={{ color: "#f0d060", fontWeight: 700, fontSize: 18 }}>
          🆕 New User Registration
        </div>
        <button onClick={onIdle} style={{
          background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)",
          color: "#7a9cc0", padding: "8px 20px", borderRadius: 8,
          cursor: "pointer", fontSize: 13, fontFamily: "Inter"
        }}>✕ Cancel</button>
      </div>

      <div style={{
        flex: 1, display: "flex", alignItems: "center",
        justifyContent: "center", padding: "40px 80px"
      }}>
        <div style={{
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(200,168,75,0.2)",
          borderRadius: 24, padding: "48px 60px",
          maxWidth: 600, width: "100%", textAlign: "center"
        }}>
          {captureInfo ? (
            <>
              <div style={{ fontSize: 80, marginBottom: 20, animation: "pulse 1s infinite" }}>
                {ANGLE_EMOJIS[captureInfo.angle] || "📷"}
              </div>
              <p style={{ color: "#f0d060", fontSize: 24, fontWeight: 700, marginBottom: 8 }}>
                Face Capture
              </p>
              <p style={{ color: "#d0dce8", fontSize: 18, marginBottom: 32 }}>
                {captureInfo.instruction}
              </p>
              <div style={{
                background: "rgba(255,255,255,0.05)", borderRadius: 12,
                height: 10, width: "100%", overflow: "hidden"
              }}>
                <div style={{
                  width: `${captureInfo.progress}%`, height: "100%",
                  background: "linear-gradient(90deg, #c8a84b, #f0d060)",
                  borderRadius: 12, transition: "width 0.5s ease"
                }} />
              </div>
              <p style={{ color: "#556a80", marginTop: 10, fontSize: 14 }}>
                {captureInfo.progress}% complete
              </p>
            </>
          ) : (
            <>
              <div style={{
                width: 100, height: 100, borderRadius: "50%",
                background: "linear-gradient(135deg, #0e2a4a, #152d4a)",
                border: "2px solid rgba(200,168,75,0.4)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 44, margin: "0 auto 28px",
                animation: status === "listening" ? "pulse 0.8s infinite" : "pulse 2.5s infinite"
              }}>
                {status === "listening" ? "🎤" : "🤖"}
              </div>
              <p style={{ color: "#f0d060", fontSize: 16, fontWeight: 600,
                letterSpacing: 1, textTransform: "uppercase", marginBottom: 12 }}>
                {status === "listening" ? "🎤 Listening..." : "CampusBuddy asks"}
              </p>
              <p style={{ color: "white", fontSize: 22, lineHeight: 1.6, fontWeight: 300 }}>
                {subtitle || "Starting registration..."}
              </p>
              {status === "listening" && (
                <div style={{ display: "flex", gap: 5, justifyContent: "center",
                  marginTop: 20, alignItems: "flex-end", height: 28 }}>
                  {[...Array(7)].map((_, i) => (
                    <div key={i} style={{
                      width: 5, borderRadius: 3, background: "#4ade80",
                      animation: `wave 0.9s ease-in-out ${i * 0.12}s infinite`
                    }} />
                  ))}
                </div>
              )}
              <p style={{ color: "#334455", fontSize: 13, marginTop: 32 }}>
                Speak clearly • Say "no" or "cancel" anytime to stop
              </p>
            </>
          )}
        </div>
      </div>

      <div style={{ height: 4, background: "linear-gradient(90deg, #c8a84b, #f0d060, #c8a84b)" }} />
    </div>
  );
}