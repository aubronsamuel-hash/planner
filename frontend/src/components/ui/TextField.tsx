import { ChangeEvent } from "react";

type TextFieldProps = {
  label: string;
  name: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  required?: boolean;
};

export const TextField = ({ label, name, value, onChange, type = "text", required = false }: TextFieldProps) => {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.value);
  };

  return (
    <label className="textfield">
      <span>{label}</span>
      <input type={type} name={name} value={value} onChange={handleChange} required={required} />
    </label>
  );
};
