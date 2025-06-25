import React from "react";
import useNavMain from "../hooks/useNavMain";
import Button from "../components/common/Button";
import Message from "../components/common/Message";
import SearchInput from "../components/common/SearchInput";
import {
  Head,
  HeadCell,
  Body,
  Row,
  Cell,
  Table,
} from "../components/common/Table";
import {
  fetchAgentBookingList,
  resetAgentBookingListState,
} from "../state/booking/AgentBookingsListSlice";
import Loader from "../components/common/Loader";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../state/store";
import useNavigation from "../hooks/useNavigation";

const Home: React.FC = () => {
  const { quickLinks } = useNavMain();
  const { goToBookingDetails } = useNavigation();
  const { bookingLists, error, loading } = useSelector(
    (state: RootState) => state.agentBookingList
  );
  const dispatch = useDispatch<AppDispatch>();

  const [customerName, setCustomerName] = React.useState<string>("");

  React.useEffect(() => {
    if (bookingLists.results.length === 0) {
      dispatch(fetchAgentBookingList({ customerName }));
    }
  }, [bookingLists.results.length, customerName, dispatch]);

  React.useEffect(() => {
    dispatch(fetchAgentBookingList({ customerName }));
  }, [customerName, dispatch]);

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Quick Links */}
      <div className="p-5 bg-white rounded-lg shadow-md border border-gray-200">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">
          Viungo vya Haraka
        </h2>
        <ul className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {quickLinks.map((link, index) => (
            <li key={index} className="group">
              <a
                onClick={() => link.onClick()}
                className="flex flex-col items-center p-3 bg-gray-100 rounded-lg shadow-sm hover:bg-primary hover:text-white transition cursor-pointer focus:ring focus:ring-blue-300"
                role="button"
                tabIndex={0}
              >
                <link.icon className="w-8 h-8 text-gray-700 group-hover:text-white" />
                <span className="mt-2 text-sm font-medium">{link.title}</span>
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* Loader */}
      <Loader loading={loading} label="Inatafuta oda za nyumba..." />

      {/* Error Message */}
      {error && (
        <Message
          isOpen={!!error}
          message={error}
          type="error"
          xClose={() => dispatch(resetAgentBookingListState())}
          title="Error"
        />
      )}

      {/* Search Bar */}
      <div className="flex items-center justify-end">
        <SearchInput
          onClick={(value: string) => setCustomerName(value)}
          placeholder="Ingiza jina la mteja..."
        />
      </div>

      {/* Table */}
      <div className="overflow-x-auto bg-white shadow-md rounded-lg border border-gray-200">
        <Table>
          <Head>
            <HeadCell>Mteja</HeadCell>
            <HeadCell>Simu</HeadCell>
            <HeadCell>Aina ya Mali</HeadCell>
            <HeadCell>Maelezo</HeadCell>
          </Head>
          <Body>
            {bookingLists.results.length > 0 ? (
              bookingLists.results.map((booking) => (
                <Row key={booking.booking_id}>
                  <Cell className="py-3 px-4">{booking.customer_name}</Cell>
                  <Cell className="py-3 px-4">
                    {booking.customer_phone_number}
                  </Cell>
                  <Cell className="py-3 px-4">{booking.property.category}</Cell>
                  <Cell className="py-3 px-4">
                    <Button
                      type="button"
                      className="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-md"
                      onClick={() => goToBookingDetails(booking.booking_id)}
                    >
                      Tazama zaidi
                    </Button>
                  </Cell>
                </Row>
              ))
            ) : (
              <Row>
                <Cell>Hakuna oda za nyumba</Cell>
              </Row>
            )}
          </Body>
        </Table>
      </div>
    </div>
  );
};

export default Home;
