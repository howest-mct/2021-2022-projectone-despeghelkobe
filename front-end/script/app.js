const lanIP = `${window.location.hostname}:5000`;
const socket = io.connect(`http://${lanIP}`);
let starting_degree = -15

digit_count = 7



const initDashboard = function(){
  // show labels on correct position on the site
  const speedometer = document.querySelector(".js-speedometer")

  for (let index = 0; index <= digit_count; index++) {
    speedometer.innerHTML += `<div class="c-didgit js-didgit">
      <div class="c-didgit__line"></div>
      <div class="c-didgit__label js-label"></div>
      </div>`
  }


  const didgits = document.querySelectorAll(".js-didgit")
  const labels = document.querySelectorAll(".js-label")
  const pointer = document.querySelector(".js-pointer")
  didgit_count = didgits.length
  console.log(didgits)

  splits = (180 + (-starting_degree*2)) / (didgit_count-1)
  i=0
  for(const didgit of didgits){
    degrees = (splits*i)+ starting_degree
    speed = 2*i
    didgit.style.transform = `rotate(${degrees}deg)`
    i++
  }

  i=0
  //show lines on correct position on the site
  for(const label of labels){
    speed = 2*i
    degrees = (splits*i)+ starting_degree
    label.innerHTML = speed
    label.style.transform = `rotate(${-degrees}deg)`
    i++
  }

  //show pointer on starting angle on the site 
  pointer.style.transform = `rotate(${starting_degree}deg)`
}



async function getData(endpoint){
  let response = await fetch(`http://${lanIP}/${endpoint}`)
  let data = await response.json()
  // console.log(data)
  return data
}

const sendParameters = function() {
  inputField = document.querySelector(".js-stop_distance")
  socket.emit('F2B_send_stopping_distance', {value: inputField.value})
}


const listenToUI = function () {
  const boost = document.querySelector(".js-stop");
  boost.addEventListener("click", function(){
    if(boost.innerHTML == "stop engine"){
      socket.emit("F2B_emergency_stop")
      boost.innerHTML = "start engine"
    }else if(boost.innerHTML == "start engine"){
      socket.emit("F2B_start_motor")
      boost.innerHTML = "stop engine"
    }
  })


  power_off = document.querySelector(".js-power-off")
  power_off.addEventListener("click", function(){
    console.log("dave")
    socket.emit("F2B_power_off")
  })
};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_send_ultrasonic", function(jsonObject){
    distance = jsonObject.distance
    icon = document.querySelectorAll('.js-car_crash path')
    if(distance < 20){
      for(const path of icon){
        path.style.fill = "red"
      }
    }else{
      for(const path of icon){
        path.style.fill = "white"
      }
    }
    
  })

  socket.on("B2F_send_voltage", function(jsonObject){
    voltage = jsonObject.voltage
    icon = document.querySelector(".js-low_fuel path")
    if(voltage < 4){
     icon.style.fill = "red"
    }else{
      icon.style.fill = "white"
    }
  })

  socket.on("B2F_send_tilt", function(jsonObject){
    degrees = jsonObject.degrees
    icon = document.querySelectorAll(".js-upside_down path")
    if(degrees > 90 && degrees < -90){
      for (const path in icon){
        path.style.fill = "red"
      }
    }else{
      for (const path in icon){
        path.style.fill = "white"
      }
    }
  })
  
  socket.on("B2F_send_speed", function(jsonObject){
    speed = jsonObject.speed
    pointer = document.querySelector(".js-pointer")
    // console.log(speed / digit_count*2)
    // console.log(180 + (-2*starting_degree))
    angle = (speed / (digit_count*2))*(180 - (2*starting_degree))
    pointer.style.transform = `rotate(${angle+starting_degree}deg)`
  })


};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  initDashboard();
  listenToUI();
  listenToSocket();
});
