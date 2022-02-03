/////////////// handle itinerary creation form //////////////
const results = document.getElementById("results");
const ERRORS = {
  blankName: "Name can't be blank",
  blankStartDate: "Please select start date",
  blankEndDate: "Please select end date",
};
let hotelNames = [];
let restNames = [];

// get place names to make drop down options in itinerary form
function getPlaceNames(placeName) {
  let nameId = {};
  for (let i = 0; i < results.childNodes.length; i++) {
    let name = results.childNodes[i].firstChild.innerText;
    let id = results.childNodes[i].firstChild.id;
    nameId["name"] = name;
    nameId["id"] = id;
  }
  placeName.push(nameId);
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

function validateField(field, errId, fieldName, errMsg, event) {
  if (field === "") {
    event.preventDefault();
    const err = document.getElementById(errId);
    const input = document.getElementsByName(fieldName)[0];
    input.focus();
    err.innerHTML = errMsg;
  }
}

//validate itinerary form
const startDate = document.getElementsByName("start_date")[0];
const endDate = document.getElementsByName("end_date")[0];
const itiForm = document.getElementById("iti-form");

itiForm.addEventListener("submit", function (e) {
  const itiname = document.getElementsByName("iti-name")[0].value;
  const errId1 = "name-error";
  const fieldName1 = "iti-name";
  const blankNameErr = ERRORS["blankName"];
  validateField(itiname, errId1, fieldName1, blankNameErr, e);
  const errId2 = "start-date-error";
  const fieldName2 = "start_date";
  const blankStartDateErr = ERRORS["blankStartDate"];
  validateField(startDate.value, errId2, fieldName2, blankStartDateErr, e);
  const errId3 = "end-date-error";
  const fieldName3 = "end_date";
  const blankEndDateErr = ERRORS["blankEndDate"];
  validateField(endDate.value, errId3, fieldName3, blankEndDateErr, e);
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
const hotelInputDiv = document.querySelector(".hotel_div");
const restInputDiv = document.querySelector(".rest_div");
const addHotelBtn = document.querySelector(".addHotelBtn");
const addRestBtn = document.querySelector(".addRestBtn");
const newHotelSelect = document.createElement("select");
const newRestSelect = document.createElement("select");

results.addEventListener(
  "DOMNodeInserted",
  function () {
    const placeType = document.getElementsByName("type");
    let type;
    for (let i = 0; i < placeType.length; i++) {
      if (placeType[i].checked) {
        type = placeType[i].value;
      }
    }
    if (type === "lodging") {
      addHotelBtn.classList.add("show");
      hotelInputDiv.classList.add("show");
      getPlaceNames(hotelNames);
      createOptions("hotel", hotelInputDiv, hotelNames, newHotelSelect);
    } else if (type === "restaurant") {
      addRestBtn.classList.add("show");
      restInputDiv.classList.add("show");
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

////////////// handle Search box and display results in a table///////////////

let usStates = [
  { name: "ALABAMA", abbreviation: "AL" },
  { name: "ALASKA", abbreviation: "AK" },
  { name: "AMERICAN SAMOA", abbreviation: "AS" },
  { name: "ARIZONA", abbreviation: "AZ" },
  { name: "ARKANSAS", abbreviation: "AR" },
  { name: "CALIFORNIA", abbreviation: "CA" },
  { name: "COLORADO", abbreviation: "CO" },
  { name: "CONNECTICUT", abbreviation: "CT" },
  { name: "DELAWARE", abbreviation: "DE" },
  { name: "DISTRICT OF COLUMBIA", abbreviation: "DC" },
  { name: "FEDERATED STATES OF MICRONESIA", abbreviation: "FM" },
  { name: "FLORIDA", abbreviation: "FL" },
  { name: "GEORGIA", abbreviation: "GA" },
  { name: "GUAM", abbreviation: "GU" },
  { name: "HAWAII", abbreviation: "HI" },
  { name: "IDAHO", abbreviation: "ID" },
  { name: "ILLINOIS", abbreviation: "IL" },
  { name: "INDIANA", abbreviation: "IN" },
  { name: "IOWA", abbreviation: "IA" },
  { name: "KANSAS", abbreviation: "KS" },
  { name: "KENTUCKY", abbreviation: "KY" },
  { name: "LOUISIANA", abbreviation: "LA" },
  { name: "MAINE", abbreviation: "ME" },
  { name: "MARSHALL ISLANDS", abbreviation: "MH" },
  { name: "MARYLAND", abbreviation: "MD" },
  { name: "MASSACHUSETTS", abbreviation: "MA" },
  { name: "MICHIGAN", abbreviation: "MI" },
  { name: "MINNESOTA", abbreviation: "MN" },
  { name: "MISSISSIPPI", abbreviation: "MS" },
  { name: "MISSOURI", abbreviation: "MO" },
  { name: "MONTANA", abbreviation: "MT" },
  { name: "NEBRASKA", abbreviation: "NE" },
  { name: "NEVADA", abbreviation: "NV" },
  { name: "NEW HAMPSHIRE", abbreviation: "NH" },
  { name: "NEW JERSEY", abbreviation: "NJ" },
  { name: "NEW MEXICO", abbreviation: "NM" },
  { name: "NEW YORK", abbreviation: "NY" },
  { name: "NORTH CAROLINA", abbreviation: "NC" },
  { name: "NORTH DAKOTA", abbreviation: "ND" },
  { name: "NORTHERN MARIANA ISLANDS", abbreviation: "MP" },
  { name: "OHIO", abbreviation: "OH" },
  { name: "OKLAHOMA", abbreviation: "OK" },
  { name: "OREGON", abbreviation: "OR" },
  { name: "PALAU", abbreviation: "PW" },
  { name: "PENNSYLVANIA", abbreviation: "PA" },
  { name: "PUERTO RICO", abbreviation: "PR" },
  { name: "RHODE ISLAND", abbreviation: "RI" },
  { name: "SOUTH CAROLINA", abbreviation: "SC" },
  { name: "SOUTH DAKOTA", abbreviation: "SD" },
  { name: "TENNESSEE", abbreviation: "TN" },
  { name: "TEXAS", abbreviation: "TX" },
  { name: "UTAH", abbreviation: "UT" },
  { name: "VERMONT", abbreviation: "VT" },
  { name: "VIRGIN ISLANDS", abbreviation: "VI" },
  { name: "VIRGINIA", abbreviation: "VA" },
  { name: "WASHINGTON", abbreviation: "WA" },
  { name: "WEST VIRGINIA", abbreviation: "WV" },
  { name: "WISCONSIN", abbreviation: "WI" },
  { name: "WYOMING", abbreviation: "WY" },
];

function createStateOptions() {
  const state = document.getElementById("state");
  for (var i = 0; i < usStates.length; i++) {
    var option = document.createElement("option");
    option.text = usStates[i].name;
    option.value = usStates[i].abbreviation;
    state.add(option);
  }
}

createStateOptions();

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
      for (let j = 0; j < 5; j++) {
        if (data[i]["result"]["rating"] < j + 0.5) {
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

const plantripDiv = document.getElementById("planTripImg");

//extract user input from search form and send to BE
async function processForm(evt) {
  evt.preventDefault();
  const loader = document.querySelector(".loader");
  const city = document.getElementById("city");
  const placeType = document.getElementsByName("type");
  const state = document.getElementById("state");
  const planMyTripBtn = document.getElementById("submitItiBtn");
  let type;
  planMyTripBtn.classList.remove("hide");

  for (let i = 0; i < placeType.length; i++) {
    if (placeType[i].checked) {
      type = placeType[i].value;
    }
  }

  results.innerHTML = "";
  if (city.value === "") {
    Swal.fire("Please fill in the city name");
    return;
  }
  loader.classList.remove("hide");
  const typeName = type;
  const cityName = city.value;
  const stateName = state.value;
  let response = await getResultsByLocation(cityName, stateName, typeName);
  let data = response.data;
  handleResults(data);
  plantripDiv.classList.add("hide");
  setTimeout(function () {
    loader.classList.add("hide");
  }, 1000);
}

//clear results on the html page
function clearResults() {
  removeAllChildren(results);
  plantripDiv.classList.remove("hide");
}

function removeAllChildren(parent) {
  while (parent.childNodes[0]) {
    parent.removeChild(parent.childNodes[0]);
  }
}

function removeChildrenNotFirstChild(inputDiv) {
  while (
    inputDiv.firstElementChild &&
    inputDiv.firstElementChild !== inputDiv.lastElementChild
  ) {
    inputDiv.removeChild(inputDiv.lastElementChild);
  }
}

function clearOptionsAndSelect() {
  hotelNames.splice(0, hotelNames.length);
  restNames.splice(0, restNames);
  removeChildrenNotFirstChild(hotelInputDiv);
  removeChildrenNotFirstChild(restInputDiv);
  removeAllChildren(newHotelSelect);
  removeAllChildren(newRestSelect);
}

const searchForm = document.getElementById("search-form");

searchForm.addEventListener("submit", processForm);
searchForm.addEventListener("change", clearResults);
city.addEventListener("change", clearOptionsAndSelect);
