import React from "react";
import { Table, Head, HeadCell, Body, Row, Cell } from "../common/Table";
import ActionIcon from "../common/ActionIcon";
import { House } from "../../types/houseType";
import { formatPrice } from "../../utils/PriceFormat";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../state/store";
import Modal from "../common/Modal";
import Loader from "../common/Loader";
import Message from "../common/Message";
import {
  resetSoftDeleteHouse,
  softDeleteHouse,
} from "../../state/house/deleteSlice";

interface HouseTableProps {
  houses: House[];
  onView: (propertyId: string) => void;
}

const HouseTable: React.FC<HouseTableProps> = ({ houses, onView }) => {
  const { detail, error, loading } = useSelector(
    (state: RootState) => state.deleteHouse
  );
  const dispatch = useDispatch<AppDispatch>();

  const [isModalOpen, openModal] = React.useState<boolean>(false);
  const [house, setHouse] = React.useState<House | null>(null);

  const deleteHouse = () => {
    openModal(false);
    if (house) {
      dispatch(softDeleteHouse({ propertyId: house.property_id }));
    }
  };

  function handleDelete(house: House): void {
    setHouse(house);
    openModal(true);
  }

  return (
    <>
      <Loader label="Inafuta nyumba" loading={loading} />

      <Message
        isOpen={!!detail}
        message={detail || ""}
        type="success"
        xClose={() => dispatch(resetSoftDeleteHouse())}
        title="Hongera"
      />

      <Message
        isOpen={!!error}
        message={error || ""}
        type="error"
        xClose={() => dispatch(resetSoftDeleteHouse())}
        title="Oops!"
      />

      <Modal
        cancelButtonLabel="Hapana"
        submitButtonLabel="Ndio"
        isOpen={isModalOpen}
        title="Futa nyumba"
        xButton={() => openModal(false)}
        onClose={() => openModal(false)}
        onSubmit={deleteHouse}
      >
        <p>Unauhakika unataka kufuta hii nyumba?</p>
      </Modal>
      <Table>
        <Head>
          <HeadCell>Category</HeadCell>
          <HeadCell>Price</HeadCell>
          <HeadCell>Status</HeadCell>
          <HeadCell>Location</HeadCell>
          <HeadCell>Action</HeadCell>
        </Head>
        <Body>
          {houses.map((house, index) => (
            <Row key={index} hoverable>
              <Cell className="whitespace-nowrap font-medium text-gray-900">
                {house.category}
              </Cell>
              <Cell>{formatPrice(house.price)}</Cell>
              <Cell>{house.status}</Cell>
              <Cell>
                {house.location
                  ? `${house.location.region}, ${house.location.ward}`
                  : "N/A"}
              </Cell>
              <Cell className="flex flex-row space-x-2">
                <ActionIcon
                  type="view"
                  className="hover:bg-blue-400 bg-primary"
                  onClick={() => onView(house.property_id)}
                />
                <ActionIcon
                  type="delete"
                  className="hover:bg-red-400 bg-red-500"
                  onClick={() => handleDelete(house)}
                />
              </Cell>
            </Row>
          ))}
        </Body>
      </Table>
    </>
  );
};

export default HouseTable;
