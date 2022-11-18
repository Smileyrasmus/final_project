import theatres from "../database/theatres.json";
import movieShowings from "../database/movieshowing.json";
import seats from "../database/seats.json";
import BookingClient from "./BookingClient";

async function syncLocations(client) {
  let theatreApiIds = [];

  for (let theatre of theatres) {
    let response = await client.getAsync("locations", {
      name: theatre.name,
    });
    let results = response.results;
    if (results.length == 0) {
      let data = { name: theatre.name };
      let apiLocation = client.postAsync("locations", data);
      theatreApiIds.push(apiLocation.id);
    }
  }

  return theatreApiIds;
}

export default async function sync() {
  const config = {
    headers: {
      //Authorization: "Token 741149ee55478c463eff3248d9c9a0389c38a82b", /*REBL*/
      Authorization: "Token ca87b84d81f0af7416910d3d605203ca38a8f983", /*MBJ*/
    },
  };

  const client = new BookingClient("http://localhost:8000", config);

  let theatreApiIds = await syncLocations(client);
}
