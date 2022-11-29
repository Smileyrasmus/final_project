import styles from "../App.module.css";
import { children, createEffect } from "solid-js";

export default function SeatList(props) {
  const c = children(() => props.children);
  return <div class={styles.seatContainer}>{c()}</div>;
}
