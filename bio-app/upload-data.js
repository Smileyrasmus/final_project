
const axios = require('axios');

const config = {
  headers: {
    Authorization: "Token 741149ee55478c463eff3248d9c9a0389c38a82b"
  }
}

const data = {

}

// axios post request
function post1() {
  axios
  .post('http://localhost:3000/api/upload', data)
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

get1()

