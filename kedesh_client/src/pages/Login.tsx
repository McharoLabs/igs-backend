import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import { signIn } from "../state/auth/AuthSlice";
import { SubmitHandler, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoginFormData, loginSchema } from "../schemas/authSchema";
import TextInput from "../components/common/InputText";
import useNavigation from "../hooks/useNavigation";
import Button from "../components/common/Button";
import Card from "../components/common/Card";

const Login = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { loading } = useSelector((state: RootState) => state.auth);
  const { goToDashboard, goToRegistration } = useNavigation(); // Added goToRegistration

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit: SubmitHandler<LoginFormData> = (data) => {
    dispatch(signIn({ username: data.phone_number, password: data.password }))
      .unwrap()
      .then(() => {
        goToDashboard();
        reset();
      })
      .catch((error) => {
        setError("phone_number", { type: "manual", message: error.detail });
        setError("password", { type: "manual", message: error.detail });
      });
  };

  return (
    <div className="flex justify-center items-center min-h-screen p-4">
      <Card title="Ingia" className="w-full sm:w-[420px]">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <TextInput
            label="Namba ya simu"
            type="tel"
            placeholder="07########"
            error={errors.phone_number?.message}
            register={register("phone_number")}
          />
          <TextInput
            label="Nywila"
            type="password"
            placeholder="********"
            error={errors.password?.message}
            register={register("password")}
          />
          <div>
            <Button
              type="submit"
              isLoading={loading}
              disabled={loading}
              className="w-full"
            >
              Ingia
            </Button>
          </div>
        </form>

        <div className="mt-4 text-center text-sm text-gray-600">
          Hauna akaunti?{" "}
          <button
            onClick={goToRegistration}
            className="text-primary hover:underline"
          >
            Jisajili
          </button>
        </div>
      </Card>
    </div>
  );
};

export default Login;
