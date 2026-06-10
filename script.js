// Welcome Message

console.log("AI Crowd Prediction System Loaded");

// Form Validation

function validateForm(){

let passenger =
document.getElementById("passenger_count");

let occupancy =
document.getElementById("occupancy");

if(passenger.value <= 0){

alert("Passenger count must be greater than 0");
return false;

}

if(occupancy.value < 0 || occupancy.value > 100){

alert("Occupancy should be between 0 and 100");
return false;

}

return true;

}