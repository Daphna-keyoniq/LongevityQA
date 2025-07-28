import React, { useState } from "react";

interface ButtonProps {
  type?: "button" | "submit" | "reset"; // Button type
  children: React.ReactNode; // Button content
  style?: React.CSSProperties; // Custom styles
  disabled?: boolean; // Disabled state
}

const Button: React.FC<ButtonProps> = ({ type = "button", children, style, disabled = false }) => {
  const [buttonColor, setButtonColor] = useState<string>("#54769D"); // Initial button color

  const handleButtonClick = () => {
    setButtonColor("#31527F"); // Change to the new color
    setTimeout(() => {
      setButtonColor("#54769D"); // Change back to the original color after 200ms
    }, 150);
  };

  return (
    <button
      type={type}
      onClick={handleButtonClick}
      disabled={disabled}
      style={{
        padding: "10px 20px",
        backgroundColor: disabled ? "#cccccc" : buttonColor, // Use dynamic color
        color: "white",
        border: "none",
        borderRadius: "4px",
        cursor: disabled ? "not-allowed" : "pointer", // No pointer when disabled
        ...style, // Allow overriding styles
      }}
    >
      {children}
    </button>
  );
};

export default Button;
{/* <button
onClick={handleButtonClick}
style={{
  marginTop: "10px",
  padding: "10px 20px",
  backgroundColor: buttonColor,
  color: "#fff",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
}}
>
Click Me
</button> */}
// const Button: React.FC<{

//         <Button
//           type="submit"
//           style={{
//             padding: "10px 20px",
//             backgroundColor: "#007BFF",
//             color: "white",
//             border: "none",
//             borderRadius: "4px",
//             cursor: "pointer",
//           }}
//         >
//           Submit
//         </Button>
