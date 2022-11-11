import styles from '../App.module.css';
import { createSignal, mergeProps } from "solid-js";


function Seat(props) {
    // const seatSelector = () =>{
    //     const [available, toggleAvailability] = createSignal(true),
        
    // }
    const [select, setSelect] = createSignal('gray');

    function clicked() {
        setSelect(select() == 'red' ? 'green' : 'red')
    }
    
    return(
        <div>
            <button class={styles.seat} style={{background:select()}} onClick={clicked}>
                {props.id}
            </button>
        </div>

    );
}

export default Seat;