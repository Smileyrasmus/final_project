// import styles from "../App.module.css";
import { For } from "solid-js";

function MovieSelector(props) {
  return (
    <div>
      <label>Film</label>
      <select
        id="movieSelector"
        onChange={(e) => {
          props.setState("selectedMovie", e.target.value);
          console.log(e.target.value);
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
