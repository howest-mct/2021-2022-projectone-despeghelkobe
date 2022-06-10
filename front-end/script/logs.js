const lanIP = `${window.location.hostname}:5000`;


const initTable = async function(){
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
                                <td>${row.value}</td>
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


document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    initTable();
    // listenToUI();
    // listenToSocket();
  });