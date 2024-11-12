import { CirclePlus, File } from "lucide-react";
import React, { useState } from "react";
import toast from "react-hot-toast";
import { useDispatch } from "react-redux";
import logo from "../assets/logo.svg";
import { addMessage, clearMessages } from "../redux/slices/messagesSlice";
import { setPDF } from "../redux/slices/pdfSlice";
import { uploadPDF } from "../services/api";
import { Message, PDFDocument, ROLE } from "../types";

const Header = () => {
  const [currentPDF, setCurrentPDF] = useState<PDFDocument | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const dispatch = useDispatch();

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    try {
      // Implement your file upload logic here
      const newPDF = await uploadPDF(file);

      setCurrentPDF(newPDF);
      dispatch(
        setPDF({ ...newPDF, uploadedAt: newPDF.uploadedAt.toISOString() })
      );
      dispatch(clearMessages());
      const greetMessage: Message = {
        id: crypto.randomUUID(),
        role: ROLE.assistant,
        content: `Hello, I'm AI Planet. How can I help you today?`,
      };

      dispatch(addMessage(greetMessage));
      setIsUploading(false);
    } catch (error) {
      setIsUploading(false);
      console.error("Error uploading file:", error);
      toast.error("Failed to upload PDF");
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file && file.type === "application/pdf") {
      handleFileUpload(file);
    } else {
      setIsUploading(false);
      toast.error("Please select a PDF file");
    }
  };

  return (
    <header className="bg-white border-b p-4 w-full z-10 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <img
            src={logo}
            alt="AI Planet"
            width={110}
            height={110}
            className="min-w-[110px]"
          />
        </div>
        <div className="flex items-center space-x-4">
          {currentPDF && (
            <div className="flex items-center gap-2 text-primary text-sm justify-end w-60">
              <div className="border rounded-sm p-1 border-primary">
                <File size={16} />
              </div>
              <div className="truncate text-end max-w-40 sm:max-w-60">
                {currentPDF.name}
              </div>
            </div>
          )}

          <label
            className={`
            cursor-pointer sm:px-8 px-2 py-2 bg-white border border-gray-500 rounded-lg
            ${
              isUploading ? "opacity-50 cursor-not-allowed" : "hover:bg-gray-50"
            }
          `}
          >
            <input
              type="file"
              onChange={handleFileChange}
              className="hidden"
              disabled={isUploading}
            />
            <div className="flex items-center space-x-2 font-semibold">
              <CirclePlus size={16} />
              <span className="hidden sm:block">
                {isUploading ? "Uploading..." : "Upload PDF"}
              </span>
            </div>
          </label>
        </div>
      </div>
    </header>
  );
};

export default Header;
