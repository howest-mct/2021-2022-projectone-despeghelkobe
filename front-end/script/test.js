const init_dashboard = function(){
  const didgits = document.querySelectorAll(".js-didgit")
  const labels = document.querySelectorAll(".js-label")
  const pointer = document.querySelector(".js-pointer")
  didgit_count = didgits.length
  i=0
  starting_degree = -15
  splits = (180 + (-starting_degree*2)) / (didgit_count-1)
  console.log(-starting_degree*2)
  
  
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

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  init_dashboard()

});