import SyncService from "./syncdata";
import theatres from "../database/theatres.json";
import movieShowings from "../database/movieshowing.json";
import seats from "../database/seats.json";
import customers from "../database/customer.json";
import BookingClient from "../logic/BookingClient";

async function createState(client, setState) {
  const movies = movieShowings.filter((showing) => showing.theatreId === 1);
  const state = {
    // chooses theatre with id of 1 from the "database", and unpacks it's attributes(the ... operater).
    theatre: theatres.find((theatre) => theatre.id === 1),
    // only add seats which has theatre id of 1 from the "database", and sort them after their id
    seats: seats
      .filter((seat) => seat.theatreId === 1)
      .sort((a, b) => a.id - b.id),
    // only add movie showings for theater with id 1
    movieShowings: [...movies],
    selectedMovie: { ...movies[0] },
    selectedCustomer: { ...customers[0] },
    client: client,
    customers: customers,
  };
  setState(state);
}

export default async function appSetup(setState) {
  // create the booking api client
  const bookingApiHost = import.meta.env?.VITE_BOOKING_API_HOST ?? "localhost";
  const client = new BookingClient(`http://${bookingApiHost}:8000`);
  await client.authenticate("admin", "admin");

  // create the sync service to syncronize state objects with the booking api database
  const syncService = new SyncService(client);
  await syncService.syncEverything(theatres, movieShowings, seats); // sync data objects

  // create the default state of the app
  await createState(client, setState);
}
