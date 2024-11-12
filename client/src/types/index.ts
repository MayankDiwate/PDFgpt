export enum ROLE {
  user = "user",
  assistant = "assistant",
}

export interface Message {
  id: string;
  role: ROLE.user | ROLE.assistant;
  content: string;
}

export interface PDFDocument {
  id: string;
  name: string;
  uploadedAt: Date;
}

export interface ErrorResponse {
  message: string;
  code: string;
}
