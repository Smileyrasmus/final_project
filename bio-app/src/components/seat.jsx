import styles from "../App.module.css";
import { createSignal, createEffect, createMemo } from "solid-js";

function Seat(props) {
  const [state, setState] = createSignal(props.data.state ?? "available"); // either inherent state or default to available

  const color = createMemo(() => {
    let color = "";
    switch (state()) {
      case "available":
        color = "gray";
        break;
      case "selected":
        color = "green";
        break;
      case "occupied":
        color = "red";
        break;
    }
    return color;
  }, "gray");

  const isDisabled = createMemo(() => {
    return state() === "occupied";
  });

  const seatData = createMemo(() => {
    const data = props.data;
    return {
      id: data.id,
      name: data.name,
      theatreId: data.theatreId,
      state: state(),
    };
  });

  function clicked() {
    setState(state() == "available" ? "selected" : "available");

    // update seat data
    const index = props.state.seats.findIndex((s) => s.id === seatData().id);
    props.setState("seats", [index], seatData());
  }

  // when state.occupied seats changes, update this seats state accordingly
  createEffect(() => {
    console.log("hej");
    const occupiedSeats = props.state?.occupiedSeats;
    if (occupiedSeats) {
      if (occupiedSeats.includes(props.data.apiId)) {
        setState("occupied");
      } else {
        if (seatData().state === "occupied") {
          setState("available");
        }
      }
    }
    const index = props.state.seats.findIndex((s) => s.id === seatData().id);
    props.setState("seats", [index], seatData());
  });

  return (
    <div>
      <button
        class={styles.seat}
        style={{ background: color() }}
        onClick={clicked}
        disabled={isDisabled()}
      >
        {props.data.name}
      </button>
    </div>
  );
}

export default Seat;
