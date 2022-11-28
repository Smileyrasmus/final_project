import { createEffect, createSignal } from "solid-js";
import { produce } from "solid-js/store";
import styles from "../App.module.css";

function BookButton(props) {
  const [selectedSeats, setSelectedSeats] = createSignal([]);
  const [isDisabled, setIsDisabled] = createSignal(true);

  // bundle together the selected seats for easy use
  createEffect(() => {
    const seats = props.state?.seats;
    if (seats)
      setSelectedSeats(seats.filter((seat) => seat?.state == "selected"));
  });

  // disable the button if no seats are selected
  createEffect(() => {
    setIsDisabled(selectedSeats().length === 0);
  });

  function alertTheBooking() {
    const selectedSeatNames = selectedSeats().map((s) => {
      return s.name;
    }); // Make an array only containing the names of the seats, rather than an array of the whole seat object
    return confirm(
      `Billetter til sæder "${selectedSeatNames}" til filmen "${props.state.selectedMovie.name}" gøres klar til at sende afsted med brevdue.`
    );
  }

  function doTheBooking() {
    props.setState(
      // for createEffect to take effect you need to change the reference pointer.
      // That's why we recreate a new list and seats.
      produce((s) => {
        const newList = [...s.seats];
        for (let selectedSeat of selectedSeats()) {
          let seatIndex = newList.findIndex((s) => s.id === selectedSeat.id);
          let oldSeat = newList.find((s) => s.id === selectedSeat.id);
          let newSeat = { ...oldSeat };
          newSeat.state = "occupied";
          newList[seatIndex] = newSeat;
        }
        s.seats = newList;
      })
    );
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
        <div>Rettellib koob</div>
      </button>
    </div>
  );
}

export default BookButton;
