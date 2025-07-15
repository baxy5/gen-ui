import React from "react";
import { Loader, Send } from "lucide-react";

const Chat = () => {
  return (
    <div className="w-full flex justify-center items-center h-1/3">
      <div className="bg-gray-200 text-gray-500  border border-gray-500 w-full max-w-[600px] max-h-fit p-2 rounded-lg shadow-md hover:shadow-lg">
        <div className="flex w-full">
          <textarea
            name=""
            id=""
            placeholder="Ask for anything"
            className="flex-grow py-2 rounded-lg text-gray-500 focus:outline-none min-h-[40px] max-h-[200px] resize-none"
            rows={2}
          ></textarea>
        </div>
        <div className="flex justify-end">
          <button className="bg-gray-300 p-2 rounded-full cursor-pointer hover:bg-gray-400 border border-gray-500">
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
