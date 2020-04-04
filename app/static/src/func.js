function notFound() {
    row = `<tr>
            <td align="left">No results found</td>
            </tr>`
    $("#barChart").remove();
    $("#spinner").remove();

    $("#mainTable").fadeIn(1000);

    $('#mainTable tr:last').after(row);
}



function onReady() {
    console.log("ready!");

    // $('form input').keydown(function (e) {
    //     if (e.keyCode == 13) {
    //         e.preventDefault();
    //         callAjax();
    //         return false;
    //     }
    // });
}


let colorMap = {
    0: "#a3a3a3",
    20: "#7f94a3",
    40: "#788AA3",
    60: "#e1b794",
    100: "#DB2763"
}
let colorThres = Object.keys(colorMap)

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

function salariesChart() {
    var main_skills = $("#skillNames").val().replace(/, /g, ",");

    $.ajax({
        url: "/skill_salaries",
        data: {
            skills: main_skills
        },
        success: function (result) {
            var min_arr = JSON.parse(result)["min_quantiles"];
            var max_arr = JSON.parse(result)["max_quantiles"];

            for (var i = 0; i < min_arr.length; i++) {
                if (min_arr[i] > max_arr[i]) {
                    var tmp = max_arr[i];
                    max_arr[i] = min_arr[i];
                    min_arr[i] = tmp;
                }
            }

            let labels = ["1st quantile", "2nd quantile", "3rd quantile", "4th quantile"];
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
                        text: 'Salaries'
                    }
                }
            };
            var barchart = new Chart(document.getElementById('salariesCanvas'), config);
        }
    });
}

function seniorityChart() {
    var main_skills = $("#skillNames").val().replace(/, /g, ",");

    $.ajax({
        url: "/skill_seniority",
        data: {
            skills: main_skills
        },
        success: function (result) {
            var min_arr = JSON.parse(result)["min_quantiles"];
            var max_arr = JSON.parse(result)["max_quantiles"];

            for (var i = 0; i < min_arr.length; i++) {
                if (min_arr[i] > max_arr[i]) {
                    var tmp = max_arr[i];
                    max_arr[i] = min_arr[i];
                    min_arr[i] = tmp;
                }
            }

            let labels = ["1st quantile", "2nd quantile", "3rd quantile", "4th quantile"];
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
                        text: 'Salaries'
                    }
                }
            };
            var barchart = new Chart(document.getElementById('salariesCanvas'), config);
        }
    });
}
