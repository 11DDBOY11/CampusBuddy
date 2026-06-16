import React from "react";
import campusBg from "../assets/campus.png";

export default function IdleScreen({ onStart, onWakeWord }) {
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', sans-serif",
        backgroundImage: `url(${campusBg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        display: "flex",
        alignItems: "stretch",
        justifyContent: "center",
      }}
    >
      {/* Main dark overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(110deg, rgba(7,16,28,0.90) 0%, rgba(10,24,42,0.84) 38%, rgba(10,24,42,0.72) 58%, rgba(7,16,28,0.88) 100%)",
          zIndex: 0,
        }}
      />

      {/* Soft vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at center, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.00) 35%, rgba(0,0,0,0.34) 100%)",
          zIndex: 0,
        }}
      />

      {/* Top branding lines */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          zIndex: 1,
        }}
      >
        <div style={{ height: 5, background: "#B22222" }} />
        <div
          style={{
            height: 2,
            background: "linear-gradient(90deg, #C8972B, #D4AF37, #C8972B)",
          }}
        />
      </div>

      {/* Main content */}
      <div
        style={{
          position: "relative",
          zIndex: 2,
          width: "100%",
          height: "100%",
          display: "grid",
          gridTemplateColumns: "1.15fr 0.85fr",
          padding: "48px 64px 36px",
          gap: 32,
        }}
      >
        {/* Left side */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            minWidth: 0,
          }}
        >
          {/* Header */}
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div
              style={{
                width: 58,
                height: 58,
                borderRadius: 14,
                background: "linear-gradient(135deg, #C8972B, #E1BC55)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#0B1526",
                fontSize: 28,
                fontWeight: 800,
                boxShadow: "0 8px 30px rgba(200,151,43,0.28)",
                fontFamily: "'Playfair Display', Georgia, serif",
              }}
            >
              A
            </div>

            <div>
              <div
                style={{
                  color: "#F3D98B",
                  fontSize: 15,
                  letterSpacing: 2.4,
                  textTransform: "uppercase",
                  fontWeight: 700,
                }}
              >
                Alva&apos;s Institute of Engineering & Technology
              </div>
              <div
                style={{
                  color: "#8FA8C2",
                  fontSize: 13,
                  letterSpacing: 1.1,
                  textTransform: "uppercase",
                  marginTop: 4,
                }}
              >
                Shobhavana Campus · Mijar · Moodbidri
              </div>
            </div>
          </div>

          {/* Hero copy */}
          <div style={{ marginTop: 20 }}>
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 10,
                padding: "8px 14px",
                borderRadius: 999,
                background: "rgba(200,151,43,0.10)",
                border: "1px solid rgba(200,151,43,0.26)",
                color: "#E3C66D",
                fontSize: 13,
                fontWeight: 600,
                letterSpacing: 0.6,
                backdropFilter: "blur(8px)",
              }}
            >
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "#D4AF37",
                  boxShadow: "0 0 12px rgba(212,175,55,0.6)",
                }}
              />
              AI Voice Assistant for Our Campus
            </div>

            <h1
              style={{
                margin: "24px 0 16px",
                fontSize: "clamp(48px, 6vw, 86px)",
                lineHeight: 0.98,
                color: "#FFFFFF",
                fontWeight: 700,
                letterSpacing: -1.8,
                fontFamily: "'Playfair Display', Georgia, serif",
                maxWidth: 780,
              }}
            >
              CampusBuddy
            </h1>

            <p
              style={{
                fontSize: 24,
                lineHeight: 1.5,
                color: "#D4E1EE",
                maxWidth: 760,
                fontWeight: 300,
                marginBottom: 28,
              }}
            >
              Ask about departments, placements, hostel, admissions, events,
              timetables, and campus information in simple voice.
            </p>

            <div
              style={{
                display: "flex",
                gap: 12,
                flexWrap: "wrap",
                marginBottom: 30,
              }}
            >
              {[
                "Departments",
                "Placements",
                "Admissions",
                "Hostel",
                "Events",
                "Faculty Info",
              ].map((item) => (
                <div
                  key={item}
                  style={{
                    padding: "10px 16px",
                    borderRadius: 999,
                    background: "rgba(11,21,38,0.48)",
                    border: "1px solid rgba(255,255,255,0.10)",
                    color: "#D7E2EE",
                    fontSize: 14,
                    fontWeight: 500,
                    backdropFilter: "blur(10px)",
                  }}
                >
                  {item}
                </div>
              ))}
            </div>

            {/* Main actions */}
            <div
              style={{
                display: "flex",
                alignItems: "stretch",
                gap: 14,
                flexWrap: "wrap",
                marginBottom: 18,
              }}
            >
              <button
                onClick={onStart}
                style={{
                  background: "linear-gradient(135deg, #C8972B, #E1BC55)",
                  color: "#0B1526",
                  border: "none",
                  borderRadius: 14,
                  padding: "18px 34px",
                  fontSize: 18,
                  fontWeight: 800,
                  cursor: "pointer",
                  boxShadow: "0 12px 30px rgba(200,151,43,0.26)",
                  minWidth: 240,
                }}
              >
                🎤 Tap to Start
              </button>

              <button
                onClick={onWakeWord}
                style={{
                  background: "rgba(11,21,38,0.58)",
                  color: "#F4D77A",
                  border: "1px solid rgba(200,151,43,0.28)",
                  borderRadius: 14,
                  padding: "18px 24px",
                  fontSize: 16,
                  fontWeight: 700,
                  cursor: "pointer",
                  backdropFilter: "blur(10px)",
                  minWidth: 260,
                }}
              >
                🔊 Say “Hi CampusBuddy”
              </button>
            </div>

            {/* Wake note */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                color: "#AFC3D8",
                fontSize: 15,
                lineHeight: 1.5,
                maxWidth: 700,
              }}
            >
              <span
                style={{
                  width: 10,
                  height: 10,
                  borderRadius: "50%",
                  background: "#4ADE80",
                  boxShadow: "0 0 12px rgba(74,222,128,0.55)",
                  flexShrink: 0,
                }}
              />
              You can either tap the screen or wake the assistant by saying
              <span style={{ color: "#F3D98B", fontWeight: 700 }}>
                &nbsp;“Hi CampusBuddy”
              </span>
            </div>
          </div>

          {/* Bottom info */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 28,
              flexWrap: "wrap",
              marginTop: 30,
              paddingTop: 18,
              borderTop: "1px solid rgba(255,255,255,0.10)",
            }}
          >
            {[
              { value: "AIET", label: "Official Campus Assistant" },
              { value: "2008", label: "Established" },
              { value: "Voice + Touch", label: "Interaction" },
            ].map((item) => (
              <div key={item.label}>
                <div
                  style={{
                    color: "#F0CF70",
                    fontSize: 24,
                    fontWeight: 700,
                    fontFamily: "'Playfair Display', Georgia, serif",
                  }}
                >
                  {item.value}
                </div>
                <div
                  style={{
                    color: "#8FA8C2",
                    fontSize: 12,
                    letterSpacing: 0.8,
                    textTransform: "uppercase",
                    marginTop: 3,
                  }}
                >
                  {item.label}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right side poster panel */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              width: "100%",
              maxWidth: 520,
              height: "86%",
              borderRadius: 26,
              background: "rgba(10,20,35,0.52)",
              border: "1px solid rgba(200,151,43,0.20)",
              boxShadow: "0 20px 60px rgba(0,0,0,0.34)",
              backdropFilter: "blur(14px)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              padding: "28px 28px 24px",
              overflow: "hidden",
              position: "relative",
            }}
          >
            <div
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                height: 3,
                background:
                  "linear-gradient(90deg, #C8972B, #E1BC55, #C8972B)",
              }}
            />

            <div>
              <div
                style={{
                  color: "#F3D98B",
                  fontSize: 12,
                  letterSpacing: 2,
                  textTransform: "uppercase",
                  fontWeight: 700,
                  marginBottom: 14,
                }}
              >
                Voice Help Desk
              </div>

              <div
                style={{
                  width: 120,
                  height: 120,
                  borderRadius: "50%",
                  margin: "0 auto 20px",
                  background:
                    "radial-gradient(circle at 30% 30%, rgba(225,188,85,0.95), rgba(200,151,43,0.78) 55%, rgba(120,82,18,0.45) 100%)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow:
                    "0 0 0 10px rgba(200,151,43,0.08), 0 0 0 22px rgba(200,151,43,0.04)",
                }}
              >
                <span style={{ fontSize: 48 }}>🎙️</span>
              </div>

              <h2
                style={{
                  color: "#FFFFFF",
                  textAlign: "center",
                  fontSize: 32,
                  lineHeight: 1.18,
                  fontWeight: 700,
                  fontFamily: "'Playfair Display', Georgia, serif",
                  marginBottom: 12,
                }}
              >
                Tap to begin
                <br />
                or wake by voice.
              </h2>

              <p
                style={{
                  color: "#C8D8E8",
                  textAlign: "center",
                  fontSize: 17,
                  lineHeight: 1.65,
                  maxWidth: 370,
                  margin: "0 auto 22px",
                }}
              >
                Start by touching the screen, or simply say
                <span style={{ color: "#F3D98B", fontWeight: 700 }}>
                  {" "}
                  “Hi CampusBuddy”
                </span>
                to begin your campus query.
              </p>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: 12,
                }}
              >
                {[
                  "Ask in simple English",
                  "Fast voice response",
                  "Hands-free wake option",
                  "Useful on campus",
                ].map((item) => (
                  <div
                    key={item}
                    style={{
                      background: "rgba(255,255,255,0.05)",
                      border: "1px solid rgba(255,255,255,0.08)",
                      borderRadius: 12,
                      padding: "14px 12px",
                      color: "#D8E4EF",
                      fontSize: 14,
                      lineHeight: 1.4,
                      textAlign: "center",
                    }}
                  >
                    {item}
                  </div>
                ))}
              </div>
            </div>

            <div
              style={{
                borderTop: "1px solid rgba(255,255,255,0.08)",
                paddingTop: 18,
                display: "flex",
                justifyContent: "space-between",
                gap: 10,
                flexWrap: "wrap",
              }}
            >
              {[
                "Placements",
                "Departments",
                "Hostel",
                "Admissions",
              ].map((item) => (
                <span
                  key={item}
                  style={{
                    color: "#9EB5CC",
                    fontSize: 13,
                    letterSpacing: 0.3,
                  }}
                >
                  {item}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom gold line */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: 3,
          background: "linear-gradient(90deg, #C8972B, #D4AF37, #C8972B)",
          zIndex: 2,
        }}
      />
    </div>
  );
}