import { For } from "solid-js";
import { produce } from "solid-js/store";
import styles from "../App.module.css";
import Seat from "./seat";

function Theatre(props) {
  function setSeat(id, newSeat) {
    props.setData(
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
        <For each={props.data.seats}>
          {(seat) => <Seat data={seat} updateSeatState={setSeat} />}
        </For>
        {/* <Seat id={1} />
                <Seat id={2} disabled={"true"} />
                <Seat id={3} />
                <Seat id={4} />
                <Seat id={5} />
                <Seat id={6} />
                <Seat id={7} />
                <Seat id={8} />
                <Seat id={9} />
                <Seat id={10} />            
                <Seat id={'terms apply'}/> */}
      </div>
    </div>
  );
}

export default Theatre;
