

let colorMap = {
    0: "#a3a3a3",
    20: "#7f94a3",
    40: "#788AA3",
    60: "#e1b794",
    100: "#DB2763"
}
let colorThres = Object.keys(colorMap)

let radialChartRef = null
let barChartRef = null
let salaryChartRef = null
let seniorityChartRef = null


function notFound() {
    row = `<tr>
            <td align="left">No results found</td>
            </tr>`
    $("#spinner").remove();

    if (barChartRef != null) barChartRef.destroy();
    if (salaryChartRef != null) salaryChartRef.destroy();
    if (seniorityChartRef != null) seniorityChartRef.destroy();
    if (radialChartRef != null) radialChartRef.destroy();

    $("#mainTable").fadeIn(1000);

    $('#mainTable tr:last').after(row);
}



function onReady() {
    console.log("ready!");
    $("#pills").hide();
}

function addRow(parsedRow) {
    if (parsedRow['skill'] != undefined) {

        var crafted = craftRow(parsedRow.skill, parsedRow.percentage);
        $("#spinner").remove();

        $("#mainTable").fadeIn(1000);

        $('#mainTable tr:last').after(crafted);
    }
}


function craftModalRow(key, value) {
    let row = `<tr>
        <td align="center" id="skillName">${key}</td>
        <td align="center">${value}</td>
    </tr>`
    return row;
}


function craftRow(skill, value) {
    let color = colorMap[20]
    for (let j = 0; j < colorThres.length; j++) {
        if (colorThres[j] > value) {
            break
        }
        else {
            color = colorMap[colorThres[j]]
        }
    }

    row = `<tr class="clickable-row" onclick='onSkillClick("${skill}")'>
            <td align="left" id="skillName" style="width:60%">${skill}</td>
            <td align="center"  style="width:40%">
                <div class="container">
                    <div class="row">
                        <div class="col-8 mt-1">
                            <div class="progress">
                                <div class="progress-bar" role="progressbar"
                                    style="width: ${value}%; background-color: ${color};" aria-valuenow="${value}"
                                    aria-valuemin="0" aria-valuemax="500">
                                </div>
                            </div>
                        </div>
                        <div class="col-3">
                            ${value}%
                        </div>
                    </div>
                </div>
            </td>
        </tr>`
    return row;
}


var colors = Chart.helpers.color;

var options = {
    title: {
        display: true,
        text: 'What skills are co-occuring?',
        position: 'top'
    },
    rotation: -0.7 * Math.PI,
    resposive: true,
    elements: {
        center: {
            text: '90%',
            color: '#D6C9C9', // Default is #000000
            fontStyle: 'Arial', // Default is Arial
            sidePadding: 20 // Defualt is 20 (as a percentage)
        }
    }
};



function salariesChart(main_skills) {

    if (salaryChartRef != null) {
        salaryChartRef.destroy();
    }
    console.log(main_skills)
    $.ajax({
        url: "/skill_salaries",
        data: {
            skills: main_skills
        },
        success: function (result) {
            console.log(result)
            var min_arr = JSON.parse(result)["min_quantiles"];
            var max_arr = JSON.parse(result)["max_quantiles"];

            for (var i = 0; i < min_arr.length; i++) {
                if (min_arr[i] > max_arr[i]) {
                    var tmp = max_arr[i];
                    max_arr[i] = min_arr[i];
                    min_arr[i] = tmp;
                }
            }

            let labels = ["1st quantile (min, max)",
                "2nd quantile (min, max)", "3rd quantile (min, max)", "4th quantile (min, max)"];
            let backgroundColors = ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9"];

            var config = {
                type: 'horizontalBar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            backgroundColor: backgroundColors,
                            data: min_arr
                        },
                        {
                            backgroundColor: backgroundColors,
                            data: max_arr
                        }
                    ]
                },
                options: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: 'Salaries (annual, in €)'
                    }
                }
            };
            salaryChartRef = new Chart(document.getElementById('salariesCanvas'), config);
        }
    });
}


function seniorityChart(main_skills) {
    if (seniorityChartRef != null) {
        seniorityChartRef.destroy();
    }

    $.ajax({
        url: "/skill_seniority",
        data: {
            skills: main_skills
        },
        success: function (result) {
            seniority = JSON.parse(result);
            console.log(seniority)

            seniorityKeys = Object.keys(seniority);

            let labels = [];
            let counts = [];
            seniorityKeys.forEach((el) => {
                labels.push(el);
                counts.push(seniority[el]);
            });

            let backgroundColors = ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9"];

            var config = {
                type: 'horizontalBar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            backgroundColor: backgroundColors,
                            data: counts
                        },
                    ]
                },
                options: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: 'Experience Levels'
                    }
                }
            };
            seniorityChartRef = new Chart(document.getElementById('seniorityCanvas'), config);
        }
    });
}


function radialChart(datapoints, labelpoints) {
    if (radialChartRef != null) {
        radialChartRef.destroy();
    }

    var config = {
        type: 'radar',
        data: {
            labels: labelpoints,
            datasets: [{
                label: 'Skill layout',
                backgroundColor: colors('#E1B794').alpha(0.2).rgbString(),
                borderColor: '#90A9B7',
                pointBackgroundColor: '#A28497',
                data: datapoints
            }]
        },
        options: {
            legend: {
                position: 'top',
                display: false
            },
            title: {
                display: true,
                text: 'Skill radar chart'
            },
            scale: {
                ticks: {
                    beginAtZero: true
                }
            }
        }
    };
    var rcanvas = document.getElementById("skillChart");
    radialChartRef = new Chart(rcanvas, config);
}


function requestMatchingSkills() {
    if (filled) {
        $("#mainTable").fadeOut(300);
        $("#mainTable").html("<tr></tr>");
        $("#mainTable").fadeIn(1000);

        $("#bat")
    }
    if (barChartRef != null) {
        barChartRef.destroy();
    }

    var all_skills = $("#skillNames").val().replace(/, /g, ",");

    document.getElementById("iframe_courses").src = "http://127.0.0.1:5000/courses?skill=" + all_skills;

    console.log(all_skills);
    filled = true;

    $("#spinner").css("visibility", "visible");
    $.ajax({
        url: "/skill_search",
        data: {
            skills: all_skills
        },
        success: function (result) {
            if (result === "[]") {
                notFound();
            }
            else {

                // generate bar chart here 
                var result_arr = JSON.parse(result);

                let datapoints = []
                let labelpoints = []
                let sumOffers = 0
                result_arr.forEach(element => {
                    // addRow(element);
                    if (element['count'] != undefined) {
                        datapoints.push(element['count'])
                        labelpoints.push(element['skill'])
                        sumOffers += element['count']
                    }
                });

                req = labelpoints.join(',')
                console.log(req);
                salariesChart(all_skills);
                seniorityChart(all_skills);

                data = {
                    datasets: [{
                        data: datapoints,
                        backgroundColor: ['#E1B794', '#7F94A3', '#E3E3E3', '#DB2763',
                            '#7392B7', '#C6CAED', '#A28497', '#73683B', '#583E23',
                            '#E8EEF2', '#D6C9C9', '#90A9B7', '#8D5A97'],
                    }],
                    labels: labelpoints
                }

                setTimeout(function () {
                    // getSkillNumbers(result_arr);
                    radialChart(datapoints, labelpoints)

                    options.elements.center.text = sumOffers
                    var canvas = document.getElementById("barChart");


                    var ctx = canvas.getContext('2d');
                    barChartRef = new Chart(ctx, {
                        type: 'doughnut',
                        data: data,
                        options: options
                    });
                    barChartRef.show();
                }, 1000);

                setTimeout(function () {
                    result_arr.forEach(element => {
                        addRow(element);
                    });
                    $("#pills").show();
                }, 1000);
            }
        }
    });
};


function addModalRow(parsedRow) {
    var crafted = craftModalRow(parsedRow.name, parsedRow.result);
    console.log(crafted);

    $("#modalSpinner").remove();

    $("#modalTable").fadeIn(1000);
    console.log($('#modalTable tr:last'));

    $('#modalTable tr:last').after(crafted);
}

function onSkillClick(skill) {
    console.log(skill);
    window.location.replace("/courses?skill=" + skill);
}

function fillModal(skill) {
    $("#exampleModalCenter").find('#exampleModalCenterTitle').html(skill);
    $("#modalTable").html("<tbody><tr id='toDelete'></tr></tbody>");

    $.ajax({
        url: "http://0.0.0.0:5000/stats",
        data: {
            text: $('#positionName').val(),
            limit: 20
        },
        success: function (result) {
            var result_arr = JSON.parse(result);
            result_arr.forEach(element => {
                addModalRow(element);
            });
        }
    });
}