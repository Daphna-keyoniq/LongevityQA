import React from "react";

interface TextBoxProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  label?: string;
}

const TextBox: React.FC<TextBoxProps> = ({ value, onChange, placeholder, label }) => {
  return (
    <div style={{ marginBottom: "10px" }}>
      {label && (
        <label
          style={{
            display: "block",
            marginBottom: "5px",
            fontWeight: "bold",
            color: "#54769D", 
          }}
        >
          {label}
        </label>
      )}
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder={placeholder || "Type something..."}
        style={{
          width: "300px",
          padding: "10px",
          border: "2px solid #54769D", // Add a unique border color
          borderRadius: "4px",
          backgroundColor: "#f9f9f9", // Add a light background color
        }}
      />
    </div>
  );
};

export default TextBox;