

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
  let data = response.data;
  for (i = 0; i < data.length; i++) {
    let name = data[i]["result"]["name"];
    let address = data[i]["result"]["adr_address"];
    const tr = document.createElement("tr");
    const nameTd = document.createElement("td");
    const placeName = document.createTextNode(name);
    const addressDiv = document.createElement("div");

    nameTd.appendChild(placeName);
    tr.appendChild(nameTd);
    addressDiv.append(address);
    if(data[i]["result"]["website"]){
        const websiteTd = document.createElement("td");
        const websiteName = document.createTextNode(data[i]["result"]["website"]);
        tr.appendChild(websiteTd)
    }
    if(data[i]["result"]["formatted_phone_number"]){
        const phoneNumberTd = document.createElement("td");
        const phoneNumber = document.createTextNode(data[i]["result"]["formatted_phone_number"]);
        tr.appendChild(phoneNumberTd)
    }
    results.appendChild(tr)
  }
}

form.addEventListener("submit", processForm);
