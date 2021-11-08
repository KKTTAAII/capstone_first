/////////////// handle itinerary creation form //////////////

const hotelInputDiv = document.getElementById("hotel_div");
const restInputDiv = document.getElementById("rest_div");
const addHotelBtn = document.getElementById("addHotelBtn");
const addRestBtn = document.getElementById("addRestBtn");
const startDate = document.getElementsByName("start_date")[0];
const endDate = document.getElementsByName("end_date")[0];
const results = document.getElementById("results");
const newHotelSelect = document.createElement("select");
const newRestSelect = document.createElement("select");
const hotelNames = [];
const restNames = [];
const city = document.getElementById("city");
const placeType = document.getElementById("type");
const state = document.getElementById("state");
const searchForm = document.getElementById("search-form");
const itiForm = document.getElementById("iti-form");

//validate itinerary name - cannot be blank
itiForm.addEventListener("submit", function (e) {
  const itiname = document.getElementsByName("iti-name")[0].value;
  if (itiname === "") {
    e.preventDefault();
    const err = document.getElementById("name-error");
    const nameInput = document.getElementsByName("iti-name")[0];
    nameInput.focus();
    err.innerHTML = "Name can't be blank";
  }
  if (startDate.value === "") {
    e.preventDefault();
    const err = document.getElementById("start-date-error");
    const startDateInput = document.getElementsByName("start_date")[0];
    startDateInput.focus();
    err.innerHTML = "Please select start date";
  }
  if (endDate.value === "") {
    e.preventDefault();
    const err = document.getElementById("end-date-error");
    const endtDateInput = document.getElementsByName("end_date")[0];
    endtDateInput.focus();
    err.innerHTML = "Please select end date";
  }
});

// Ensure that the start date is not before the current date
let today = new Date().toISOString().split("T")[0];
startDate.setAttribute("min", today);

// Ensure that the end date is not before the start date
startDate.addEventListener(
  "change",
  function () {
    if (startDate.value) endDate.min = startDate.value;
  },
  false
);

// show options to add hotels and restaurants to the itinerary form when there are results only
results.addEventListener(
  "DOMNodeInserted",
  function () {
    let type = document.getElementById("type").value;
    if (type === "lodging") {
      addHotelBtn.style.display = "block";
      hotelInputDiv.style.display = "block";
      getPlaceNames(hotelNames);
      createOptions("hotel", hotelInputDiv, hotelNames, newHotelSelect);
    } else if (type === "restaurant") {
      addRestBtn.style.display = "block";
      restInputDiv.style.display = "block";
      getPlaceNames(restNames);
      createOptions("restaurant", restInputDiv, restNames, newRestSelect);
    }
  },
  false
);

// allows user to add multiple hotels
addHotelBtn.addEventListener("click", function () {
  const clone = newHotelSelect.cloneNode(true);
  hotelInputDiv.appendChild(clone);
});

// allows user to add multiple restaurants
addRestBtn.addEventListener("click", function () {
  const clone = newRestSelect.cloneNode(true);
  restInputDiv.appendChild(clone);
});

// get place names to make drop down options in itinerary form
function getPlaceNames(placeName) {
  for (let i = 0; i < results.childNodes.length; i++) {
    let nameId = {};
    let name = results.childNodes[i].firstChild.innerText;
    let id = results.childNodes[i].firstChild.id;
    nameId["name"] = name;
    nameId["id"] = id;
    placeName.push(nameId);
  }
}

//create drop down options from the results (names of places)
function createOptions(placeType, inputDiv, names, selectTag) {
  let option = document.createElement("option");
  if (results.childNodes[0]) {
    selectTag.name = placeType;
    selectTag.id = placeType;
    selectTag.className = "form-select mb-2";

    for (let i = 0; i < names.length; i++) {
      option.value = [names[i]["name"], names[i]["id"]];
      option.text = names[i]["name"];
      selectTag.appendChild(option);
    }
    inputDiv.appendChild(selectTag);
  }
  return;
}

////////////// handle Search box and display results in a table///////////////

// make a request to BE to get results based on user inputs
async function getResultsByLocation(city, state, type) {
  const resp = await axios.get("/iti/search", {
    params: { city: city, type: type, state: state },
  });
  return resp;
}

// add results to the html page
function handleResults(data) {
  if (!Array.isArray(data)) {
    errorMsg = data["result"];
    Swal.fire(errorMsg);
  }
  for (i = 0; i < data.length; i++) {
    let name = data[i]["result"]["name"];
    let address = data[i]["result"]["formatted_address"];
    let placeId = data[i]["place_id"];
    const tr = document.createElement("tr");
    const nameTd = document.createElement("td");
    nameTd.id = placeId;
    const placeName = document.createTextNode(name);
    const infoDiv = document.createElement("div");
    infoDiv.className = "place-info";
    const addressDetail = document.createElement("p");
    const placeAddress = document.createTextNode(address);

    nameTd.appendChild(placeName);
    tr.appendChild(nameTd);
    infoDiv.append(addressDetail);
    tr.appendChild(infoDiv);
    addressDetail.appendChild(placeAddress);
    if (data[i]["result"]["website"]) {
      const pWebsite = document.createElement("p");
      const website = document.createElement("a");
      website.href = data[i]["result"]["website"];
      const websiteName = document.createTextNode(data[i]["result"]["website"]);
      website.appendChild(websiteName);
      pWebsite.appendChild(website);
      infoDiv.append(pWebsite);
    }
    if (data[i]["result"]["formatted_phone_number"]) {
      const phoneNumber = document.createElement("p");
      const number = document.createTextNode(
        data[i]["result"]["formatted_phone_number"]
      );
      phoneNumber.appendChild(number);
      infoDiv.append(phoneNumber);
    }
    if (data[i]["result"]["rating"]) {
      const rating = document.createElement("span");
      for (let i = 0; i < 5; i++) {
        if (data[i]["result"]["rating"] < i + 0.5) {
          rating.innerHTML += "&#10025;";
        } else {
          rating.innerHTML += "&#10029;";
        }
        infoDiv.append(rating);
      }
    }
    results.appendChild(tr);
  }
}

//extract user input from search form and send to BE
async function processForm(evt) {
  evt.preventDefault();
  const type_name = placeType.value;
  const city_name = city.value;
  const state_name = state.value;
  let response = await getResultsByLocation(city_name, state_name, type_name);
  let data = response.data;
  handleResults(data);
}

//clear results on the html page
function clearResults() {
  while (results.childNodes[0]) {
    results.removeChild(results.childNodes[0]);
  }
}

searchForm.addEventListener("submit", processForm);
searchForm.addEventListener("change", clearResults);