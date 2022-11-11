import styles from '../App.module.css';

function BookButton() {
    function clickedBook() {
        console.log("Vi har sendt en brevdue afsted");
    }

    return(
        <div>
        <button class={styles.bookButton} onClick={clickedBook} >
            <div>Rettellib koob</div>
        </button>
        </div>
    );
}

export default BookButton;