import { createSlice } from "@reduxjs/toolkit";
import type { PDFDocument } from "../../types";

export interface PDFState {
  pdf: PDFDocument | null;
  isUploading: boolean;
}

const initialState: PDFState = {
  pdf: null,
  isUploading: false,
};

const pdfSlice = createSlice({
  name: "pdf",
  initialState,
  reducers: {
    setPDF: (state, action) => {
      state.pdf = action.payload;
    },
    setUploading: (state, action) => {
      state.isUploading = action.payload;
    },
  },
});

export const { setPDF, setUploading } = pdfSlice.actions;
export default pdfSlice.reducer;
