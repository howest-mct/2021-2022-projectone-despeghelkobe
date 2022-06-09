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



// const clearClassList = function (el) {
//   el.classList.remove("c-room--wait");
//   el.classList.remove("c-room--on");
// };

const listenToUI = function () {
  const boost = document.querySelector(".js-boost");
  boost.addEventListener("click", function(){
    socket.send("F2B_boost")
    console.log("boost")
  })

  // for (const knop of knoppen) {
  //   knop.addEventListener("click", function () {
  //     const id = this.dataset.idlamp;
  //     let nieuweStatus;
  //     if (this.dataset.statuslamp == 0) {
  //       nieuweStatus = 1;
  //     } else {
  //       nieuweStatus = 0;
  //     }
  //     //const statusOmgekeerd = !status;
  //     clearClassList(document.querySelector(`.js-room[data-idlamp="${id}"]`));
  //     document.querySelector(`.js-room[data-idlamp="${id}"]`).classList.add("c-room--wait");
  //     socket.emit("F2B_switch_light", { lamp_id: id, new_status: nieuweStatus });
  //   });
  // }
};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_wall_crash", function(){
    console.log("wallcrash")
  })

  // socket.on("B2F_status_lampen", function (jsonObject) {
  //   console.log("alle lampen zijn automatisch uitgezet");
  //   console.log("Dit is de status van de lampen");
  //   console.log(jsonObject);
  //   for (const lamp of jsonObject.lampen) {
  //     const room = document.querySelector(`.js-room[data-idlamp="${lamp.id}"]`);
  //     if (room) {
  //       const knop = room.querySelector(".js-power-btn");
  //       knop.dataset.statuslamp = lamp.status;
  //       clearClassList(room);
  //       if (lamp.status == 1) {
  //         room.classList.add("c-room--on");
  //       }
  //     }
  //   }
  // });

  // socket.on("B2F_verandering_lamp", function (jsonObject) {
  //   console.log("Er is een status van een lamp veranderd");
  //   console.log(jsonObject.lamp.id);
  //   console.log(jsonObject.lamp.status);

  //   const room = document.querySelector(`.js-room[data-idlamp="${jsonObject.lamp.id}"]`);
  //   if (room) {
  //     const knop = room.querySelector(".js-power-btn"); //spreek de room, als start. Zodat je enkel knop krijgt die in de room staat
  //     knop.dataset.statuslamp = jsonObject.lamp.status;

  //     clearClassList(room);
  //     if (jsonObject.lamp.status == 1) {
  //       room.classList.add("c-room--on");
  //     }
  //   }
  // });
  
  // socket.on("B2F_verandering_lamp_from_HRDWR", function (jsonObject) {
  //   console.log(jsonObject)
  // }) 

  socket.on("B2F_send_distance", function (jsonObject){
    console.log(jsonObject.distance)
    const HTML_distance = document.querySelector(".js-distance");
    htmlstring = `${jsonObject.distance.toFixed(2)} cm`
    HTML_distance.innerHTML = htmlstring
  });

};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  initDashboard()
  listenToUI();
  listenToSocket();
});
