import toast from "react-hot-toast";
import { ROLE, type Message, type PDFDocument } from "../types";

export class APIError extends Error {
  constructor(public code: string, message: string) {
    super(message);
    this.name = "APIError";
  }
}

export const uploadPDF = async (file: File): Promise<PDFDocument> => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/upload-pdf`,
      {
        method: "POST",
        body: formData,
      }
    );
    const data = await response.json();

    if (!response.ok) {
      toast.error(data.detail);
    }

    let parsedData: PDFDocument | null = null;
    if (data.id && data.name && data.uploaded_at) {
      parsedData = {
        id: data.id,
        name: data.name,
        uploadedAt: new Date(data.uploaded_at),
      };

      toast.success("PDF uploaded successfully");
    }

    return parsedData!;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    toast.error("Failed to upload PDF");
    throw new APIError("UPLOAD_ERROR", "Failed to upload PDF");
  }
};

export const sendMessage = async (
  documentId: string,
  question: string
): Promise<Message> => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/ask-question`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question, document_id: documentId }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      toast.error(data.detail);
      throw new APIError("MESSAGE_ERROR", data.detail);
    }

    // const readable = data.response.content as ReadableStream<Uint8Array>;
    // const messageContent = await readableStreamToString(readable);

    return {
      id: crypto.randomUUID(),
      role: ROLE.assistant,
      content: data.content,
      // timestamp: new Date(),
    };
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    toast.error("Failed to send message");
    throw new APIError("MESSAGE_ERROR", "Failed to send message");
  }
};
