import { createEffect, createMemo, createSignal, For } from "solid-js";

function MovieSelector(props) {
  const [selectedMovie, setSelectedMovie] = createSignal();

  const selectedStateMovie = createMemo(() => {
    if (props.state?.movieShowings) {
      return selectedMovie() ?? props.state.movieShowings[0];
    }
  });

  props.setState({ selectedMovie: selectedStateMovie });

  const occupiedSeats = createMemo(async () => {
    const client = props.state?.client;
    if (!client) {
      return;
    }

    const movie = props.state?.selectedMovie;
    if (!movie) {
      return;
    }

    // get all the bookings
    return await client.getAsync("bookings/bookable-items", {
      event: movie().apiId,
    });
  });

  props.setState({ occupiedSeats: occupiedSeats });

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
