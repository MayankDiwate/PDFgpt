import { createSlice } from "@reduxjs/toolkit";
import { Message } from "../../types";

export interface MessagesState {
  messages: Message[];
  isLoading: boolean;
}

const initialState: MessagesState = {
  messages: [],
  isLoading: false,
};

const messagesSlice = createSlice({
  name: "messages",
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    clearMessages: (state) => {
      state.messages = [];
    }
  },
});

export const { addMessage, setLoading, clearMessages } = messagesSlice.actions;
export default messagesSlice.reducer;
