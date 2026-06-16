import React, { useState, useEffect, useRef, useCallback } from "react";
import IdleScreen from "./components/IdleScreen";
import ActiveScreen from "./components/ActiveScreen";
import RegisterScreen from "./components/RegisterScreen";

const WS_URL = "ws://localhost:8000/ws";

export default function App() {
  const [screen, setScreen] = useState("idle");
  const [user, setUser] = useState(null);
  const [subtitle, setSubtitle] = useState("");
  const [status, setStatus] = useState("idle");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [captureInfo, setCaptureInfo] = useState(null);
  const [registerStep, setRegisterStep] = useState(null);

  const ws = useRef(null);
  const wakeActive = useRef(false);
  const screenRef = useRef("idle");

  const updateScreen = (val) => {
    screenRef.current = val;
    setScreen(val);
  };

  const send = useCallback((obj) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(obj));
    }
  }, []);

  const connect = useCallback(() => {
    ws.current = new WebSocket(WS_URL);

    ws.current.onmessage = (e) => {
      const msg = JSON.parse(e.data);

      switch (msg.type) {
        case "recognized":
          setUser(msg);
          updateScreen("active");
          setSubtitle(`Welcome back, ${msg.name}!`);
          setStatus("speaking");
          setIsSpeaking(true);
          break;

        case "wake_detected":
          wakeActive.current = false;
          setUser({ name: "Visitor", role: "Visitor", verified: false });
          updateScreen("active");
          setSubtitle("Hello! How can I help you today?");
          setStatus("idle");
          setIsSpeaking(false);
          break;

        case "wake_timeout":
          wakeActive.current = false;
          break;

        case "no_face":
          break;

        case "listening":
          setStatus("listening");
          setIsSpeaking(false);
          setSubtitle("Listening...");
          break;

        case "transcribed":
          setSubtitle(`You said: "${msg.text}"`);
          setStatus("thinking");
          setIsSpeaking(false);
          break;

        case "thinking":
          setStatus("thinking");
          setIsSpeaking(false);
          setSubtitle("Thinking...");
          break;

        case "answer":
          setSubtitle(msg.text);
          setStatus("speaking");
          setIsSpeaking(true);
          break;

        case "speech_finished":
          setStatus("idle");
          setIsSpeaking(false);
          break;

        case "speech_stopped":
          setStatus("idle");
          setIsSpeaking(false);
          setSubtitle("Speech stopped. Ask me anything.");
          break;

        case "no_speech":
          setSubtitle("Sorry, I didn't catch that. Please try again.");
          setStatus("idle");
          setIsSpeaking(false);
          break;

        case "auto_listen":
          if (screenRef.current === "active") {
            setTimeout(() => {
              send({ action: "listen" });
            }, 1200);
          }
          break;

        case "goodbye":
          setSubtitle("Goodbye! Have a great day.");
          setStatus("idle");
          setIsSpeaking(false);
          setTimeout(() => {
            updateScreen("idle");
            setUser(null);
            setSubtitle("");
          }, 2500);
          break;

        case "start_register":
          updateScreen("register");
          setStatus("idle");
          setIsSpeaking(false);
          setCaptureInfo(null);
          break;

        case "register_ask":
          setRegisterStep({ question: msg.question });
          setSubtitle(msg.question);
          setStatus("speaking");
          setIsSpeaking(true);
          break;

        case "register_heard":
          setSubtitle(`Heard: "${msg.value}"`);
          setStatus("thinking");
          setIsSpeaking(false);
          break;

        case "capture_angle":
          setCaptureInfo({
            angle: msg.angle,
            instruction: msg.instruction,
            progress: msg.progress,
          });
          setSubtitle(msg.instruction);
          setStatus("capturing");
          setIsSpeaking(false);
          break;

        case "register_success":
          setSubtitle(`Registration successful! Welcome, ${msg.name}!`);
          setStatus("speaking");
          setIsSpeaking(true);
          setTimeout(() => {
            updateScreen("idle");
            setUser(null);
            setCaptureInfo(null);
            setIsSpeaking(false);
          }, 4000);
          break;

        case "register_failed":
        case "register_cancelled":
          setSubtitle(msg.message || "Registration cancelled.");
          setStatus("idle");
          setIsSpeaking(false);
          setTimeout(() => updateScreen("idle"), 3000);
          break;

        default:
          break;
      }
    };

    ws.current.onclose = () => setTimeout(connect, 2000);
  }, [send]);

  useEffect(() => {
    connect();
    return () => ws.current?.close();
  }, [connect]);

  useEffect(() => {
    if (screen !== "idle") return;

    const faceInterval = setInterval(() => {
      send({ action: "identify" });
    }, 5000);

    const triggerWake = () => {
      if (!wakeActive.current && ws.current?.readyState === WebSocket.OPEN) {
        wakeActive.current = true;
        send({ action: "check_wake" });
      }
    };

    triggerWake();
    const wakeInterval = setInterval(triggerWake, 500);

    return () => {
      clearInterval(faceInterval);
      clearInterval(wakeInterval);
    };
  }, [screen, send]);

  const handleListen = () => send({ action: "listen" });
  const handleStop = () => send({ action: "stop_speech" });
  const handleRegister = () => send({ action: "register_voice" });

  const handleIdle = () => {
    updateScreen("idle");
    setUser(null);
    setSubtitle("");
    setCaptureInfo(null);
    setRegisterStep(null);
    setStatus("idle");
    setIsSpeaking(false);
  };

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      {screen === "idle" && (
        <IdleScreen status={status} subtitle={subtitle} />
      )}
      {screen === "active" && (
        <ActiveScreen
          user={user}
          subtitle={subtitle}
          status={status}
          isSpeaking={isSpeaking}
          onListen={handleListen}
          onStop={handleStop}
          onRegister={handleRegister}
          onIdle={handleIdle}
        />
      )}
      {screen === "register" && (
        <RegisterScreen
          subtitle={subtitle}
          status={status}
          captureInfo={captureInfo}
          registerStep={registerStep}
          onIdle={handleIdle}
        />
      )}
    </div>
  );
}