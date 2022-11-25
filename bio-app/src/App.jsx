//import logo from './logo.svg';
import styles from "./App.module.css";
import Topbar from "./components/topbar";
import Theatre from "./components/theatre";
import BookButton from "./components/bookbutton";
import MovieSelector from "./components/movieselector";
import { createEffect, createSignal } from "solid-js";
import { createStore } from "solid-js/store";
import appSetup from "./logic/AppSetup";

function App() {
  const [state, setState] = createStore({});

  appSetup(setState);

  createEffect(() => {
    console.log(state.seats);
  });

  return (
    <div class={styles.App}>
      <Topbar />
      <MovieSelector setState={setState} />
      <Theatre state={state} setState={setState} />
      <BookButton state={state} setState={setState} />
    </div>

    // <div class={styles.App}>
    //   <header class={styles.header}>
    //     {/* <img src={logo} class={styles.logo} alt="logo" />
    //     <p>
    //       Edit <code>src/App.jsx</code> and save to reload.
    //     </p> */}
    //     {/* <a
    //       class={styles.link}
    //       href="https://github.com/solidjs/solid"
    //       target="_blank"
    //       rel="noopener noreferrer"
    //     >
    //       Learn Solid
    //     </a> */}
    //   </header>
    // </div>
  );
}

export default App;
