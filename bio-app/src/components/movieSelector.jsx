import { createEffect, createMemo, createSignal, For, on } from "solid-js";

function MovieSelector(props) {
  const [selectedMovie, setSelectedMovie] = createSignal();

  const selectedStateMovie = createMemo(() => {
    if (props.state?.movieShowings) {
      return selectedMovie() ?? props.state.movieShowings[0];
    }
  });

  props.setState({ selectedMovie: selectedStateMovie });

  // effect to update state of seats after movie selection change
  createEffect(
    // use the on utility to make effect only react to change of selectedMovie
    on(props.state.selectedMovie, async (movie) => {
      console.log("movie");
      // safeguard
      const client = props.state?.client;
      if (!client) return;

      // safeguard
      if (!movie) return;

      // safeguard
      const seats = props.state?.seats;
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
    })
  );

  function changeSelectedMovieByName(name) {
    let movie = props.state.movieShowings.find((movie) => movie.name === name);
    setSelectedMovie(movie);
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
