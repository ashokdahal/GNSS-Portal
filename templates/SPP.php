{% from "_render_field.html" import render_field, render_radio_fields %}
<!doctype html>
<html lang="en">

<head>
  <title>Post processing</title>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
  <!-- VENDOR CSS -->
      <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v0.12.0/mapbox-gl.js'></script>
  <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v0.12.0/mapbox-gl.css' rel='stylesheet' />
<script src='/static/js/stations.js'></script>
  
  <link rel="stylesheet" href="/static/vendor/bootstrap/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/vendor/font-awesome/css/font-awesome.min.css">
  <link rel="stylesheet" href="/static/vendor/linearicons/style.css">
  <link rel="stylesheet" href="/static/vendor/chartist/css/chartist-custom.css">
  <!-- MAIN CSS -->
  <link rel="stylesheet" href="/static/css/main.css">
  <link rel="stylesheet" href="/static/css/user.css">
  
   
  <!-- FOR DEMO PURPOSES ONLY. You should remove this in your project -->
  <link rel="stylesheet" href="/static/css/demo.css">
  <!-- GOOGLE FONTS -->
  <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700" rel="stylesheet">
  <!-- ICONS -->
  <link rel="apple-touch-icon" sizes="76x76" href="/static/img/apple-icon.png">
  <link rel="icon" type="image/png" sizes="96x96" href="/static/img/favicon.ico">
  
    <link rel="stylesheet" href="/static/css/leaflet.css"/>
  <script src="/static/js/leaflet.js"></script>
</head>
<body>
  <!-- WRAPPER -->
  <div id="wrapper">
    
    {% include 'header.php' %}
    <div class="main">
      <!-- MAIN CONTENT -->
      {% include 'button.php' %}
      <h1>Post-processing of GNSS data</h1>
      <div class="main-content">
        <div class="container-fluid">
          
          <div class="row">
            <div class="col-md-6">
                      <div class="panel">
                          <div class="panel-heading">
                            <h3 class="panel-title">World-wide reference stations</h3>
                          </div>
                                            <div class="panel-body">
                    <!--<div id="demo-line-chart" class="ct-chart"></div>-->
                   <div id="map" style="width:1=500px;height:500px"></div>
                   <script>
                                      ///// Base map 
                mapboxgl.accessToken = 'pk.eyJ1IjoicmljaGllZGxvbiIsImEiOiJjajYzN2FhZTQxZGphMzJuMHdjOG53bnBiIn0.UhqBT6Fn3AXMDS2hzj0QxQ';
                      var map = new mapboxgl.Map({
                          container: 'map',
                          style: 'mapbox://styles/mapbox/streets-v8',
                          center: [30, 30],
                          zoom: 0
                      });

                      map.on('style.load', function () {
                          map.addSource("markers", {
                              "type": "geojson",
                              "data": cors
                          });

                          map.addLayer({
                              "id": "markers",
                              "interactive": true,
                              "type": "symbol",
                              "source": "markers",
                              "layout": {
                                  "icon-image": "mountain-15",
                                  "icon-size": 1
                              },
                              "paint": {
                                  /*"text-size": 10,*/
                              }
                          });
                      });

                      map.on('click', function (e) {
                          // Use featuresAt to get features within a given radius of the click event
                          // Use layer option to avoid getting results from other layers
                          map.featuresAt(e.point, {layer: 'markers', radius: 10, includeGeometry: true}, function (err, features) {
                              if (err) throw err;
                              // if there are features within the given radius of the click event,
                              // fly to the location of the click event
                              if (features.length) {
                                  // Get coordinates from the symbol and center the map on those coordinates
                                  map.flyTo({center: features[0].geometry.coordinates});
                                  var stnid = features[0].properties.stnid;                                  
                                  var Earliest_Date = features[0].properties.earliest_d;                                  
                                  var Latest_Date = features[0].properties.latest_dat;                                  
                                  var interval = features[0].properties.interval;                                  
                                  var tooltip = new mapboxgl.Popup()
                                      .setLngLat(e.lngLat)
                                      .setHTML('<h5>Station ID :</h5><p>'+ stnid + '</p><h5>Earliest Date :</h5><p>'+Earliest_Date+'</p><h5>Latest Date :</h5><p>'+Latest_Date+'</p>')                     
              
                                      .addTo(map);
                              }
                          });
                      });

                      // Use the same approach as above to indicate that the symbols are clickable
                      // by changing the cursor style to 'pointer'.
                      map.on('mousemove', function (e) {
                          map.featuresAt(e.point, {layer: 'markers', radius: 10}, function (err, features) {
                              if (err) throw err;
                              map.getCanvas().style.cursor = features.length ? 'pointer' : '';
                          });
                      });
                      </script>
                
                </div>
                      </div>
           
            </div>
            <div class="col-md-6">
              <div class="panel">
                <div class="panel-heading">
                  <h3 class="panel-title">Single Point Post-processing</h3>
                </div>
                <div class="panel-body">                          
         
        <form id="upload-form" action="{{ url_for('SPP') }}" method="POST" enctype="multipart/form-data">
                          {{ SPP.csrf_token }}                 
                                <fieldset>                              
                                  {{ render_field(SPP.sfileObsRover) }}
                                  <p style="color:red;">{{errorObs}}</p>
                                  {{ render_field(SPP.sfileNavRover) }}
                                  <p style="color:red;">{{errorNav}}</p>
                                  {{ render_field(SPP.sema) }}
                                  {{ render_radio_fields(SPP.sfrq) }}
                                  {{ render_field(SPP.semail) }}
                                  {{ render_field(SPP.sName) }}
                                  <div class="form-group">
                                    <div class="col-md-6 col-lg-offset-2">
                                      <button type="reset" class="btn btn-default">Reset</button>
                                      <button type="submit" class="btn btn-primary">Submit</button>
                                    </div>
                                  </div>
                                </fieldset>
                            </form>
                                                         
                </div>
              </div>
            </div>
          </div>
          
          </div>
        </div>
      <!-- END MAIN CONTENT -->
      </div>    
    </div>
    <div class="col-md-12">
    {% include 'footer.php' %}</div> 
    <div class="clearfix"></div>
     
  </div>
  <!-- END WRAPPER -->
  <!-- Javascript -->
  <script src="/static/vendor/jquery/jquery.min.js"></script>
  <script src="/static/vendor/bootstrap/js/bootstrap.min.js"></script>
  <script src="/static/vendor/jquery-slimscroll/jquery.slimscroll.min.js"></script>
  <script src="/static/vendor/jquery.easy-pie-chart/jquery.easypiechart.min.js"></script>
  <script src="/static/vendor/chartist/js/chartist.min.js"></script>
  <script src="/static/js/klorofil-common.js"></script>
  
</body>

</html>

  
        
