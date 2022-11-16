
const axios = require('axios');

const data = {

}

// axios post request
axios
.post('http://localhost:3000/api/upload', data)
.then((res) => {
  console.log(res.data),
  console.log(res.status)
})
.catch((err) => { 
  console.log(err) 
});

// axios get request
axios
.get('http://localhost:8000/bookableitems')
.then(res => {
  console.log(`statusCode: ${res.statusCode}`)
  // console.log(res.data)
}) 
.catch(error => {
  console.error(error)
})

