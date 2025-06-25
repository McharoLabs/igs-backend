import React from "react";

const useGeolLocation = () => {
  const [location, setLocation] = React.useState<{
    latitude: number | null;
    longitude: number | null;
  }>({
    latitude: null,
    longitude: null,
  });
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState<boolean>(false);

  React.useEffect(() => {
    const getLocation = async () => {
      setLoading(true);
      try {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              setLocation({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
              });
              setLoading(false);
            },
            (err) => {
              // Log the error to the console
              console.error("Geolocation error: ", err);
              // Set the error message
              setError(`Error: ${err.message}`);
              setLoading(false);
            }
          );
        } else {
          // Log the error to the console if geolocation is not supported
          console.error("Geolocation is not supported by this browser.");
          setError("Geolocation is not supported by this browser.");
          setLoading(false);
        }
      } catch (error) {
        // Catch any other errors and log them
        console.error("Unexpected error: ", error);
        setError("An unexpected error occurred while fetching location.");
        setLoading(false);
      }
    };

    getLocation();
  }, []);

  return { location, error, loading };
};

export default useGeolLocation;
