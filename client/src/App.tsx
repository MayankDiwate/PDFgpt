import React from "react";
import { Toaster } from "react-hot-toast";
import Header from "./components/Header";
import MessageInput from "./components/MessageInput";
import MessageList from "./components/Messages";

const App: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header />

      <Toaster reverseOrder={false} position="top-center" />

      <main className="flex-1 max-w-7xl mx-4 md:mx-auto md:px-10 lg:px-20 max-h-[calc(100vh-160px)] w-full overflow-y-auto">
        <MessageList />
      </main>

      <MessageInput />
    </div>
  );
};

export default App;
