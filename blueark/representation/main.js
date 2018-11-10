var powerctx = document.getElementById("power").getContext('2d');
var consumersctx = document.getElementById("consumers").getContext('2d');
var pipesctx = document.getElementById("pipes").getContext('2d');
var tanksctx = document.getElementById("tanks").getContext('2d');
var bordercolors = [
    'rgba(255,99,132,1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)'
];

var backgroundcolors = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'
];

var num_lines = 2;
var num_values = 10;
var legends = ['Power generated', 'Water Consumed']

var power_data = {
    labels: [],
    datasets: []
};

var consumers_data = {
    labels: [],
    datasets: []
};

var tanks_data = {
    labels: [],
    datasets: []
};

var pipes_data = {
    labels: [], // labels on the x-axis
    datasets: []
};

var options = {
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }]
    }
};

var powerchart = new Chart(powerctx, {
    type: 'line',
    data: power_data,
    options: options
});

var pipeschart = new Chart(pipesctx, {
    type: 'line',
    data: pipes_data,
    options: options
});

var consumerschart = new Chart(consumersctx, {
    type: 'line',
    data: consumers_data,
    options: options
});

var tankschart = new Chart(tanksctx, {
    type: 'line',
    data: tanks_data,
    options: options
});


function add_data_point(chart, i, labels, matrix) {
    if (i >= matrix.length) { return; }

    chart.data.labels.push("Day " + (i + 1)); // x axis => data points
    var cols = matrix[0].length;
    var m = chart.data.datasets.length;

    while (m < cols) {
        chart.data.datasets.push({});
        chart.data.datasets[m].backgroundColor = backgroundcolors[m % 6];
        chart.data.datasets[m].borderColor = bordercolors[m % 6];
        chart.data.datasets[m].label = labels[m];
        chart.data.datasets[m].data = [];
        chart.data.datasets[m].borderWidth = 1;
        m++;
    }

    for (var j = 0; j < cols; j++) {
        chart.data.datasets[j].data.push(matrix[i][j]);
    }
    chart.update();
    setTimeout(add_data_point, 500, chart, i + 1, labels, matrix);
}
function get_data(path, chart) {

    var matrix;
    var labels;

    fetch(path)
        .then(response => response.text())
        .then(text => {
            matrix =
                text.split('\n')
                    .filter((_, i) => i > 0)
                    .map(l => l.split(','));

            labels = text.split('\n')[0].split(',');
        })
        .then(m => add_data_point(chart, 0, labels, matrix));
}

get_data('./data/fake_power.txt', powerchart);
get_data('./data/fake_pipes.txt', pipeschart);
get_data('./data/fake_tanks.txt', tankschart);
get_data('./data/fake_consumers.txt', consumerschart);
