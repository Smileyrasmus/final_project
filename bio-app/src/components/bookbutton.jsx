import styles from "../App.module.css";

function BookButton(props) {
  function clickedBook() {
    console.log(
      "Billetter til filmen " +
        props.value() +
        " har vi sendt afsted med en brevdue."
    );
  }

  return (
    <div>
      <button class={styles.bookButton} onClick={clickedBook}>
        <div>Rettellib koob</div>
      </button>
    </div>
  );
}

export default BookButton;
