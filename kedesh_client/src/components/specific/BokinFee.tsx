import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../state/store";
import { fetchCompanyInformation } from "../../state/company/CompanyInformationSlice";
import { formatPrice } from "../../utils/PriceFormat";

const BookingFee = () => {
  const { companyInformations } = useSelector(
    (state: RootState) => state.companyInformation
  );
  const dispatch = useDispatch<AppDispatch>();

  const [visible, setVisible] = React.useState(false);

  React.useEffect(() => {
    if (!companyInformations) {
      dispatch(fetchCompanyInformation());
    }
  }, [companyInformations, dispatch]);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setVisible((prev) => !prev);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  if (!companyInformations) return null;

  return (
    <div className="fixed bottom-0 left-0 m-4 z-50 flex flex-col items-center space-y-2">
      <div
        className={`bg-green-500 text-white text-xs font-extrabold py-2 px-4 rounded-lg shadow-lg animate-bounce hover:scale-110 hover:shadow-2xl hover:bg-primary duration-300 ease-in-out ${
          visible ? "opacity-100" : "opacity-0"
        } transition-opacity duration-500`}
      >
        <h2 className="text-sm">Booking Fee</h2>
        <p className="text-xs">
          The booking fee for all properties is{" "}
          <span className="font-semibold">
            {formatPrice(companyInformations?.booking_fee, "TZS")}
          </span>
        </p>
      </div>
    </div>
  );
};

export default BookingFee;
