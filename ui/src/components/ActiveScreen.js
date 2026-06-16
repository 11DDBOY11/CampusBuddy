import React from "react";
import campusBg from "../assets/campus.png";

const STATUS_CONFIG = {
  idle:      { color: "#C8972B", label: "Ready — Ask me anything", icon: "💬" },
  listening: { color: "#4ade80", label: "Listening...",             icon: "🎤" },
  thinking:  { color: "#60a5fa", label: "Thinking...",              icon: "⏳" },
  speaking:  { color: "#C8972B", label: "Speaking...",              icon: "🔊" },
  capturing: { color: "#a78bfa", label: "Capturing face...",        icon: "📸" },
};

export default function ActiveScreen({
  user,
  subtitle,
  status,
  isSpeaking,
  onListen,
  onStop,
  onRegister,
  onIdle,
}) {
  const cfg = STATUS_CONFIG[status] || STATUS_CONFIG.idle;

  return (
    <div style={{
      width: "100vw",
      height: "100vh",
      backgroundImage: `url(${campusBg})`,
      backgroundSize: "cover",
      backgroundPosition: "center",
      backgroundRepeat: "no-repeat",
      fontFamily: "'Inter', sans-serif",
      overflow: "hidden",
      position: "relative",
    }}>

      {/* Dark overlay so text stays readable over photo */}
      <div style={{
        position: "absolute",
        inset: 0,
        background: "linear-gradient(160deg, rgba(11,21,38,0.91) 0%, rgba(14,30,56,0.85) 50%, rgba(11,21,38,0.93) 100%)",
        zIndex: 0,
      }} />

      {/* All content above overlay */}
      <div style={{
        position: "relative",
        zIndex: 1,
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
      }}>

        {/* AIET red top strip */}
        <div style={{ height: 5, background: "#B22222", flexShrink: 0 }} />

        {/* Gold accent line */}
        <div style={{
          height: 2,
          background: "linear-gradient(90deg, #C8972B, #D4AF37, #C8972B)",
          flexShrink: 0,
        }} />

        {/* Header */}
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "14px 48px",
          borderBottom: "1px solid rgba(200,151,43,0.2)",
          flexShrink: 0,
          backdropFilter: "blur(8px)",
          background: "rgba(11,21,38,0.4)",
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{
              width: 42, height: 42, borderRadius: 8,
              background: "linear-gradient(135deg, #C8972B, #D4AF37)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: "'Playfair Display', Georgia, serif",
              fontSize: 22, fontWeight: 800, color: "#0B1526",
            }}>A</div>
            <div>
              <div style={{
                fontFamily: "'Playfair Display', Georgia, serif",
                color: "#D4AF37", fontWeight: 700, fontSize: 17, letterSpacing: 0.5,
              }}>CampusBuddy</div>
              <div style={{
                color: "#7a9cc0", fontSize: 11,
                letterSpacing: 1, textTransform: "uppercase",
              }}>AIET · Moodubidri</div>
            </div>
          </div>

          <button onClick={onIdle} style={{
            background: "rgba(255,255,255,0.06)",
            border: "1px solid rgba(255,255,255,0.12)",
            color: "#7a9cc0", padding: "8px 20px", borderRadius: 8,
            cursor: "pointer", fontSize: 13, fontFamily: "Inter",
          }}>← Exit</button>
        </div>

        {/* Main content */}
        <div style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 72px",
          gap: 56,
        }}>

          {/* Left panel */}
          <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 24 }}>

            {/* User card */}
            <div style={{
              background: "rgba(11,21,38,0.65)",
              backdropFilter: "blur(12px)",
              border: "1px solid rgba(200,151,43,0.25)",
              borderRadius: 14, padding: "18px 24px",
              display: "flex", alignItems: "center", gap: 16,
            }}>
              <div style={{
                width: 52, height: 52, borderRadius: 12, flexShrink: 0,
                background: user?.verified
                  ? "linear-gradient(135deg, #C8972B, #D4AF37)"
                  : "linear-gradient(135deg, #1A2942, #2A3F6A)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 22,
              }}>
                {user?.verified ? "👤" : "👋"}
              </div>
              <div>
                <div style={{
                  color: "white", fontWeight: 700, fontSize: 18,
                  fontFamily: "'Playfair Display', Georgia, serif",
                }}>
                  {user?.verified ? `Welcome back, ${user.name}!` : "Hello, Visitor!"}
                </div>
                {user?.verified && (
                  <div style={{ color: "#8aaccc", fontSize: 13, marginTop: 3 }}>
                    {user.role} · {user.branch}{user.usn ? ` · ${user.usn}` : ""}
                  </div>
                )}
              </div>
            </div>

            {/* Status + answer box */}
            <div style={{
              background: "rgba(11,21,38,0.70)",
              backdropFilter: "blur(14px)",
              border: `1px solid ${cfg.color}44`,
              borderRadius: 14, padding: "24px 28px",
              minHeight: 150, position: "relative",
            }}>
              {/* Gold vertical rule */}
              <div style={{
                position: "absolute", left: 0, top: 16, bottom: 16,
                width: 3, background: cfg.color,
                borderRadius: "0 3px 3px 0",
              }} />

              <div style={{
                display: "flex", alignItems: "center",
                gap: 10, marginBottom: 14, paddingLeft: 8,
              }}>
                <span style={{ fontSize: 16 }}>{cfg.icon}</span>
                <span style={{
                  color: cfg.color, fontSize: 12, fontWeight: 600,
                  letterSpacing: 1.5, textTransform: "uppercase",
                }}>
                  {cfg.label}
                </span>
              </div>

              <p style={{
                color: "#c8d8e8", fontSize: 19, lineHeight: 1.75,
                fontWeight: 300, paddingLeft: 8,
              }}>
                {subtitle || "Ask me anything about AIET — departments, faculty, events, placements, timetables..."}
              </p>

              {status === "listening" && (
                <div style={{
                  display: "flex", gap: 4, alignItems: "flex-end",
                  marginTop: 14, height: 28, paddingLeft: 8,
                }}>
                  {[14, 22, 18, 28, 16, 24, 20, 26, 14].map((h, i) => (
                    <div key={i} style={{
                      width: 4, height: h, borderRadius: 3,
                      background: "#4ade80", opacity: 0.85,
                    }} />
                  ))}
                </div>
              )}

              {status === "thinking" && (
                <div style={{
                  display: "flex", gap: 8,
                  marginTop: 14, paddingLeft: 8,
                }}>
                  {[0, 1, 2].map((i) => (
                    <div key={i} style={{
                      width: 9, height: 9, borderRadius: "50%",
                      background: "#60a5fa",
                    }} />
                  ))}
                </div>
              )}
            </div>

            {/* Action buttons */}
            <div style={{ display: "flex", gap: 14, flexWrap: "wrap" }}>
              <button onClick={onListen} style={{
                flex: 1, minWidth: 180,
                background: "linear-gradient(135deg, #C8972B, #D4AF37)",
                border: "none", color: "#0B1526",
                padding: "15px 0", borderRadius: 10,
                fontSize: 15, fontWeight: 700, cursor: "pointer",
                fontFamily: "Inter",
                boxShadow: "0 4px 20px rgba(200,151,43,0.35)",
              }}>
                🎤 Ask a Question
              </button>

              {!user?.verified && (
                <button onClick={onRegister} style={{
                  flex: 1, minWidth: 180,
                  background: "rgba(11,21,38,0.6)",
                  backdropFilter: "blur(8px)",
                  border: "1px solid rgba(200,151,43,0.35)",
                  color: "#D4AF37",
                  padding: "15px 0", borderRadius: 10,
                  fontSize: 15, fontWeight: 600, cursor: "pointer",
                  fontFamily: "Inter",
                }}>
                  🆕 Register Face
                </button>
              )}

              {isSpeaking && (
                <button onClick={onStop} style={{
                  flex: 1, minWidth: 180,
                  background: "rgba(178,34,34,0.18)",
                  backdropFilter: "blur(8px)",
                  border: "1px solid rgba(178,34,34,0.5)",
                  color: "#ff7070",
                  padding: "15px 0", borderRadius: 10,
                  fontSize: 15, fontWeight: 600, cursor: "pointer",
                  fontFamily: "Inter",
                }}>
                  ⏹ Stop Speaking
                </button>
              )}
            </div>

            {/* Stats strip */}
            <div style={{
              display: "flex",
              borderTop: "1px solid rgba(200,151,43,0.15)",
              paddingTop: 18,
              background: "rgba(11,21,38,0.45)",
              backdropFilter: "blur(8px)",
              borderRadius: 10,
              padding: "14px 0",
            }}>
              {[
                { value: "218+", label: "Recruiters" },
                { value: "406",  label: "Students Placed" },
                { value: "10",   label: "Departments" },
                { value: "2008", label: "Established" },
              ].map((stat, i) => (
                <div key={i} style={{
                  flex: 1, textAlign: "center",
                  borderRight: i < 3 ? "1px solid rgba(200,151,43,0.15)" : "none",
                }}>
                  <div style={{
                    color: "#D4AF37", fontSize: 22, fontWeight: 700,
                    fontFamily: "'Playfair Display', Georgia, serif",
                  }}>{stat.value}</div>
                  <div style={{
                    color: "#5a7a9a", fontSize: 11,
                    marginTop: 2, letterSpacing: 0.5,
                  }}>{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right — Bot avatar */}
          <div style={{
            width: 180, height: 220, flexShrink: 0,
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center", gap: 14,
          }}>
            <div style={{
              width: 160, height: 160, borderRadius: "50%",
              background: "rgba(11,21,38,0.55)",
              backdropFilter: "blur(10px)",
              border: `2px solid ${cfg.color}66`,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 72,
              boxShadow: `0 0 50px ${cfg.color}22`,
              transition: "all 0.5s ease",
            }}>
              {status === "listening" ? "🎤"
                : status === "thinking" ? "🤔"
                : isSpeaking ? "🔊"
                : "🤖"}
            </div>

            {/* Accreditation badges */}
            <div style={{
              display: "flex", gap: 6,
              flexWrap: "wrap", justifyContent: "center",
            }}>
              {["VTU", "AICTE", "NAAC", "NBA"].map(badge => (
                <span key={badge} style={{
                  background: "rgba(11,21,38,0.6)",
                  backdropFilter: "blur(6px)",
                  border: "1px solid rgba(200,151,43,0.3)",
                  color: "#a07828", fontSize: 9, fontWeight: 700,
                  padding: "2px 6px", borderRadius: 4, letterSpacing: 0.5,
                }}>{badge}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom gold rule */}
        <div style={{
          height: 3,
          background: "linear-gradient(90deg, #C8972B, #D4AF37, #C8972B)",
          flexShrink: 0,
        }} />

      </div>
    </div>
  );
}