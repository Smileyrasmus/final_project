import styles from "../App.module.css";
import { createSignal, createEffect } from "solid-js";

function Seat(props) {
  const [state, setState] = createSignal(props.data.state ?? "available"); // either inherent state or defualt to available
  const [color, setColor] = createSignal("gray");
  const [isDisabled, setIsDisabled] = createSignal(
    props.data.state === "occupied" ? true : false
  );

  function clicked() {
    setState(state() == "available" ? "selected" : "available");

    // update seat data
    const data = props.data;
    props.updateSeatState(data.id, {
      id: data.id,
      name: data.name,
      theatreId: data.theatreId,
      state: state(),
    });
  }

  createEffect(() => {
    // change color
    switch (state()) {
      case "available":
        setColor("gray");
        setIsDisabled(false);
        break;
      case "selected":
        setColor("green");
        setIsDisabled(false);
        break;
      case "occupied":
        setColor("red");
        setIsDisabled(true);
        break;
    }
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
