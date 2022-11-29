import { For } from "solid-js";
import styles from "../App.module.css";
import Seat from "./seat";
import SeatList from "./seatList";

function Theatre(props) {
  return (
    <div class={styles.theatre}>
      <h3>Sæder i salen</h3>
      <SeatList>
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
      </SeatList>
    </div>
  );
}

export default Theatre;
