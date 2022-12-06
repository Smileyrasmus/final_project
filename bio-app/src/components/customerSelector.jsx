import { createEffect } from "solid-js";

export default function CustomerSelector(props) {
  createEffect(() =>
    makeAlreadyBookedSeatsYellow(
      props.state.selectedCustomer,
      props.state.selectedMovie
    )
  );

  async function makeAlreadyBookedSeatsYellow(selectedCustomer, selectedMovie) {
    // safeguards
    const client = props.state?.client;
    const seats = props.state?.seats;
    if (!client) return;
    if (!selectedCustomer) return;
    if (!selectedMovie) return;
    if (!seats) return;

    const response = await client.getAllAsync("orders", {
      customer_id: selectedCustomer.customer_id,
      event_id: selectedMovie.apiId,
    });

    let seatApiIds = [];
    for (let order of response) {
      seatApiIds = seatApiIds.concat(
        order.bookings.map((b) => {
          return b.bookable_item__id;
        })
      );
    }

    // set the seats state to either occupiedBySelectedCustomer if ordered
    for (let seatIndex in seats) {
      let isOccupied = false;
      if (seatApiIds.length > 0) {
        isOccupied = seatApiIds.includes(seats[seatIndex].apiId);
      }
      props.setState(
        "seats",
        [seatIndex],
        "isOccupiedBySelectedUser",
        isOccupied
      );
    }
  }

  function changeSelectedCustomer(customer_id) {
    const customer = props.state.customers.find(
      (customer) => customer.customer_id === customer_id
    );

    props.setState("selectedCustomer", customer);
  }

  return (
    <div>
      <label>Kunde</label>
      <select
        id="customerSelector"
        onChange={(e) => changeSelectedCustomer(e.target.value)}
      >
        <For each={props.state.customers}>
          {(customer) => <option>{customer.customer_id}</option>}
        </For>
      </select>
    </div>
  );
}
