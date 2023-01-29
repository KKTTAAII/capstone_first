///////////////////////////////////////////////////// handle itinerary creation form //////////////////////////////////////
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

////////////////////////////////////////////// handle Search box and display results in a table/////////////////////////////////

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

///////////////////////////////////////////////////////////handle pagination////////////////////////////////////
//creating page list
const paginationNumbersContainer =
  document.getElementById("pagination-numbers");
const paginatedList = document.getElementById("results");
const listItems = paginatedList.querySelectorAll("tr");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");

let pageCount;
let paginationLimit = 10;
let currentPage;

function appendPageNumber(index) {
  const pageNumber = document.createElement("button");
  pageNumber.className = "pagination-number";
  pageNumber.id = index;
  pageNumber.innerHTML = index;
  pageNumber.setAttribute("page-index", index);
  pageNumber.setAttribute("aria-label", "Page " + index);
  paginationNumbersContainer.appendChild(pageNumber);
}

function getPaginationNumbers() {
  for (let i = 1; i <= pageCount; i++) {
    appendPageNumber(i);
  }
}

function handleActivePageNumber() {
  document.querySelectorAll(".pagination-number").forEach(button => {
    button.classList.remove("active");

    const pageIndex = Number(button.getAttribute("page-index"));
    if (pageIndex == currentPage) {
      button.classList.add("active");
      button.classList.add("btn-primary");
    }
  });
}

function setCurrentPage(pageNum, listItems) {
  currentPage = pageNum;

  handleActivePageNumber();

  const prevRange = (pageNum - 1) * paginationLimit;
  const currRange = pageNum * paginationLimit;
  //ensure that only the items on the current page show, the other will display none
  listItems.forEach((item, index) => {
    item.classList.add("hidden");
    if (index >= prevRange && index < currRange) {
      item.classList.remove("hidden");
    }
  });
}

function createPageNumbers(data, HTMLArray) {
  pageCount = Math.ceil(data.length / paginationLimit);
  getPaginationNumbers();
  setCurrentPage(1, HTMLArray);

  //the pagination buttons
  document.querySelectorAll(".pagination-number").forEach(button => {
    const pageIndex = Number(button.getAttribute("page-index"));
    if (pageIndex) {
      button.addEventListener("click", () => {
        setCurrentPage(pageIndex, HTMLArray);
      });
    }
  });
}

///////////////////////////////////////////////// add results to the html page//////////////////////////////////
function handleResults(data) {
  if (!Array.isArray(data)) {
    errorMsg = data["result"];
    Swal.fire(errorMsg);
  }

  //used for createPageNumbers function
  const HTMLelementArray = [];

  for (i = 0; i < data.length; i++) {
    let name = data[i]["result"]["name"];
    let address = data[i]["result"]["formatted_address"];
    let placeId = data[i]["place_id"];
    const tr = document.createElement("tr");
    tr.className = "result";
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
    HTMLelementArray.push(tr);
    results.appendChild(tr);
  }

  //used this for pageination
  return HTMLelementArray;
}

//////////////////////////////////////////get lat and lng for GG map markers///////////////////////////////////
function getLocations(data) {
  return data.map(place => {
    return { name: place.result.name, location: place.location };
  });
}


/////////////////////////////////////////////////////////////////////process form/////////////////////////////////
const plantripDiv = document.getElementById("planTripImg");
let data, locations;

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
  const response = await getResultsByLocation(cityName, stateName, typeName);
  data = response.data;
  locations = getLocations(data);
  initMap();
  const HTMLArray = handleResults(data);
  createPageNumbers(data, HTMLArray);
  plantripDiv.classList.add("hide");
  setTimeout(function () {
    loader.classList.add("hide");
  }, 1000);
}

/////////////////////////////////////////clear results on the html page///////////////////////////////////////
function clearResults() {
  removeAllChildren(results);
  removeAllChildren(paginationNumbersContainer);
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

//////////////////////////////////////////////////////////google map/////////////////////////////////////
let map;
//generate a map
function initMap() {
  const USA = { lat: 39.80976, lng: -98.74831 };
  if (locations && locations.length > 0) {
    map = new google.maps.Map(document.getElementById("map"), {
      center: locations[0].location,
      zoom: 15,
    });
    createMarkers(locations);
  } else {
    map = new google.maps.Map(document.getElementById("map"), {
      center: USA,
      zoom: 5,
    });
  }
}

//generate map markers
function createMarkers(locations) {
  let infowindow = new google.maps.InfoWindow();
  let marker, count;
  for (count = 0; count < locations.length; count++) {
    marker = new google.maps.Marker({
      position: locations[count].location,
      map: map,
      title: locations[count].name,
    });

    google.maps.event.addListener(
      marker,
      "click",
      (function (marker) {
        return function () {
          let content = marker.getTitle();
          infowindow.setContent(
            '<div class="infowindow">' + content + "</div>"
          );
          infowindow.open(map, marker);
        };
      })(marker)
    );
  }
}

//////////////////////////////////////////////////search form eventListeners//////////////////////////////////////////

const searchForm = document.getElementById("search-form");

searchForm.addEventListener("submit", processForm);
searchForm.addEventListener("change", clearResults);
city.addEventListener("change", clearOptionsAndSelect);
