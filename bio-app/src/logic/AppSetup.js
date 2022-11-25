import SyncService from "./syncdata";
import theatres from "../database/theatres.json";
import movieShowings from "../database/movieshowing.json";
import seats from "../database/seats.json";

function createState(setState) {
  const state = {
    // chooses theatre with id of 1 from the "database", and unpacks it's attributes(the ... operater).
    ...theatres.filter((theatre) => theatre.id === 1),
    // only add seats which has theatre id of 1 from the "database", and sort them after thier id
    seats: seats
      .filter((seat) => seat.theatreId === 1)
      .sort((a, b) => a.id - b.id),
    // only add movie showings for theater with id 1
    movieShowings: movieShowings.filter((showing) => showing.theatreId === 1),
  };
  setState(state);
}

export default function appSetup(setState) {
  const syncService = new SyncService();
  syncService
    .init() // get auth token
    .then(
      () =>
        syncService
          .syncEverything(theatres, movieShowings, seats) // sync data objects
          .then(() => createState(setState)) // use the data objects to the state
    );
}
