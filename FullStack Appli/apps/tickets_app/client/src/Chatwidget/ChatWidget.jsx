import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./ChatWidget.css";

const API_URL = "http://localhost:8001/chat";

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const trimmedPrompt = prompt.trim();

    if (!trimmedPrompt || loading) {
      return;
    }

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: trimmedPrompt,
      },
    ]);

    setPrompt("");
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: trimmedPrompt,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      // Add assistant response
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "error",
          content:
            error.message || "Unable to connect to the server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          className="chat-floating-button"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
        >
          💬
        </button>
      )}

      {/* Overlay */}
      {isOpen && (
        <div
          className="chat-overlay"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Side Panel */}
      <div className={`chat-side-panel ${isOpen ? "open" : ""}`}>
        {/* Header */}
        <div className="chat-header">
          <div className="chat-header-left">
            <div className="chat-avatar">AI</div>

            <div>
              <div className="chat-title">
                Technical Assistant
              </div>

              <div className="chat-subtitle">
                React · FastAPI · MongoDB
              </div>
            </div>
          </div>

          <div className="chat-header-actions">
            <button
              className="chat-header-button"
              onClick={clearChat}
              title="Clear chat"
            >
              ↻
            </button>

            <button
              className="chat-close-button"
              onClick={() => setIsOpen(false)}
              title="Close"
            >
              ×
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-welcome">
              <div className="chat-welcome-icon">
                🤖
              </div>

              <h3>How can I help?</h3>

              <p>
                Ask me questions about:
              </p>

              <div className="chat-topic-list">
                {[
                  "React",
                  "FastAPI",
                  "MongoDB",
                  "REST APIs",
                  "JWT",
                  "Docker",
                ].map((topic) => (
                  <span
                    key={topic}
                    className="chat-topic"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-message-row ${
                message.role === "user"
                  ? "user"
                  : "assistant"
              }`}
            >
              <div
                className={`chat-message ${
                  message.role === "user"
                    ? "user-message"
                    : message.role === "error"
                    ? "error-message"
                    : "assistant-message"
                }`}
              >
                {message.role === "assistant" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  message.content
                )}
              </div>
            </div>
          ))}

          {/* Loading */}
          {loading && (
            <div className="chat-message-row assistant">
              <div className="chat-message assistant-message">
                <div className="chat-typing">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="chat-input-section">
          <div className="chat-input-wrapper">
            <textarea
              value={prompt}
              onChange={(event) =>
                setPrompt(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              rows={1}
              disabled={loading}
            />

            <button
              className="chat-send-button"
              onClick={sendMessage}
              disabled={!prompt.trim() || loading}
            >
              ➤
            </button>
          </div>

          <div className="chat-input-hint">
            Enter to send · Shift + Enter for new line
          </div>
        </div>
      </div>
    </>
  );
}