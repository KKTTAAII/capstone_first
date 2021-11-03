////// handle itinerary creation form /////

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

startDate.addEventListener(
  "change",
  function () {
    if (startDate.value) endDate.min = startDate.value;
  },
  false
);

results.addEventListener("DOMNodeInserted", function(){
    let type = document.getElementById("type").value;
    if(type === "lodging"){
        getPlaceNames(hotelNames);
        createOptions("hotel", hotelInputDiv, hotelNames, newHotelSelect);}
    else if(type === "restaurant"){
        getPlaceNames(restNames);
        createOptions("restaurant", restInputDiv, restNames, newRestSelect);
    }
}, false);

addHotelBtn.addEventListener("click", function () {
    const clone = newHotelSelect.cloneNode(true);
    hotelInputDiv.appendChild(clone);
  });
  
addRestBtn.addEventListener("click", function () {
    const clone = newRestSelect.cloneNode(true);
    restInputDiv.appendChild(clone);
  });


function getPlaceNames(placeNames) {
  for (let i = 0; i < results.childNodes.length; i++) {
    let name = results.childNodes[i].lastChild.innerText;
    placeNames.push(name);
  }
}

function createOptions(placeType, inputDiv, names, selectTag) {
  let option = document.createElement("option");
  if (results.childNodes[0]) {
    selectTag.name = placeType;
    selectTag.id = placeType;

    for (const name of names) {
      option.value = name;
      option.text = name;
      selectTag.appendChild(option);
    }
    inputDiv.appendChild(selectTag);
  }
  return;
}
