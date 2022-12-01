export default class SyncService {
  constructor(client) {
    this.client = client;
  }

  async syncEverything(theatres, movieShowings, seats) {
    await this.syncTheatres(theatres);
    await this.syncMovieShowings(movieShowings, theatres[0].apiId);
    await this.syncSeats(seats, theatres[0].apiId);
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
        theatre.apiId = apiLocation.id;
      } else {
        // if found in booking API
        theatre.apiId = results[0].id;
      }
    }
  }

  async syncMovieShowings(movieShowings, theatreId) {
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

  async syncSeats(seats, theatreApiId) {
    const uri = "bookableitems";

    const apiSeats = await this.client.getAllAsync(uri, {
      params: { location: theatreApiId },
    });

    const objectsToPost = [];
    for (let seat of seats) {
      const apiCopy = apiSeats.find((as) => as.name === seat.name);
      if (!apiCopy) {
        // if not found in booking API
        const data = {
          name: seat.name,
          location: theatreApiId,
        };
        objectsToPost.push(data);
      } else {
        // if found in booking API
        seat.apiId = apiCopy.id;
      }
    }

    const apiResults = await this.client.postAsync(uri, objectsToPost);
    // make sure seats gains apiId after post
    for (let apiSeat of apiResults) {
      const matchingSeat = seats.find((s) => s.name === apiSeat.name);
      matchingSeat.apiId = apiSeat.id;
    }
  }
}
