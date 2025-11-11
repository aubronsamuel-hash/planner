import { ButtonHTMLAttributes } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement>;

export const Button = ({ children, ...props }: ButtonProps) => {
  return (
    <button {...props} className={`btn ${props.className ?? ""}`.trim()}>
      {children}
    </button>
  );
};
