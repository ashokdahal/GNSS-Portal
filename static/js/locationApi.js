
			var myCenter=new google.maps.LatLng(7.675323, 80.641338);
			var matale=new google.maps.LatLng(7.467275, 80.623102);
			var horana=new google.maps.LatLng(6.722744, 80.064028);
			var kataragama=new google.maps.LatLng(6.414428, 81.332568);
			var vauniya=new google.maps.LatLng(8.7521311,80.4174508);
			var jaffna=new google.maps.LatLng(9.661664, 80.025403);
			var matara=new google.maps.LatLng(5.954894, 80.554524);
			var kandy=new google.maps.LatLng(7.289606, 80.632819);
			var gampaha=new google.maps.LatLng(7.087554, 80.013171);
			var kankasa=new google.maps.LatLng(9.666124, 80.133517);
			function initialize()
			{
			var mapProp = {
			  center:myCenter,
			  zoom:7,
			  mapTypeId:google.maps.MapTypeId.ROADMAP
			  };

			var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

			var marker1Suyya=new google.maps.Marker({
			  position:matale,
			  });
			var marker2Diga=new google.maps.Marker({
			  position:horana,
			  });
			var marker3Selle=new google.maps.Marker({
			  position:kataragama,
			  });
			var marker4Naren=new google.maps.Marker({
			  position:vauniya,
			  });
			var marker5Pahi=new google.maps.Marker({
			  position:jaffna,
			  });
			var marker6Sanda=new google.maps.Marker({
			  position:matara,
			  });
			var marker7Sila=new google.maps.Marker({
			  position:kandy,
			  });
			var marker8Miga=new google.maps.Marker({
			  position:gampaha,
			  });
			var marker9Sano=new google.maps.Marker({
			  position:kankasa,
			  });	
			   			  
			marker1Suyya.setMap(map);
			marker2Diga.setMap(map);
			marker3Selle.setMap(map);
			marker4Naren.setMap(map);
			marker5Pahi.setMap(map);
			marker6Sanda.setMap(map);
			marker7Sila.setMap(map);
			marker8Miga.setMap(map);
			marker9Sano.setMap(map);
			}

			google.maps.event.addDomListener(window, 'load', initialize);
