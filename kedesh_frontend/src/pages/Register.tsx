import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, SubmitHandler } from "react-hook-form";
import { useDispatch, useSelector } from "react-redux";
import TextInput from "../components/common/InputText";
import { AppDispatch, RootState } from "../state/store";
import {
  RegistrationFormData,
  registrationSchema,
} from "../schemas/registrationSchema";
import Select from "../components/common/Select";
import { GENDER } from "../types/enums";
import FileInput from "../components/common/FileInput";
import Button from "../components/common/Button";
import {
  registerAgent,
  resetRegistrationState,
} from "../state/registration/registrationSlice";
import { Link } from "react-router-dom";
import { ROUTES } from "../routes/routes";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import useNavigation from "../hooks/useNavigation";

const Register = () => {
  const { goToLogin } = useNavigation();
  const { error, loading, success, detail } = useSelector(
    (state: RootState) => state.registration
  );
  const dispatch = useDispatch<AppDispatch>();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
  });

  const onSubmit: SubmitHandler<RegistrationFormData> = async (data) => {
    try {
      await dispatch(registerAgent(data)).unwrap();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen  p-4">
      <div className="w-full max-w-4xl bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-center text-gray-600 mb-6">
          Dalali au mwenye nyumba? Jisajili sasa
        </h2>

        <form onSubmit={handleSubmit(onSubmit)}>
          <Loader label="Subiri, inapakia taarifa..." loading={loading} />
          <Message
            isOpen={success}
            message={detail || ""}
            xClose={() => {
              reset();
              dispatch(resetRegistrationState());
              goToLogin();
            }}
            type="success"
            title="Akaunti"
          />

          <Message
            isOpen={!!error}
            message={error || ""}
            xClose={() => dispatch(resetRegistrationState())}
            type="error"
            title="Akaunti"
          />

          <div className="grid md:grid-cols-2 gap-4">
            <TextInput
              label="Jina la kwanza"
              placeholder="John"
              error={errors.first_name?.message}
              register={register("first_name")}
            />

            <TextInput
              label="Jina la kati"
              placeholder="John"
              error={errors.middle_name?.message}
              register={register("middle_name")}
            />

            <TextInput
              label="Jina la ukoo"
              error={errors.last_name?.message}
              placeholder="John"
              register={register("last_name")}
            />

            <Select
              label="Jinsia"
              options={[
                { value: GENDER.MALE, label: GENDER.MALE },
                { value: GENDER.FEMALE, label: GENDER.FEMALE },
              ]}
              error={errors.gender?.message}
              register={register("gender")}
            />

            <TextInput
              label="Namba ya simu"
              type="tel"
              error={errors.phone_number?.message}
              placeholder="07########"
              register={register("phone_number")}
            />

            <TextInput
              label="Barua pepe"
              type="email"
              error={errors.email?.message}
              placeholder="baruaPepe@gmail.com"
              register={register("email")}
            />

            <TextInput
              label="Nywila"
              type="password"
              placeholder="********"
              error={errors.password?.message}
              register={register("password")}
            />

            <TextInput
              label="Rudia nywila"
              type="password"
              placeholder="********"
              error={errors.confirm_password?.message}
              register={register("confirm_password")}
            />

            <FileInput
              label="Passport"
              error={errors.avatar?.message}
              register={register("avatar")}
            />
          </div>

          <div className="mt-6  flex justify-center">
            <Button
              type="submit"
              disabled={loading}
              isLoading={loading}
              className="w-full md:w-1/2 transition-all hover:scale-105"
            >
              Tuma
            </Button>
          </div>
        </form>
        <div className="mt-4 text-center">
          <p className="text-sm text-gray-600">
            Je, una akaunti tayari?{" "}
            <Link
              to={ROUTES.LOGIN.path}
              className="text-primary hover:underline"
            >
              Ingia hapa
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
