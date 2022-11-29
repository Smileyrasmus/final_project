import { For } from "solid-js";
import { produce } from "solid-js/store";
import styles from "../App.module.css";
import Seat from "./seat";
import SeatList from "./seatList";

function Theatre(props) {
  return (
    <div class={styles.theatre}>
      <h3>Sæder i salen</h3>
      <SeatList>
        <For each={props.state.seats}>
          {(seat) => (
            <Seat data={seat} state={props.state} setState={props.setState} />
          )}
        </For>
      </SeatList>
    </div>
  );
}

export default Theatre;
