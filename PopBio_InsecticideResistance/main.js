var svg = d3.select('svg');

var svgWidth = +svg.attr('width');
var svgHeight = +svg.attr('height');

var padding = {
	t: 40, 
	r: 10, 
	b: 70, 
	l: 20
};

var chartPadding = {
	t: 0, 
	r: 0, 
	b: 0, 
	l: 40
};

var svgAvailableWidth = svgWidth - padding.l - padding.r;
var svgAvailableHeight = svgHeight - padding.t - padding.b;

var chartWidth = svgAvailableWidth * 0.5;
var chartHeight = svgAvailableHeight;

var chartAvailableWidth = chartWidth - chartPadding.l - chartPadding.t;
var chartAvailableHeight = chartHeight - chartPadding.t - chartPadding.b;

var selectionChart = svg.append('g')
	.attr('class', 'chart')
	.attr('transform', 'translate('+[padding.l, padding.t]+')');

var backgroundChart = svg.append('g')
	.attr('class', 'chart')
	.attr('transform', 'translate('+[padding.l+chartWidth, padding.t]+')');

function getRandomColor() {
	var choices = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
	var c = '#';
	for (var i = 0; i < 6; i++) {
		var index = Math.floor(Math.random() * choices.length);
		c = c + choices[index];
	}
	return c;
}

var toolTip = d3.tip()
	.attr('class', 'd3-tip')
	.offset([0, 0])
	.html(function(d) {
		var bins = d[0];
		for (var i = 0; i < bins.length; i++) {
			var bin = bins[i];
			if (bin.length > 0) {
				var obj = bin[0];
				return obj.insecticide;
			}
		}
		return "Data not found";
	});
	
//toolTip.direction('e');
//svg.call(toolTip);

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
		
		var byLocation = dataset.filter(function(d) {
			return d.locations == "Jamaica"; // hardcoded for our demo
		});
		
		var background = dataset.filter(function(d) {
			return d.measurementType == "mortality rate (percent)" && d.phenotypeValue <= 100.0;
		});
		
		createChart(byLocation, selectionChart, true, true);
		createChart(background, backgroundChart, true, false);		
		
		// Append labels
		var title = svg.append('text')
			.attr('class', 'title')
			.attr('x', svgAvailableWidth * 0.4)
			.attr('y', padding.t * 0.5)
			.text("mortality rate (percent)");
	});
	
function createChart(dataset, group, showAxes, isBackground) {
	
	var insecticides = d3.map(dataset, function(d) {
		return d.insecticide;
	}).keys().sort();
	
	var subsets = [];
		
	insecticides.forEach(function(insecticide) {
		var byInsecticide = dataset.filter(function(d) {
			return d.insecticide == insecticide;
		});
		subsets.push({
			insecticideType: insecticide,
			color: getRandomColor(),
			subset: byInsecticide
		});
	});	
	
	// x-axis = frequency
	// y-axis = mortality rate (percent)	
	
	// create scales
	var xScale = d3.scaleLinear()
		.domain([0, 1]) // 0% to 100% of selected samples
		.range([0, chartAvailableWidth]);
		
	var yExtent = d3.extent(dataset, function(d) {
		return d.phenotypeValue;
	})
		
	var yScale = d3.scaleLinear()
		.domain(yExtent) // min/max mortality rate
		.range([chartAvailableHeight, 0]);
		
	var xAxisX = chartPadding.l;
	var xAxisY = chartHeight - chartPadding.b;
	
	var yAxisX = chartPadding.l;
	var yAxisY = chartPadding.t;
	
	var histogramBins = 10;
	var histogramThresholds = [];
	
	var histMin = yScale.domain()[0];
	var histMax = yScale.domain()[1];
	var histStep = (histMax - histMin) / histogramBins;
	
	for (var thresh = histMin + histStep; thresh <= histMax; thresh = thresh + histStep) {
		histogramThresholds.push(thresh);
	}
	
	var histogram = d3.histogram()
		.value(function(d) {
			return d.phenotypeValue;
		})
		.domain(yScale.domain()) // 0% to 100% of selected samples
		.thresholds(histogramThresholds);
		
	// overlapping area plots for each subset
	for (var i = 0; i < subsets.length; i++) {
		var subset = subsets[i];
		var subsetData = subset['subset'];
		
		var bins = histogram(subsetData);
		
		var subsetPlotG = group.append('g')
			.attr('class', 'subset-plot')
			.attr('transform', 'translate(' + [chartPadding.l, chartPadding.t] + ')');			
		
		var area_ = d3.area()
			.x0(function(d) {
				return 0; // chartPadding.l;
			})
			.x1(function(d) {
				return xScale(d.length / subsetData.length);
			})
			.y(function(d) {
				return yScale(d.x0);
			})
			.curve(d3.curveMonotoneY);
			
		var line_ = d3.line()
			.x(function(d) {
				return xScale(d.length / subsetData.length);
			})
			.y(function(d) {
				return yScale(d.x0);
			})
			.curve(d3.curveMonotoneY);			
		
		var areaPlot = subsetPlotG.append('path')
			.data([bins])
			.attr('class', 'area-plot')
			.attr('fill', subset['color'])
			.attr('stroke', 'none')
			.attr('d', area_)
			.on('mouseover', function(d) {
				var hovered = d3.select(this);
				hovered.attr('class', 'area-plot-hovered');
				//toolTip.show();
			})
			.on('mouseout', function(d) {
				var hovered = d3.select(this);
				hovered.attr('class', 'area-plot');
				//toolTip.hide();
			});
			
		var linePlot = subsetPlotG.append('path')
			.data([bins])
			.attr('class', 'line-plot')
			.attr('fill', 'none')
			.attr('stroke-width', '3')
			.attr('d', line_)
			.on('mouseover', function(d) {
				var hovered = d3.select(this);
				hovered.attr('class', 'line-plot-hovered');
				//toolTip.show();
			})
			.on('mouseout', function(d) {
				var hovered = d3.select(this);
				hovered.attr('class', 'line-plot');
				//toolTip.hide();
			});
			
		areaPlot.data(subsetData);
		linePlot.data(subsetData);	

		if (showAxes) {
			group.append('g')
				.attr('class', 'x axis')
				.attr('transform', 'translate(' + [chartPadding.l, chartPadding.t + chartAvailableHeight] + ')')
				.call(d3.axisBottom(xScale).ticks(5));
				
			group.append('g')
				.attr('class', 'y axis')
				.attr('transform', 'translate('+[chartPadding.l, chartPadding.t]+')')
				.call(d3.axisLeft(yScale));				
		}
		
		// Append labels
		var label = group.append('text')
			.attr('class', 'axis-label')
			.attr('x', chartAvailableWidth * 0.3)
			.attr('y', svgHeight - padding.b)
			.text(function() {
				var txt = "";
				if (isBackground) {
					txt += "Background";
				} else {
					txt += "Selection";
				}
				txt += " (n=" + dataset.length + ")";
				return txt;
			});
		
	}
}
		
	