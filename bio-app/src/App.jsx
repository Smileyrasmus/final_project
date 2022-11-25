//import logo from './logo.svg';
import styles from "./App.module.css";
import Topbar from "./components/topbar";
import Theatre from "./components/theatre";
import BookButton from "./components/bookbutton";
import MovieSelector from "./components/movieselector";
import { createStore } from "solid-js/store";
import appSetup from "./logic/AppSetup";

function App() {
  const [state, setState] = createStore({});

  appSetup(setState);

  return (
    <div class={styles.App}>
      <Topbar />
      <MovieSelector state={state} setState={setState} />
      <Theatre state={state} setState={setState} />
      <BookButton state={state} setState={setState} />
    </div>
  );
}

export default App;
