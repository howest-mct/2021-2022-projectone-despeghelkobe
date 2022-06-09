const lanIP = `${window.location.hostname}:5000`;


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

async function getLogsData(){
    let response = await fetch(`https://${lanIP}/logs`)
    let data = await response.json()
    return data
}


document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    initTable();
    data = getLogsData()
    console.log(data)
    // listenToUI();
    // listenToSocket();
  });