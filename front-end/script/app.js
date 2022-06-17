const lanIP = `${window.location.hostname}:5000`;
const socket = io.connect(`http://${lanIP}`);

const initDashboard = function(){
  const didgits = document.querySelectorAll(".js-didgit")
  const labels = document.querySelectorAll(".js-label")
  const pointer = document.querySelector(".js-pointer")
  didgit_count = didgits.length
  i=0
  starting_degree = -15
  splits = (180 + (-starting_degree*2)) / (didgit_count-1)
  
  
  // show labels on correct position on the site
  for(const didgit of didgits){
    degrees = (splits*i)+ starting_degree
    speed = 20*i
    didgit.style.transform = `rotate(${degrees}deg)`
    i++
  }

  i=0
  //show lines on correct position on the site
  for(const label of labels){
    speed = 20*i
    degrees = (splits*i)+ starting_degree
    label.innerHTML = speed
    label.style.transform = `rotate(${-degrees}deg)`
    i++
  }

  //show pointer on starting angle on the site 
  pointer.style.transform = `rotate(${starting_degree}deg)`
}

const initTable = async function(){
  //check if needed to display
  logs = document.querySelector(".js-logs")
  if (window.innerWidth < 1024) {
    logs.style.display = "none"
  }else{
    logs.style.display = "block"
  }

  //make table
  table = document.querySelector(".js-tbody");

  data = await getLogsData()
  i = 0
  for(const row of data){
      let color = ""
      if(i%2 == 0){
          color = "#113377"
      }
      table.innerHTML += `<tr style="background-color: ${color}">
                              <td>${new Date(row.datetime).toLocaleString()}</td>
                              <td>${row.name}</td>
                              <td>${row.action_description}</td>
                              <td>${((row.value == null) ? row.value : row.value.toFixed(2))}</td>
                              <td>${row.comment}</td>
                          </tr>`
      i++
  }
}

async function getLogsData(){
  let response = await fetch(`http://${lanIP}/logs`)
  let data = await response.json()
  // console.log(data)
  return data
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
    // socket.emit("F2B_power_off")
  })

  window.onresize = function(){
    logs = document.querySelector(".js-logs")
    width = window.innerWidth
    if(width < 1024){
      logs.style.display = "none"
    }else{
      logs.style.display = "block"
    }
  }
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
 
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  initDashboard();
  initTable();
  listenToUI();
  listenToSocket();
});
