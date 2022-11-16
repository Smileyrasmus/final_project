
const axios = require('axios');

const config = {
  headers: {
    Authorization: "Token ca87b84d81f0af7416910d3d605203ca38a8f983"
  }
}

const location = {name: "Sal 1"}

const bookableitems = [
  {
    location: location,
    active: true,
    name: "Kakao?"
  }



]

function postLocation(data) {
  axios
  .post('http://localhost:8000/locations/', data, config)
  .then((res) => {
    console.log(res.data),
    console.log(res.status)
  })
  .catch((err) => { 
    console.log(err) 
  });
}

// axios post request
function postBookableItem(data) {
  axios
  .post('http://localhost:8000/bookableitems/', data, config)
  .then((res) => {
    console.log(res.data),
    console.log(res.status)
  })
  .catch((err) => { 
    console.log(err) 
  });
}

// axios get request
function get1() {
  axios
  .get('http://localhost:8000/bookableitems', config)
  .then(res => {
    console.log(`statusCode: ${res.statusCode}`)
    console.log(res.data)
  }) 
  .catch(error => {
    console.error(error)
  })
}

postLocation(location)

for (const data of bookableitems) {
  postBookableItem(data)
}

get1()

