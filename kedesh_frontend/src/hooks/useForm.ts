import { useState } from "react";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type FormValues = { [key: string]: any };

export function useForm(initialValues: FormValues) {
  const [values, setValues] = useState<FormValues>(initialValues);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setValues((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setValues(initialValues);
  };

  return { values, handleChange, resetForm };
}
