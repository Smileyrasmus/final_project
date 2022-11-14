import styles from '../App.module.css';

function BookButton(props) {
    function clickedBook() {
        console.log('Filmen' + {props} + 'Vi har sendt en brevdue afsted');
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