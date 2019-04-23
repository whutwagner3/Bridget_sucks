var svg = d3.select('svg');

var svgWidth = +svg.attr('width');
var svgHeight = +svg.attr('height');

var padding = {t: 0, r: 0, b: 0, l: 0};

var svgAvailableWidth = svgWidth - padding.l - padding.r;
var svgAvailableHeight = svgHeight - padding.t - padding.b;

var chartWidth = svgAvailableWidth * 0.8;
var chartHeight = svgAvailableHeight * 0.8;

function getRandomColor() {
	var choices = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
	var c = '#';
	for (var i = 0; i < 6; i++) {
		var index = Math.floor(Math.random() * choices.length);
		c = c + choices[index];
	}
	return c;
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
					
		// We might not need to use this for now
		var background = dataset.filter(function(d) {
			return d.measurementType == "mortality rate (percent)" && d.phenotypeValue <= 100.0;
		});
		
		var byLocation = dataset.filter(function(d) {
			return d.locations == "Jamaica"; // hardcoded for our demo
		});
		
		var insecticides = d3.map(byLocation, function(d) {
			return d.insecticide;
		}).keys().sort();
		
		var subsets = [];
		
		insecticides.forEach(function(insecticide) {
			var byInsecticide = byLocation.filter(function(d) {
				return d.insecticide == insecticide;
			});
			subsets.push({
				insecticideType: insecticide,
				color: getRandomColor(),
				subset: byInsecticide
			});
		});
		
		// Subsets where location == "Jamaica" and possible insecticides == "malathion" or "permethrin"
		
		// Attempt to draw a plot
		
		// x-axis = frequency
		// y-axis = mortality rate (percent)
		
		// create scales
		var xScale = d3.scaleLinear()
			.domain([0, 1]) // 0% to 100% of selected samples
			.range([0, chartWidth / 2]);
			
		var yExtent = d3.extent(byLocation, function(d) {
			return d.phenotypeValue;
		})
			
		var yScale = d3.scaleLinear()
			.domain(yExtent) // min/max mortality rate
			.range([chartHeight, 0]);
			
			
		var xTranslate = 40;
		var yTranslate = 10;
			
		var xAxisX = 0 + xTranslate;
		var xAxisY = chartHeight + yTranslate;
		
		var yAxisX = 0 + xTranslate;
		var yAxisY = 0 + yTranslate;
		
		// plots for each subset
		for (var i = 0; i < subsets.length; i++) {
			var subset = subsets[i];
			var subsetData = subset['subset'];
			
			// create histogram bins		
			var bins = [[], [], [], [], [], [], [], [], [], []];
			
			subsetData.forEach(function(d) {
				for (var j = 0; j < 10; j++) {
					if (d.phenotypeValue >= (j * 10) && d.phenotypeValue < ((j+1) * 10)) {
						bins[j].push(d);
					}
				}
				if (d.phenotypeValue >= 100) {
					bins[9].push(d);
				}
			});
			
			var subsetPlotG = svg.append('g')
				.attr('class', 'subset-plot')
				.attr('transform', 'translate(' + [padding.l, padding.t] + ')');
			
			// ~~~~~~~~~~~~~~~~~~~~ scatterplot to debug ~~~~~~~~~~~~~~~~~~~~
			subsetPlotG.selectAll('.data-case')
				.data(subsetData)
				.enter()
				.append('circle')
				.attr('class', 'data-case')
				.attr('r', function(d) {
					return 5;
				})
				.attr('cx', function(d) {
					var xValue = 0;

					for (var j = 0; j < bins.length; j++) {
						var bin = bins[i];
						for (var k = 0; k < bin.length; k++) {
							if (bin[k].sampleId == d.sampleId) {
								xValue = (bin.length * 1.0) / subsetData.length;
							}
						}
					}

					return xTranslate + xScale(xValue);
				})
				.attr('cy', function(d) {
					return yTranslate + yScale(d.phenotypeValue);
				})
				.style('fill', function(d) {
					return subset['color'];
				});
			// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		}
			
		// create axes
		svg.append('g')
			.attr('class', 'x axis')
			.attr('transform', 'translate(' + [xAxisX, xAxisY] + ')')
			.call(d3.axisBottom(xScale).ticks(5));
			
		// create axes
		svg.append('g')
			.attr('class', 'y axis')
			.attr('transform', 'translate(' + [yAxisX, yAxisY] + ')')
			.call(d3.axisLeft(yScale));
	});
	
	