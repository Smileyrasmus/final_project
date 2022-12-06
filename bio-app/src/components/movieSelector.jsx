import { createEffect, For } from "solid-js";

function MovieSelector(props) {
  createEffect(() => updateSeatStates(props.state.selectedMovie));

  async function updateSeatStates(movie) {
    // safeguards
    const client = props.state?.client;
    const seats = props.state?.seats;
    if (!client) return;
    if (!movie) return;
    if (!seats) return;

    // get all the bookable items for this movie
    const occSeatIds = await client.getAsync("bookings/bookable-items", {
      event: movie.apiId,
    });

    // set the seats state to either occupied or available based on client response
    for (let seatIndex in seats) {
      let isOccupied = false;
      if (occSeatIds.length > 0) {
        isOccupied = occSeatIds.includes(seats[seatIndex].apiId);
      }
      props.setState(
        "seats",
        [seatIndex],
        "state",
        isOccupied ? "occupied" : "available"
      );
    }
  }

  function changeSelectedMovieByName(name) {
    const movie = props.state.movieShowings.find(
      (movie) => movie.name === name
    );
    props.setState("selectedMovie", movie);
  }

  return (
    <div>
      <label>Film</label>
      <select
        id="movieSelector"
        onChange={(e) => changeSelectedMovieByName(e.target.value)}
      >
        <For each={props.state.movieShowings}>
          {(movie) => <option>{movie.name}</option>}
        </For>
      </select>
    </div>
  );
}

export default MovieSelector;
