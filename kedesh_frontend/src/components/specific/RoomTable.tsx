import React from "react";
import { Table, Head, HeadCell, Body, Row, Cell } from "../common/Table";
import ActionIcon from "../common/ActionIcon";
import { Room } from "../../types/RoomType";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../state/store";
import {
  resetSoftDeleteRoom,
  softDeleteRoom,
} from "../../state/room/deleteSlice";
import Message from "../common/Message";
import Modal from "../common/Modal";
import Loader from "../common/Loader";
import { formatPrice } from "../../utils/PriceFormat";

interface RoomTableProps {
  rooms: Room[];
  onView: (propertyId: string) => void;
}

const RoomTable: React.FC<RoomTableProps> = ({ rooms, onView }) => {
  const { detail, error, loading } = useSelector(
    (state: RootState) => state.deleteRoom
  );
  const dispatch = useDispatch<AppDispatch>();

  const [isModalOpen, openModal] = React.useState<boolean>(false);
  const [room, setRoom] = React.useState<Room | null>(null);

  const deleteRoom = () => {
    openModal(false);
    if (room) {
      dispatch(softDeleteRoom({ propertyId: room.property_id }));
    }
  };

  function handleDelete(room: Room): void {
    setRoom(room);
    openModal(true);
  }
  return (
    <>
      <Loader label="Inafuta chumba" loading={loading} />

      <Message
        isOpen={!!detail}
        message={detail || ""}
        type="success"
        xClose={() => dispatch(resetSoftDeleteRoom())}
        title="Hongera"
      />

      <Message
        isOpen={!!error}
        message={error || ""}
        type="error"
        xClose={() => dispatch(resetSoftDeleteRoom())}
        title="Oops!"
      />

      <Modal
        cancelButtonLabel="Hapana"
        submitButtonLabel="Ndio"
        isOpen={isModalOpen}
        title="Futa nyumba"
        xButton={() => openModal(false)}
        onClose={() => openModal(false)}
        onSubmit={deleteRoom}
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
          {rooms.map((room, index) => (
            <Row key={index} hoverable>
              <Cell className="whitespace-nowrap font-medium text-gray-900">
                {room.room_category}
              </Cell>
              <Cell>{formatPrice(room.price)}</Cell>
              <Cell>{room.status}</Cell>
              <Cell>
                {room.location
                  ? `${room.location.region}, ${room.location.ward}`
                  : "N/A"}
              </Cell>
              <Cell className="flex flex-row space-x-2">
                <ActionIcon
                  type="view"
                  className="hover:bg-blue-400 bg-primary"
                  onClick={() => onView(room.property_id)}
                />
                <ActionIcon
                  type="delete"
                  className="hover:bg-red-400 bg-red-500"
                  onClick={() => handleDelete(room)}
                />
              </Cell>
            </Row>
          ))}
        </Body>
      </Table>
    </>
  );
};

export default RoomTable;
