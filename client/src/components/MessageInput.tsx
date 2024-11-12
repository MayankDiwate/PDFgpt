import { SendHorizonal } from "lucide-react";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addMessage, setLoading } from "../redux/slices/messagesSlice";
import { RootState } from "../redux/store";
import { sendMessage } from "../services/api";
import { Message, ROLE } from "../types";

const MessageInput = () => {
  const dispatch = useDispatch();
  const [inputMessage, setInputMessage] = useState("");
  const uploadedPDF = useSelector((state: RootState) => state.pdf.pdf);
  const isLoading = useSelector((state: RootState) => state.messages.isLoading);
  const isPDFUploaded = uploadedPDF !== null;

  const handleSend = async () => {
    dispatch(setLoading(true));

    if (inputMessage.trim()) {
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: ROLE.user,
        content: inputMessage,
      };
      dispatch(addMessage(userMessage));
      setInputMessage("");

      const aiResponse = await sendMessage(uploadedPDF!.id, inputMessage);

      if (aiResponse) {
        dispatch(setLoading(false));
        dispatch(addMessage(aiResponse));
      } else {
        dispatch(setLoading(false));
      }
    }
    dispatch(setLoading(false));
  };

  return (
    <div className="fixed bottom-4 left-0 right-0 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="relative">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Send a message..."
            className="w-full p-3 pr-12 rounded-lg border focus:outline-none bg-white shadow-md focus:ring-2 focus:ring-green-500"
            disabled={isLoading || !isPDFUploaded}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !isPDFUploaded || !inputMessage.trim()}
            className="absolute right-3 top-1/2 transform -translate-y-1/2"
          >
            <SendHorizonal
              size={20}
              className={`
                ${
                  isLoading || isPDFUploaded || !inputMessage.trim()
                    ? "text-gray-400"
                    : "text-green-500 hover:text-green-600"
                }
              `}
            />
          </button>
        </div>
      </div>
    </div>
  );
};

export default MessageInput;
