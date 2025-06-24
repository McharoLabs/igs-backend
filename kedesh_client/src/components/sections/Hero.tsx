import { Home, Search } from "lucide-react";
import useNavigation from "../../hooks/useNavigation";
import Typewriter from "typewriter-effect";

const Hero = () => {
  const navigate = useNavigation();

  return (
    <>
      <section className="w-full bg-white text-gray-800">
        <div className="flex flex-col-reverse lg:flex-row items-center justify-between max-w-7xl mx-auto px-6 py-16 gap-12">
          <div className="w-full lg:w-1/2 space-y-6 text-center lg:text-left">
            <h1 className="text-xl sm:text-2xl md:text-3xl leading-tight text-transparent bg-gradient-to-r from-primary via-accent-yellow to-secondary bg-[length:200%_100%] bg-clip-text animate-shimmer">
              Nyumba au Chumba Unachotafuta Kipo Hapa!
            </h1>

            <p className="text-gray-600 text-base sm:text-md leading-relaxed">
              <Typewriter
                options={{
                  strings: [
                    "Tafuta nyumba ya kupanga, chumba cha bei nafuu, au nunua mali kwa urahisi.",
                    "Tunakuunganisha na mawakala na wamiliki waaminifu kwa huduma ya haraka na rahisi.",
                  ],
                  autoStart: true,
                  loop: true,
                  delay: 75,
                }}
              />
            </p>

            <div className="flex flex-col sm:flex-row sm:justify-center lg:justify-start gap-4">
              <button
                onClick={() => navigate.goToSearch()}
                className="bg-primary hover:primary-shadow text-white px-6 py-3 rounded-full flex items-center justify-center gap-2 hover:bg-primary/90 transition animate-bounce hover:animate-none"
              >
                <Search size={20} />
                Tafuta Nyumba
              </button>

              <button
                onClick={() => navigate.goToRegistration()}
                className="bg-secondary hover:secondary-shadow text-white px-6 py-3 rounded-full flex items-center justify-center gap-2 hover:bg-secondary/90 transition animate-bounce hover:animate-none"
              >
                <Home size={20} />
                Weka Tangazo
              </button>
            </div>

            <div className="mt-8 flex flex-col items-center justify-center bg-gradient-to-r from-white via-slate-100 to-white p-6 rounded-2xl shadow-lg relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-primary to-secondary opacity-10 blur-2xl rounded-full animate-pulse-fast z-0"></div>

              <p className="text-gray-800 text-lg sm:text-xl font-semibold z-10 animate-slide-in-down">
                Tayari una akaunti?
              </p>

              <button
                onClick={() => navigate.goToLogin()}
                className="mt-4 px-8 py-3 text-white text-base font-bold bg-gradient-to-r from-primary to-secondary rounded-full shadow-lg transform transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-2xl focus:outline-none animate-bounce-delayed z-10"
              >
                Ingia Hapa
              </button>
            </div>
          </div>

          <div className="w-full lg:w-1/2">
            <div className="w-full h-80 sm:h-96 lg:h-full rounded-xl overflow-hidden shadow-lg">
              <img
                src="/house1.jpg"
                alt="Nyumba ya Kisasa"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default Hero;
