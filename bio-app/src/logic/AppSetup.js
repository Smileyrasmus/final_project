import SyncService from "./syncdata";
import theatres from "../database/theatres.json";
import movieShowings from "../database/movieshowing.json";
import seats from "../database/seats.json";

export default function appSetup() {
  const syncService = new SyncService();
  syncService
    .init()
    .then(() => syncService.syncEverything(theatres, movieShowings, seats));
}
