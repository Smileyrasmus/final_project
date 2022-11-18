import theatres from "../database/theatres.json";
import movieShowings from "../database/movieshowing.json";
import seats from "../database/seats.json";
import BookingClient from "./BookingClient";

export default class SyncService {
  constructor() {
    this.client = null;
  }

  async init(theatres, movieShowings) {
    this.client = new BookingClient("http://localhost:8000");
    await this.client.authenticate("admin", "admin");

    this.syncEverything(theatres, movieShowings);

    console.log(theatres, movieShowings);
  }

  async syncEverything(theatres, movieShowings) {
    await this.syncTheatres(theatres);
    await this.syncMovieshowings(movieShowings, theatres[0].apiId);
  }

  async syncTheatres(theatres) {
    const uri = "locations";

    for (let theatre of theatres) {
      let data = {
        name: theatre.name,
      };

      const response = await this.client.getAsync(uri, data);
      const results = response.results;
      if (results.length == 0) {
        // if not found in booking API
        let apiLocation = await this.client.postAsync(uri, data);
        console.log(apiLocation);
        theatre.apiId = apiLocation.id;
      } else {
        // if found in booking API
        theatre.apiId = results[0].id;
      }
    }
  }

  async syncMovieshowings(movieShowings, theatreId) {
    const uri = "events";

    for (let movie of movieShowings) {
      let data = {
        name: movie.name,
        locations: [theatreId],
        start_time: movie.start_time,
        end_time: movie.end_time,
      };

      const response = await this.client.getAsync(uri, data);
      const results = response.results;
      if (results.length == 0) {
        // if not found in booking API
        let apiEvent = await this.client.postAsync(uri, data);
        movie.apiId = apiEvent.id;
      } else {
        // if found in booking API
        movie.apiId = results[0].id;
      }
    }
  }
}
