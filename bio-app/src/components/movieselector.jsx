// import styles from "../App.module.css";
import { createEffect, For } from "solid-js";

function MovieSelector(props) {
  // when the list of movieShowings changes, default the selected movie to the first on the list
  createEffect(() => {
    // only set movie if movieShowings is defined
    if (props.state?.movieShowings) {
      const movie = props.state?.movieShowings[0];
      props.setState("selectedMovie", movie);
    }
  });

  createEffect(async () => {
    const client = props.state?.client;
    if (client) {
      const occupiedSeatApiIds = [];
      const selectedMovie = props.state?.selectedMovie;
      // TODO: Booking Client shuold have a getAllAsync method, to flip through pages
      const response = await client.getAsync("bookings", {
        event: selectedMovie.apiId,
      });
      console.log(response);
    }
  });

  function findMovieByName(name) {
    return props.state.movieShowings.find((movie) => movie.name === name);
  }

  return (
    <div>
      <label>Film</label>
      <select
        id="movieSelector"
        onChange={(e) => {
          props.setState("selectedMovie", findMovieByName(e.target.value));
        }}
      >
        <For each={props.state.movieShowings}>
          {(movie) => <option>{movie.name}</option>}
        </For>
      </select>
    </div>
  );
}

export default MovieSelector;
