    const lanIP = `${window.location.hostname}:5000`;


const initTable = async function(){
    table = document.querySelector(".js-tbody");

    data = await getData("logs")
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
    voltages = await getData("volt")
    speed = await getData("speed")
    const labels = []
    const data_speed = []
    for (let index = 0; index < speed.length; index++) {
        const row = speed[index];
        label = new Date(row.datetime).toLocaleTimeString()
        labels.push(label)
        data_speed.push(row.value)
    }

    for (let index = 0; index < voltages.length; index++) {
        const row = voltages[index];
        data_speed.push(row.value)
    }
    
    // const labels = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul']
    const data = {
    labels: labels,
    datasets: [{
        label: 'volt',
        backgroundColor: 'rgb(242,242,0)', //color of dots
        borderColor: 'rgb(242,242,0)', // color of lines
        data: Object.values(voltages),
        yAxisID: 'volt'
    },{
        label: 'speed',
        backgroundColor: 'rgb(255,0,0)', //color of dots
        borderColor: 'rgb(255,0,0)', // color of lines
        data: data_speed,
        yAxisID: 'speed'
    }
    ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            scales: {
                volt: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'speed',
                        color: "white"
                    },
                    ticks: {
                        color: 'white'
                    }
                },
                speed: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'voltage',
                        color: 'white'
                    },
                    ticks: {
                        color: 'white'
                    }
                    
                },
                x: {
                    ticks: {
                        color: 'white'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            }
        }
    }
    
    const chart = new Chart(document.querySelector('.js-chart'), config)


}





async function getData(endpoint){
    let response = await fetch(`http://${lanIP}/${endpoint}`)
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