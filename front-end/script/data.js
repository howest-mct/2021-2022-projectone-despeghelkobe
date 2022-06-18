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

const initChart = async function(){
    const labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
      ];

    const data = {
    labels: labels,
    datasets: [{
        label: 'volt',
        backgroundColor: 'rgb(242,242,0)', //color of dots
        borderColor: 'rgb(242,242,0)', // color of lines
        data: [0, 10, 5, 2, 20, 30, 45],
    },{
        label: 'speed',
        backgroundColor: 'rgb(255,0,0)', //color of dots
        borderColor: 'rgb(255,0,0)', // color of lines
        data: [0, 12, 18, 25 , 20, 10, 5],
    }
    ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {}
    }
    
    const chart = new Chart(document.querySelector('.js-chart'), config)


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
    initChart();
    // listenToUI();
    // listenToSocket();
  });