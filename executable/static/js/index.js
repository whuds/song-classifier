const log = $("#log");
const file_input = $("#file_input");
const submit = $("#submit");
const warning = $("#warning");
const results = $("#results");


// d3 stuff
const w = 400;
const h = 250;
const margin = {"top": 30, "bottom": 70, "left": 50, "right": 50};

file_input.on("change", function(){
    log.empty();
    var nameSplit = file_input.val().split(".");
    if(nameSplit[nameSplit.length - 1].toLowerCase() == "mp3") {
        warning.prop("hidden", false);
    }
    else {
        warning.prop("hidden", true);
    }
});

// Whenever this form has a submit event,
$("form").submit(function (event) {
    // prevent form from redirecting/making a request and do this instead
    event.preventDefault();

    // Creates FormData object and sticks file in there
    let formData = new FormData();
    let fileData = file_input[0].files[0];
    formData.append("file", fileData);

    // Makes a POST request to the uploader endpoint
    // If successful, tell user file was uploaded successfully and clear #file_input
    // Else, tell user it failed
    $.ajax({
        url: 'uploader',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        beforeSend: function() {
            log.text(fileData.name + " is being processed. Please wait.");
            submit.prop("disabled", true);
            results.empty();
            results.text("None");
            removeBarChart();
        },
        success: function(response){
            console.log(response);
            // x = response;

            // Print the results
            log.text("Processing complete!");


            results.empty();
            // results.append("<b>" + fileData.name + "</b><br/><br/>");
            // response.data.forEach(function(dat, i){
            //     console.log(i);
            //     if(i == 0){
            //         results.append("<b>" + dat.genre +":<b/> " + dat.confidence.toFixed(2).toString() + "%<br/>")
            //     }
            //     else{
            //         results.append(dat.genre + ": " + dat.confidence.toFixed(2).toString() + "%<br/>")
            //     }
            // });



            // Graph the results
            buildBarChart(fileData.name, response.data);


            file_input.val(null);
            submit.prop("disabled", false);

        },
        error: function(){
            log.text("The file upload failed.");
            submit.prop("disabled", false);
        }
    });
});

function removeBarChart() {
        d3.select("#chart").remove();
    }

function buildBarChart(fileName, data) {
    console.log("data in build", data);


    var svg2 = d3.select("#canvas")
        .append("svg")
        .attr("id", "chart")
        .attr("height", h + margin.top + margin.bottom)
        .attr("width", w + margin.left + margin.right);

    svg2.append("text")
        .attr("class", "title")
        .text(fileName)
        .attr("text-anchor", "middle")
        .attr("x", (w/2 + margin.left))
        .attr("y", margin.top/2)
        .attr("font-size", "18px");

    svg2.append("text")
        .attr("class", "x-axis")
        .text("Percent Confidence")
        .attr("text-anchor", "middle")
        .attr("x", (w/2 + margin.left))
        .attr("y", margin.top + margin.bottom/2 + h)
        .attr("font-size", "12px");

    var max = data[0].confidence;

    var xScale = d3.scaleLinear().domain([0, max]).range([0, w]);

    svg2.append("g")
        .attr("class", "x_axis")
        .attr("transform", "translate(" + margin.left + "," + (margin.top + h)+ ")")
        .call(d3.axisBottom(xScale));

    var yScale = d3.scaleBand()
        .domain(data.map(function(d){return d.genre}))
        .range([0, h]);

    svg2.append("g")
        .attr("class", "y_axis")
        .attr("transform", "translate(" + margin.left + "," + margin.top+ ")")
        .call(d3.axisLeft(yScale));

    svg2.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("y", function(d){ return (yScale(d.genre) + margin.top + 2) + "px"})
        .attr("x", (margin.left + 1) + "px")
        .attr("height", (h/data.length - 4) + "px")
        .attr("width", function(d){ return xScale(+d.confidence) + "px"})
        .attr("fill", "blue");
}