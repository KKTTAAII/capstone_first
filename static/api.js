const city = document.getElementById("city");
const placeType = document.getElementById("type");
const state = document.getElementById("state");
const form = document.getElementById("search-form");
const results = document.getElementById("results");

async function getResultsByLocation(city, state, type) {
  const resp = await axios.get("/iti/search", {
    params: { city: city, type: type, state: state },
  });
  return resp;
}

async function processForm(evt) {
  evt.preventDefault();
  const type_name = placeType.value;
  const city_name = city.value;
  const state_name = state.value;
  let response = await axios.get("/iti/search", {
    params: { city: city_name, type: type_name, state: state_name },
  });
  let data = response.data
  for(i=0; i<data.length; i++){
    console.log(data[i]["result"])
  }
  const tr = document.createElement("tr");
  tr.style.backgroundColor = i % 2 === 0 ? "#F0F0F0" : "#FFFFFF";
  
}

form.addEventListener("submit", processForm);
