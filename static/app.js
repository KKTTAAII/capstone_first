////// handle "add more ..." buttons /////

let hotelInput = `<label for="hotel">Hotel</label> 
                <input type="text" name="hotel">`;
let restInput = `<label for="restaurant">Restaurant</label> 
                <input type="text" name="restaurant">`;
                
const hotelInputDiv = document.getElementById("hotel_div");
const restInputDiv = document.getElementById("rest_div");
const addHotelBtn = document.getElementById("addHotelBtn");
const addRestBtn = document.getElementById("addRestBtn");
const start_date = document.getElementsByName("start_date")[0];
const end_date = document.getElementsByName("end_date")[0];

addHotelBtn.addEventListener("click", function () {
  let newHotelInput = hotelInputDiv.insertAdjacentHTML("beforeend", hotelInput);
  let hotelInputs = document.getElementsByName("hotel");
  setId(hotelInputs, "hotel");
});

addRestBtn.addEventListener("click", function () {
  let newRestInput = restInputDiv.insertAdjacentHTML("beforeend", restInput);
  let restInputs = document.getElementsByName("restaurant");
  setId(restInputs, "restaurant");
});

start_date.addEventListener("change", function(){
    if(start_date.value)
        end_date.min = start_date.value;
}, false)

function setId(input, idname) {
  for (let i = 0; i < input.length; i++) {
    input[i].setAttribute("id", idname + i);
  }
}
