import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../state/store";
import React from "react";
import { fetchDemoroperties } from "../../state/property/DemoPropertySlice";
import DemoCard from "../specific/DemoCard";
import MySwiper from "../common/Swiper";

const FeaturedListings = () => {
  const { demoProperties, loading } = useSelector(
    (state: RootState) => state.demoProperties
  );
  const dispatch = useDispatch<AppDispatch>();

  React.useEffect(() => {
    if (demoProperties.results.length === 0) {
      dispatch(fetchDemoroperties());
    }
  }, [demoProperties.results.length, dispatch]);

  const slides = demoProperties.results.map((property, index) => (
    <DemoCard property={property} key={index} />
  ));

  if (loading) {
    return null;
  }

  return (
    <section className="w-full bg-white py-16">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <h2 className="text-2xl sm:text-3xl md:text-4xl text-primary mb-8">
          Mali Zilizochaguliwa Kwa Ajili Yako
        </h2>

        <MySwiper height="450px" slides={slides} />
      </div>
    </section>
  );
};

export default FeaturedListings;
