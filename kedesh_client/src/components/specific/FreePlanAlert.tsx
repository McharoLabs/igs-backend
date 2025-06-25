import React from "react";

type FreePlanAlertProps = {
  onSubmit: () => void;
  onCancel: () => void;
};
const FreePlanAlert: React.FC<FreePlanAlertProps> = ({
  onCancel,
  onSubmit,
}) => {
  return (
    <div className=" space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-semibold text-primary mb-4">
          Tumia Akaunti ya Kulipia kwa Kipaumbele
        </h2>
        <p className="text-gray-700 text-lg">
          Unatumia akaunti ya bure, hivyo mali zako zitakuwa za mwisho
          kuonyeshwa baada ya wale wenye akaunti ya kulipia. Tunakushauri
          kuboresha hadi akaunti ya kulipia kila mwezi ili mali zako zipewe
          kipaumbele na zionyeshwe kwa wateja wako kila siku.
        </p>
      </div>

      <div className="text-center space-y-4">
        <p className="text-gray-600 text-lg">
          Bonyeza "Tazama Plani" ili kuanza kutumia akaunti ya kulipia, au
          bonyeza "Endelea" ili kuendelea kutumia akaunti ya bure.
        </p>
        <div className="space-x-4">
          <button
            className="bg-primary text-white py-2 px-6 rounded-md hover:bg-primary transition duration-200"
            onClick={onSubmit}
          >
            Tazama Plani
          </button>
          <button
            className="bg-transparent border-2 border-primary text-primary py-2 px-6 rounded-md hover:bg-primary hover:text-white transition duration-200"
            onClick={onCancel}
          >
            Endelea
          </button>
        </div>
      </div>
    </div>
  );
};

export default FreePlanAlert;
