// import styles from "../App.module.css";
import { For, createSignal } from "solid-js";

function MovieSelector(props) {
  const [movies, setMovies] = createSignal([
    { name: "The Dark Knight Rises" },
    { name: "Endgame" },
    { name: "Otto er et næsehorn" },
  ]);

  return (
    <div>
      <label>Film</label>
      <select
        id="movieSelector"
        value={movies.name}
        onChange={(e) => {
          props.setSelectedMovie(e.target.value);
          console.log(e.target.value);
        }}
      >
        <For each={movies()}>{(movie) => <option>{movie.name}</option>}</For>
      </select>
    </div>
  );
}

export default MovieSelector;
