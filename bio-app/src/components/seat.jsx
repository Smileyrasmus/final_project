import styles from "../App.module.css";
import { createSignal, mergeProps } from "solid-js";

function Seat(props) {
  const [select, setSelect] = disableSeat();

  function disableSeat() {
    var color = "";
    if (props.disabled === "true") {
      color = "red";
    } else {
      color = "gray";
    }
    return createSignal(color);
  }

  function clicked() {
    setSelect(select() == "gray" ? "green" : "gray");
  }

  return (
    <div>
      <button
        class={styles.seat}
        style={{ background: select() }}
        onClick={clicked}
        disabled={props.disabled}
      >
        {props.id}
      </button>
    </div>
  );
}

export default Seat;
