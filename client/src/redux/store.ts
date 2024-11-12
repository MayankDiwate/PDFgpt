import { configureStore } from "@reduxjs/toolkit";
import messagesSlice from "./slices/messagesSlice";
import pdfSlice from "./slices/pdfSlice";

export const store = configureStore({
  reducer: {
    messages: messagesSlice,
    pdf: pdfSlice,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
