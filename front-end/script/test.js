const init_dashboard = function(){
  init_didgits()
  
}

const init_didgits = function(){
  const didgits = document.querySelectorAll(".js-didgit")
  const labels = document.querySelectorAll(".js-label")
  didgit_count = didgits.length
  i=0
  splits = 180/(didgit_count-1)

  for(const didgit of didgits){
    degrees = splits*i
    speed = 20*i
    didgit.style.transform = `rotate(${degrees}deg)`
    i++
  }

  i=0
  for(const label of labels){
    speed = 20*i
    degrees = splits*i
    label.innerHTML = speed
    label.style.transform = `rotate(${-degrees}deg)`
    i++
  }
}


document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  init_dashboard()

});