import React from 'react'
import {ClipLoader} from "react-spinners";


interface LoaderProps {
    loading: boolean;
    message?: string;
    siz?: "small" | "medium" | "large";
  }
  
  const Loader: React.FC<LoaderProps> = ({ loading, message, siz = "medium" }) => {
    if (!loading) return null;
  
    const sizeStyles = {
      small: { width: "20px", height: "20px" },
      medium: { width: "40px", height: "40px" },
      large: { width: "60px", height: "60px" },
    };
  
    return (
      <div style={{ textAlign: "center", marginTop: "10px" }}>
        <div
          style={{
            ...sizeStyles[siz],
            border: "4px solid #ccc",
            borderTop: "4px solid #54769D",
            borderRadius: "50%",
            animation: "spin 1s linear infinite",
            margin: "0 auto",
          }}
        ></div>
        {message && <p style={{ marginTop: "10px", color: "#54769D" }}>{message}</p>}
        <style>
          {`
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `}
        </style>
      </div>
    );
  };
  
  export default Loader;