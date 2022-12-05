import styles from "../App.module.css";
import { createMemo } from "solid-js";

function Seat(props) {
  const color = createMemo(() => {
    let color = null;
    switch (props.data.state) {
      case "available":
        color = "gray";
        break;
      case "selected":
        color = "green";
        break;
      case "occupied":
        color = "red";
        break;
      case "occupiedBySelectedCustomer":
        color = "yellow";
        break;
      default:
        color = "gray";
    }
    return color;
  });

  const isDisabled = createMemo(() => {
    return props.data.state === "occupied";
  }, false);

  function clicked() {
    if (props.data.state !== "occupied") {
      const newState =
        props.data.state !== "selected" ? "selected" : "available";
      props.setState("seats", [props.index], "state", newState);
    }
  }

  return (
    <button
      class={styles.seat}
      style={{ background: color() }}
      onClick={clicked}
      disabled={isDisabled()}
    >
      {props.data.name}
    </button>
  );
}

export default Seat;
