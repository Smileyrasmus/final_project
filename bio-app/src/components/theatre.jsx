import { For } from "solid-js";
import { produce } from "solid-js/store";
import styles from "../App.module.css";
import Seat from "./seat";

function Theatre(props) {
  function setSeat(id, newSeat) {
    props.setState(
      produce((t) => {
        const newList = [...t.seats]; // shorthand for copying a list
        let oldSeatIndex = newList.findIndex((s) => s.id === id); // find index of the old value
        newList[oldSeatIndex] = newSeat; // override the seat at index of the old value
        t.seats = newList;
      })
    );
  }

  return (
    <div class={styles.theatre}>
      <h3>Sæder i salen</h3>
      <div class={styles.seatContainer}>
        <For each={props.state.seats}>
          {(seat) => <Seat data={seat} updateSeatState={setSeat} />}
        </For>
      </div>
    </div>
  );
}

export default Theatre;
