const axios = require("axios");

const domain = "http://localhost:8000";

const config = {
  headers: {
    Authorization: "Token 741149ee55478c463eff3248d9c9a0389c38a82b",
  },
};

function formatUri(uri) {
  uri = uri.toLocaleLowerCase();
  if (uri.charAt(0) != "/") uri = "/" + uri;
  if (uri.charAt(uri.length - 1) != "/") uri += "/";
  return uri;
}

async function post(uri, data) {
  uri = formatUri(uri);
  const res = await axios.post(domain + uri, data, config);
  console.log(res.data);
  return res.data;
}

async function get(uri) {
  uri = formatUri(uri);
  const res = await axios.get(domain + uri, config);
  console.log(res.data);
  return res.data;
}

function getBookableitems(location) {
  let bookableitems = [];
  for (let i = 0; i < 10; i++) {
    bookableitems.push({
      name: `${i} - ${location.name}`,
      location: location.url,
    });
  }
  return bookableitems;
}

async function doStuff() {
  let location = { name: "Sal 1" };
  location = await post("locations", location);

  for (const data of getBookableitems(location)) {
    post("BOOkableITems", data);
  }
}

doStuff();
