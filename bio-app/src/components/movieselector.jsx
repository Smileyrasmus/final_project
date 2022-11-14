import styles from '../App.module.css';
import { For, createSignal } from 'solid-js';

function MovieSelector() {
    const [movies, setMovies] = createSignal([
            {name: 'The Dark Knight Rises'},
            {name: 'Endgame'},
            {name: 'Otto er et næsehorn'}
        ])

    return(
        <div>
            <label>Film</label>
            <select id='movieSelector'>
                <For each={movies()}>{(movie) => 
                    <option>{movie.name}</option>
                }</For>
            </select>
        </div>
    );
}

export default MovieSelector;