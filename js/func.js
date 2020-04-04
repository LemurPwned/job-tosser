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

    $('form input').keydown(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            callAjax();
            return false;
        }
    });
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
                                    aria-valuemin="0" aria-valuemax="100">
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