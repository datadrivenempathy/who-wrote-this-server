var previousSearch;


function makeRequestForPrototypical(callback) {
    $.getJSON("/prototypical.json", callback);
}


function makeRequestForSearch(searchQuery, callback) {
    $.getJSON("/query.json", {"search": searchQuery}, callback);
}


function displayValues(records) {
    var displayArea = d3.select('#display-area');
    displayArea.html("");

    var recordDivs = displayArea.selectAll('.record')
        .data(records["records"])
        .enter()
        .append("div");

    recordDivs.classed("record", true);

    recordDivs.append("div")
        .classed("intro", true)
        .html(function(record) {
            var retText = "The most <span class=\"heavy\">" + record["source"];
            retText += "</span>-like article published by " + record["source"] + " was:";
            return retText;
        });

    var bodyDivs = recordDivs.append("div").classed("body", true);

    bodyDivs.append("a")
        .html(function(record) { return record['title']; })
        .attr("href", function(record) { return record['link']; });

    recordDivs.append("div")
        .classed("note", true)
        .html(function(record) {
            if (record["linkWillSearch"]) {
                return "* Note that a URL was not available for this article so clicking will take you to a DuckDuckGo search.";
            } else {
                return "";
            }
        })
}


function makeRequest() {
    var value = $("#search-box").val();

    if (value === previousSearch) {
        return;
    } else {
        previousSearch = value;
    }

    var onValue = function(newValues) {
        displayValues(newValues);
        $('#loading-indicator').slideUp();
        $('#display-area').slideDown();
    };

    $('#loading-indicator').slideDown();

    $('#display-area').slideUp(function() {
        if (value === "") {
            makeRequestForPrototypical(onValue);
        } else {
            makeRequestForSearch(value, onValue);
        }
    });
}


function setupListeners() {
    var typingTimeout;

    $("#search-box").on("keyup", function () {
      clearTimeout(typingTimeout);
      typingTimeout = setTimeout(makeRequest, 1000);
    });
}


function main() {
    makeRequest();
    setupListeners();
}


main();
