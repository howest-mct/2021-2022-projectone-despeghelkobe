const initTable = function(){
    table = document.querySelector(".js-tbody").children;
    i = 0
    console.log(table)
    for(const row of table){
        console.log(row)
        if(i%2 == 0){
            row.style.backgroundColor = "#113377"
        }
        i++
    }
        
}


document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    initTable();
    listenToUI();
    listenToSocket();
  });