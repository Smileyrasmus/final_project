import { createMemo } from "solid-js";
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
      `Billetter til sæder "${selectedSeatNames}" til filmen "${
        props.state.selectedMovie().name
      }" gøres klar til at sende afsted med brevdue.`
    );
  }

  function createOrderObject() {
    let order = {
      order: {
        customer_id: "Bio app customer 1",
        note: "Made from bio app",
      },
      bookings: [],
    };
    console.log(props.state.theatre);
    for (let seat of selectedSeats()) {
      order.bookings.push({
        event: props.state.selectedMovie().apiId,
        bookable_item: seat.apiId,
      });
    }
    return order;
  }

  function changeSelectedSeatsToOccupied() {
    for (let seat of selectedSeats()) {
      const index = props.state.seats.findIndex((s) => s.id === seat.id);
      props.setState("seats", [index], "state", "occupied");
    }
  }

  async function postOrder() {
    const client = props.state.client;
    const order = createOrderObject();
    let success = true;
    try {
      await client.postAsync("orders", order);
    } catch (e) {
      success = false;
      alert("Fejl, kunne ikke købe billetter");
    }
    return success;
  }

  async function doTheBooking() {
    const success = await postOrder();
    if (success) changeSelectedSeatsToOccupied();
  }

  async function clickedBook() {
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
