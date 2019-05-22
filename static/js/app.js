/**
 * Logic for the exemplar search engine.
 *
 * Copyright 2019 Data Driven Empathy LLC
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
 * associated documentation files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge, publish, distribute,
 * sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial
 * portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
 * NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
 * OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

var previousSearch;


/**
 * Execute a request for JSON about overall prototypical articles.
 *
 * @param {function} callback - The function to invoke when data is returned.
 */
function makeRequestForPrototypical(callback) {
    $.getJSON("/prototypical.json", callback);
}


/**
 * Execute a request for JSON about prototypical articles given a user query.
 *
 * @param {string} searchQuery - The user query string.
 * @param {function} callback - The function to invoke when data is returned.
 */
function makeRequestForSearch(searchQuery, callback) {
    $.getJSON("/query.json", {"search": searchQuery}, callback);
}


/**
 * Get the human readable name of a news agency.
 *
 * @param {string} originalName - The name of the agency within the database.
 * @return {string} The "clean" human readable name.
 */
function getCleanSourceName(originalName) {
    if (originalName === "BBC") {
        return "BBC News";
    } else if (originalName == "Fox") {
        return "Fox News";
    } else {
        return originalName;
    }
}


/**
 * Display results returned from the server.
 *
 * @param {arary} records - Array of parsed JSON objects describing the results.
 */
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
            var sourceName = getCleanSourceName(record["source"]);
            var retText = "The most <span class=\"heavy\">" + sourceName;
            retText += "</span>-like article published by " + sourceName + " was:";
            return retText;
        });

    var bodyDivs = recordDivs.append("div").classed("body", true);

    bodyDivs.append("a")
        .html(function(record) { return record['title']; })
        .attr("target", "_blank")
        .attr("href", function(record) { return record['link']; });

    recordDivs.append("div")
        .classed("note", true)
        .html(function(record) {
            if (record["linkWillSearch"]) {
                return "* Note that a URL was not available for this article so clicking will take you to a search on the publisher's website or relevant archive site.";
            } else {
                return "";
            }
        })
}


/**
 * Make a request for articles given the user's input query.
 */
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


/**
 * Setup event listeners for the search box.
 */
function setupListeners() {
    var typingTimeout;

    $("#search-box").on("keyup", function () {
      clearTimeout(typingTimeout);
      typingTimeout = setTimeout(makeRequest, 1000);
    });
}


/**
 * Start this appliction.
 */
function main() {
    makeRequest();
    setupListeners();
}


main();
