(function () {
    let ctx = document.getElementById('myChart');
    fetch(ctx.dataset.apiUrl)
    .then(response => response.json())
    .then(data => {
        const months = data.map(item => `Month: ${item.month} Year: ${item.year}`);
        const pages = data.map(item => item.pages_read);
        let newCtx = ctx.getContext('2d');
        const myData = {
            labels: months,
            datasets: [{
              label: 'Reading statistic',
              data: pages,
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
              ],
              borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
              ],
              borderWidth: 1
            }]
          };
        let myChart = new Chart(newCtx, {
            type: 'bar',
            data: myData,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
}) ();
