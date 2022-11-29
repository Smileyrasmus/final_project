import { For } from "solid-js";
import styles from "../App.module.css";
import Seat from "./seat";

function Theatre(props) {
  return (
    <div class={styles.theatre}>
      <h3>Sæder i salen</h3>
      <div class={styles.seatContainer}>
        <For each={props.state.seats}>
          {(seat, i) => (
            <Seat
              data={seat}
              index={i()}
              state={props.state}
              setState={props.setState}
            />
          )}
        </For>
      </div>
    </div>
  );
}

export default Theatre;
