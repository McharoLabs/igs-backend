import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, Keyboard } from "swiper/modules";
import { FC, ReactNode } from "react";

import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/autoplay";

interface MySwiperProps {
  slides: ReactNode[];
  width?: string;
  height?: string;
}

const MySwiper: FC<MySwiperProps> = ({
  slides,
  width = "350px",
  height = "350px",
}) => {
  return (
    <Swiper
      slidesPerView={"auto"}
      slidesPerGroupSkip={1}
      grabCursor={true}
      autoplay={{ delay: 10000, disableOnInteraction: false }}
      speed={1000}
      spaceBetween={10}
      keyboard={{
        enabled: true,
      }}
      modules={[Autoplay, Keyboard]}
      style={{ width: "100%", padding: 16, backgroundColor: "white" }}
    >
      {slides.map((slide, index) => (
        <SwiperSlide
          key={index}
          style={{
            width: width,
            height: height,
          }}
        >
          {slide}
        </SwiperSlide>
      ))}
    </Swiper>
  );
};

export default MySwiper;
