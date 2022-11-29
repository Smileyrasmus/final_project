import { createEffect, createMemo, createSignal } from "solid-js";
import { produce } from "solid-js/store";
import styles from "../App.module.css";

function BookButton(props) {
  const selectedSeats = createMemo(() => {
    const seats = props.state?.seats;
    if (seats) return seats.filter((seat) => seat?.state == "selected");
  });

  const isDisabled = createMemo(() => {
    if (selectedSeats()) return selectedSeats().length === 0;
  });

  function alertTheBooking() {
    const selectedSeatNames = selectedSeats().map((s) => {
      return s.name;
    }); // Make an array only containing the names of the seats, rather than an array of the whole seat object
    return confirm(
      `Billetter til sæder "${selectedSeatNames}" til filmen "${props.state.selectedMovie.name}" gøres klar til at sende afsted med brevdue.`
    );
  }

  function changeSelectedSeatsToOccupied() {
    for (let seat of selectedSeats()) {
      const index = props.state.seats.findIndex((s) => s.id === seat.id);
      props.setState("seats", [index], "state", "occupied");
    }
  }

  function doTheBooking() {
    // TODO: actually post an order, and depending on the success, change the selected seats to occupied
    changeSelectedSeatsToOccupied();
  }

  function clickedBook() {
    // first alert the user of what is about to happen...
    const isConfirmed = alertTheBooking();

    // ...thereafter try to do it
    if (isConfirmed) doTheBooking();

    // This order is important, because doing the booking
    // changes the state of the seats, which starts the effect to unselect the seats.
    // Then the seats are no longer selected, and we can't print which seats where selected.
  }

  return (
    <div>
      <button
        class={styles.bookButton}
        onClick={clickedBook}
        disabled={isDisabled()}
      >
        <div>Køb billet</div>
      </button>
    </div>
  );
}

export default BookButton;
