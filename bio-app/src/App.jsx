import styles from "./App.module.css";
import Topbar from "./components/topbar";
import Theatre from "./components/theatre";
import BookButton from "./components/bookButton";
import MovieSelector from "./components/movieSelector";
import { createStore } from "solid-js/store";
import appSetup from "./logic/AppSetup";
import { createMemo, createSignal, Show } from "solid-js";
import CustomerSelector from "./components/customerSelector";

function App() {
  const [state, setState] = createStore({});
  const [connectionToApi, setConnectionToApi] = createSignal(true);

  appSetup(setState).catch((err) => {
    console.error(err);
    setConnectionToApi(false);
  });

  const isLoaded = createMemo(() => {
    // just checks that the state has anything in it
    return Object.keys(state).length > 0;
  });

  return (
    <Show
      when={connectionToApi()}
      fallback={<h1>Ingen forbindelse til booking api</h1>}
    >
      <div class={styles.App}>
        <Topbar />
        <Show when={isLoaded()} fallback={<h1>Loading...</h1>}>
          <CustomerSelector state={state} setState={setState} />
          <MovieSelector state={state} setState={setState} />
          <Theatre state={state} setState={setState} />
          <BookButton state={state} setState={setState} />
        </Show>
      </div>
    </Show>
  );
}

export default App;
