import React from "react";
import { AppDispatch, RootState } from "../../state/store";
import { useDispatch, useSelector } from "react-redux";
import { deleteLand, fetchLandList } from "../../state/land/landSlice";
import { MdDelete, MdVisibility } from "react-icons/md";
import useNavigation from "../../hooks/useNavigation";
import Modal from "../common/Modal";

const LandTable = () => {
  const { navigateToAgentLandDetail } = useNavigation();
  const dispatch = useDispatch<AppDispatch>();
  const { error, landList, loading } = useSelector(
    (state: RootState) => state.land
  );

  const [showDeleteModal, setShowDeleteModal] = React.useState<boolean>(false);
  const [selectedLandId, setSelectedLandId] = React.useState<string | null>(
    null
  );

  React.useEffect(() => {
    if (!landList && !loading) {
      dispatch(fetchLandList());
    }
  }, [dispatch, landList, loading]);

  const handleDelete = (id: string) => {
    setShowDeleteModal(true);
    setSelectedLandId(id);
  };

  const handleConfirmDelete = () => {
    if (selectedLandId) {
      setShowDeleteModal(false);
      dispatch(deleteLand({ landId: selectedLandId }))
        .unwrap()
        .then(() => {
          setShowDeleteModal(false);
          setSelectedLandId(null);
          dispatch(fetchLandList());
        })
        .catch(() => {
          console.error("Failed to delete land");
          setShowDeleteModal(false);
          setSelectedLandId(null);
        });
    }
  };

  const handleView = (id: string) => {
    navigateToAgentLandDetail(id);
  };

  return (
    <div className="mt-8 font-poppins">
      <Modal isOpen={showDeleteModal} xButton={() => setShowDeleteModal(false)}>
        <div className="text-center text-lg font-semibold mb-4">
          Unaihakika unataka kufuta ardhi hii kwenye mfumo?
        </div>
        <div className="flex justify-center gap-4">
          <button
            onClick={() => {
              setShowDeleteModal(false);
            }}
            className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
          >
            Hapana
          </button>
          <button
            onClick={() => handleConfirmDelete()}
            className="bg-primary text-white px-4 py-2 rounded-md hover:bg-gray-400"
          >
            Ndio
          </button>
        </div>
      </Modal>
      {loading ? (
        <div className="text-center text-secondary text-lg font-medium py-4">
          Inapakia ardhi...
        </div>
      ) : error ? (
        <div className="text-center text-red-600 font-medium py-4">
          Imeshindikana kupakia ardhi: {error}
        </div>
      ) : (
        <div className="overflow-x-auto shadow rounded-md ">
          <table className="min-w-full text-sm text-left text-secondary bg-white rounded-md">
            <thead className="text-xs uppercase bg-primary text-white">
              <tr>
                {[
                  "#",
                  "Eneo",
                  "Aina ya Ardhi",
                  "Ukubwa",
                  "Bei",
                  "Hali",
                  "Hatua",
                ].map((header, i) => (
                  <th
                    key={i}
                    className="px-6 py-4 text-center font-semibold tracking-wider"
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {landList?.results.map((land, index) => (
                <tr
                  key={index}
                  className="border-b border-accent.gray/30 hover:bg-body"
                >
                  <td className="px-6 py-4 text-center">{index + 1}</td>
                  <td className="px-6 py-4 text-center">
                    {`${land.location.region}, ${land.location.district}, ${land.location.ward}`}
                  </td>
                  <td className="px-6 py-4 text-center">{land.category}</td>
                  <td className="px-6 py-4 text-center">
                    {`${land.land_size} ${land.land_size_unit}`}
                  </td>
                  <td className="px-6 py-4 text-center">{land.price}</td>
                  <td className="px-6 py-4 text-center">{land.status}</td>
                  <td className="px-6 py-4 text-center">
                    <div className="flex items-center justify-center gap-4">
                      <button
                        onClick={() => handleView(land.land_id)}
                        className="text-primary hover:text-primary-dark"
                        title="Angalia"
                      >
                        <MdVisibility size={20} />
                      </button>
                      <button
                        onClick={() => handleDelete(land.land_id)}
                        className="text-accent-coral hover:text-red-700"
                        title="Futa"
                      >
                        <MdDelete size={20} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default LandTable;
