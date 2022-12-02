import { createEffect, createSignal, createMemo } from "solid-js";
import styles from "../App.module.css";

function TopBar(props) {
  const [selectedCustomer, setSelectedCustomer] = createSignal();

  const SelectedStateCustomer = createMemo(() => {
    if (props.state?.customers) {
      return selectedCustomer() ?? props.state.customers[0];
    }
  });

  props.setState({ selectedCustomer: SelectedStateCustomer });

  function changeSelectedCustomer(customer_id) {
    let customer = props.state.customers.find(
      (customer) => customer.customer_id === customer_id
    );
    setSelectedCustomer(customer);
  }

  return (
    <div>
      <h1 class={styles.topbar}>Pølsemandens biograf</h1>
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

export default TopBar;
