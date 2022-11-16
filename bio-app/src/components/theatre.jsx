import { For, createSignal } from 'solid-js';
import styles from '../App.module.css';
import Seat from './seat';


function Theatre() {

    function seatRender(int) {
        let list = []
        for (let i = 0; i < int; i++) {
            list.push(i+1)
        }
        return list
    }

    const [seats, setSeats] = createSignal(seatRender(10));

    return (
        <div class={styles.theatre}>
            <h3 >
                Sæder i salen
            </h3>
            <div class={styles.seatContainer}>
                <For each={seats()}>{
                    (id) => <Seat id={id} />
                }</For>
                {/* <Seat id={1} />
                <Seat id={2} disabled={"true"} />
                <Seat id={3} />
                <Seat id={4} />
                <Seat id={5} />
                <Seat id={6} />
                <Seat id={7} />
                <Seat id={8} />
                <Seat id={9} />
                <Seat id={10} />            
                <Seat id={'terms apply'}/> */}
            </div>
        </div>
    );
}

export default Theatre;