///// Base map 
		var OpenStreetMap = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');	
		///// Default Base map initialization 	
		var map = L.map('map', {
				layers: [OpenStreetMap], /// Base map
				center: [6.925, 79.86],/// Map center
				zoom: 12	//// Zoom level
			});
		/////Base map initialization 	
		var baseLayers = {
			"Open Street Map": OpenStreetMap			
		};		
		///// layers from Geoserver (format WMS)
		var market = L.tileLayer.wms("http://localhost:8080/geoserver/wms", {
			layers: 'research:Markets and Shopping malls',
			format: 'image/png',
			transparent: true,
			version: '1.1.0',
			attribution: "myattribution"
		}).addTo(map);						  
		///// Group layers
		var overlays = {			
			"Market": market			
		};		