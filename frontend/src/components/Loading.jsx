import React from "react";
import { HashLoader } from "react-spinners";

const Loading = ({ isLoading }) => {
  return (
    <>
      {isLoading && (
        <div className="fixed z-50 inset-0 flex items-center justify-center overflow-y-auto">
          {/* Overlay */}
          <div className="fixed inset-0 transition-opacity">
            <div className="absolute inset-0 bg-gray-900 opacity-75" />
          </div>

          {/* Spinner and Text */}
          <div className="flex flex-col items-center z-50">
            <HashLoader color="#2462b9" size={50} />
            <p className="text-lg mt-3 text-white">
              Your summary is being generated
            </p>
          </div>
        </div>
      )}
    </>
  );
};

export default Loading;
