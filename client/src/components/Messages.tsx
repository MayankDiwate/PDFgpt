import { useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import aiLogo from "../assets/ai-logo.svg";
import ReactMarkdown from "react-markdown";

import { RootState } from "../redux/store";

const MessageList = () => {
  const messageListRef = useRef<HTMLDivElement>(null);
  const messages = useSelector((state: RootState) => state.messages.messages);
  const isLoading = useSelector((state: RootState) => state.messages.isLoading);

  useEffect(() => {
    // Scroll to the bottom of the message list whenever messages change
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div
      ref={messageListRef}
      className="overflow-y-auto max-h-[calc(100vh-160px)]"
    >
      {messages.map((message, index) => (
        <div className="flex items-start space-x-4 my-4" key={index}>
          <div
            className={`
              rounded-full flex items-center justify-center text-lg w-10 h-10 font-medium
              ${message.role === "user" ? "bg-purple-300 text-white" : ""}
            `}
          >
            {message.role === "user" ? (
              "S"
            ) : (
              <img src={aiLogo} alt="AI Planet" width={40} className="min-w-10" />
            )}
          </div>
          <div className="flex-1">
            <div className="text-gray-800 font-medium">
              {message.role === "assistant" ? "Assistant" : "You"}
            </div>
            <ReactMarkdown className="text-gray-600">
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="flex items-start space-x-4 my-4">
          <img src={aiLogo} alt="AI Planet" />
          <div className="flex-1">
            <div className="text-gray-800 font-medium">Assistant</div>
            <p className="text-gray-600 text-sm">Loading...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageList;
