var svg = d3.select('svg');

var svgWidth = +svg.attr('width');
var svgHeight = +svg.attr('height');

var padding = {t: 10, r: 30, b: 10, l: 30};

var svgAvailableWidth = svgWidth - padding.l - padding.r;
var svgAvailableHeight = svgHeight - padding.t - padding.b;

var topHistogramPadding = {t: 20, r: 0, b: 20, l: 0};
var bottomHistogramPadding = {t: 20, r: 0, b: 20, l: 0};

var topHistogramProportion = 0.5;
var bottomHistogramProportion = 1 - topHistogramProportion;

var topHistogramWidth = svgAvailableWidth;
var topHistogramHeight = svgAvailableHeight * topHistogramProportion;

var bottomHistogramWidth = svgAvailableWidth;
var bottomHistogramHeight = svgAvailableHeight * bottomHistogramProportion;

var topHistogramAvailableWidth = topHistogramWidth - topHistogramPadding.l - topHistogramPadding.r;
var topHistogramAvailableHeight = topHistogramHeight - topHistogramPadding.t - topHistogramPadding.b;

var bottomHistogramAvailableWidth = bottomHistogramWidth - bottomHistogramPadding.l - bottomHistogramPadding.r;
var bottomHistogramAvailableHeight = bottomHistogramHeight - bottomHistogramPadding.t - bottomHistogramPadding.b;

var topHistogram = svg.append('g')
	.attr('class', 'histogram')
	.attr('transform', 'translate(' + [padding.l, padding.t] + ')');
	
var bottomHistogram = svg.append('g')
	.attr('class', 'histogram')
	.attr('transform', 'translate(' + [padding.l, padding.t+topHistogramHeight] + ')');

var numBins = 20; // number of histogram bins
	

function locationChanged() {
	currentLocation = d3.select('select').property('value');
	updateChart(currentLocation);
}

function measurementChanged() {
	console.log("Measurement changed");
}

d3.csv('insecticide-resistance.csv',
	function(row) {
			
		var sample = {
			sampleId: row['Sample ID'],
			assayId: row['Assay ID'],
			recordType: row['Record type'],
			species: row['Species'],
			sampleType: row['Sample type'],
			label: row['Label'],
			collectionId: row['Collection ID'],
			collectionDateRange: row['Collection date range'],
			collectionProtocols: row['Collection protocols'],
			projects: row['Projects'],
			latitudes: +row['Latitudes'],
			longitudes: +row['Longitudes'],
			locations: row['Locations'],
			phenotypeType: row['Phenotype type'],
			insecticide: row['Insecticide'],
			protocols: row['Protocols'],
			concentration: +row['Concentration'],
			concentrationUnit: row['Concentration unit'],
			duration: +row['Duration'],
			durationUnit: row['Duration unit'],
			phenotypeValue: +row['Phenotype value'],
			phenotypeValueUnit: row['Phenotype value unit'],
			phenotypeValueType: row['Phenotype value type'],
			measurementType: (row['Phenotype value type'] + ' (' + row['Phenotype value unit'] + ')'), // not in original dataset
			citations: row['Citations'],
			tag: row['Tag'],
			attractants: row['Attractants'],
			usageLicense: row['Usage license'],
			sex: row['Sex'],
			developmentalStage: row['Developmental stage']
		};
		return sample;
	},
	function (error, dataset) {
		if (error) {
			console.error('Error while loading insecticide resistance data.');
			console.error(error);
			return;			
		}		
				
		// Set global variables
		samples = dataset;
		
		allLocations = d3.map(dataset, function(d) {
			return d.locations;
		}).keys().sort();
		currentLocation = allLocations[0];
		
		// add select box and callback for location
		var locationSelectBox = d3.select('#locationSelector')
			.attr('style', 'margin-left: 10px;')
			.append('select')
			.on('change', locationChanged);
			
		var locationOptions = locationSelectBox.selectAll('option')
			.data(allLocations)
			.enter()
			.append('option')
			.text(function (d) { 
				return d; 
			});
			
		measurementSelectBox = d3.select('#measurementSelector')
			.append('select')
			.attr('class', 'form-control');
						
		updateChart(currentLocation); 
	});
	
	
function updateChart(loc) {
	
	var byLocation = samples.filter(function(d) {
		return d.locations == loc;
	});
		
	var measurementTypes = d3.map(byLocation, function(d) {
		return d.measurementType;
	}).keys().sort();
	currentMeasurementType = measurementTypes[0];
	
	// Add select box and callback for measurement type
	var counts = new Array(measurementTypes.length);
	for (var i = 0; i < counts.length; i++) {
		counts[i] = 0;
	}
	byLocation.forEach(function(d) {
		var index = measurementTypes.indexOf(d.measurementType);
		counts[index]++;
	});
	
	// Enter, update, exit select options
	var measurementOptions = measurementSelectBox.selectAll('option')
		.data(measurementTypes);
			
	var measurementOptionsEnter = measurementOptions.enter()
		.append('option')
		.text(function(d) {
			var index = measurementTypes.indexOf(d);
			var count = counts[index];
			return d  + ': ' + count + " phenotypes";
		});
		
	// There's a bug where the count isn't updated when the measurement option doesn't change
	measurementOptions.merge(measurementOptionsEnter); 
	
	measurementOptions.exit().remove();
	
	// Now for the actual visualization!
	// Let's suppose mortality rate (percent) is the only possible measurement type for now
	
	// Create histograms from the phenotype values
	// I borrowed heavily from this example: https://bl.ocks.org/d3noob/96b74d0bd6d11427dd797892551a103c
	
	var background = samples.filter(function(d) {
		return d.measurementType == "mortality rate (percent)"; // Hard-code this for now, unfortunately
	});
	
	var byMeasurement = byLocation.filter(function(d) {
		return d.measurementType == "mortality rate (percent)"; // Hard-code this for now, unfortunately
	});
	
	// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "background" histogram on top ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	var xExtentTop = d3.extent(background, function(d) {
		return d.phenotypeValue;
	});
	
	var xScaleTop = d3.scaleLinear()
		.domain(xExtentTop)
		.range([0, topHistogramAvailableWidth]);
		
	var yScaleTop = d3.scaleLinear()
		.range([topHistogramAvailableHeight, 0])
	
	var topHist = d3.histogram()
		.value(function(d) {
			return d.phenotypeValue;
		})
		.domain(xScaleTop.domain())
		.thresholds(xScaleTop.ticks(numBins));
		
	var topBins = topHist(background);
	
	yScaleTop.domain([0, d3.max(topBins, function(d) { return d.length; })]);
	
	// Enter, update, exit
	var topBars = topHistogram.selectAll('rect')
		.data(topBins);
		
	var topBarsEnter = topBars.enter()
		.append('rect')
		.attr("class", "bar")
		.attr("x", 1)
		.attr("transform", function(d) {
		  return "translate(" + xScaleTop(d.x0) + "," + yScaleTop(d.length) + ")"; })
		.attr("width", function(d) { return xScaleTop(d.x1) - xScaleTop(d.x0) - 1 ; })
		.attr("height", function(d) { return topHistogramAvailableHeight - yScaleTop(d.length); });
		
	topBars.merge(topBarsEnter);
	
	topBars.exit().remove();
	
	// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ dynamic histogram on bottom ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	var xExtentBottom = d3.extent(byMeasurement, function(d) {
		return d.phenotypeValue;
	});
	
	var xScaleBottom = d3.scaleLinear()
		.domain(xExtentBottom)
		.range([0, bottomHistogramAvailableWidth]);
		
	var yScaleBottom = d3.scaleLinear()
		.range([bottomHistogramAvailableHeight, 0])
	
	var bottomHist = d3.histogram()
		.value(function(d) {
			return d.phenotypeValue;
		})
		.domain(xScaleBottom.domain())
		.thresholds(xScaleBottom.ticks(numBins));	
		
	var bottomBins = bottomHist(byMeasurement);
	
	yScaleBottom.domain([0, d3.max(bottomBins, function(d) { return d.length; })]);
	
	// Enter, update, exit
	var bottomBars = bottomHistogram.selectAll('rect')
		.data(bottomBins);
		
	var bottomBarsEnter = bottomBars.enter()
		.append('rect')
		.attr("class", "bar")
		.attr("x", 1)
		.attr("transform", function(d) {
		  return "translate(" + xScaleBottom(d.x0) + "," + yScaleBottom(d.length) + ")"; })
		.attr("width", function(d) { return xScaleBottom(d.x1) - xScaleBottom(d.x0) - 1 ; })
		.attr("height", function(d) { return bottomHistogramAvailableHeight - yScaleBottom(d.length); });
		
	bottomBars.merge(bottomBarsEnter);
	
	bottomBars.exit().remove();
}
	

	