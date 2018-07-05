<!doctype html>
<html lang="en">

<head>
	<title>GIC GNSS portal</title>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
	<!-- VENDOR CSS -->
	<link rel="stylesheet" href="/static/vendor/bootstrap/css/bootstrap.min.css">
	<link rel="stylesheet" href="/static/vendor/font-awesome/css/font-awesome.min.css">
	<link rel="stylesheet" href="/static/vendor/linearicons/style.css">
	<link rel="stylesheet" href="/static/vendor/chartist/css/chartist-custom.css">
	<!-- MAIN CSS -->
	<link rel="stylesheet" href="/static/css/main.css">
	<!-- FOR DEMO PURPOSES ONLY. You should remove this in your project -->
	<link rel="stylesheet" href="/static/css/demo.css">
	<!-- GOOGLE FONTS -->
	<link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700" rel="stylesheet">
	<!-- ICONS -->
	<link rel="apple-touch-icon" sizes="76x76" href="/static/img/apple-icon.png">
	<link rel="icon" type="image/png" sizes="96x96" href="/static/img/favicon.ico">
</head>

<body>


	<!-- WRAPPER -->
	<div id="wrapper">
	{% include 'header.php' %}
	
	
	<!-- MAIN -->
	<div class="main">
	{% include 'button.php' %}
		<h1>GIC | Online GNSS service portal</h1>

	
  <div id="myCarousel" class="carousel slide" data-ride="carousel">
    <!-- Indicators -->
    <ol class="carousel-indicators">
      <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
      <li data-target="#myCarousel" data-slide-to="1"></li>
      <li data-target="#myCarousel" data-slide-to="2"></li>
    </ol>

    <!-- Wrapper for slides -->
    <div class="carousel-inner">
      <div class="item active">
        <img src="/static/img/gps1.jpg" alt="Los Angeles" style="width:100%;">
      </div>

      <div class="item">
        <img src="/static/img/gps2.jpg" alt="Chicago" style="width:100%;">
      </div>
    
      <div class="item">
        <img src="/static/img/gps3.jpg" alt="New york" style="width:100%;">
      </div>
    </div>

    <!-- Left and right controls -->
    <a class="left carousel-control" href="#myCarousel" data-slide="prev">
      <span class="glyphicon glyphicon-chevron-left"></span>
      <span class="sr-only">Previous</span>
    </a>
    <a class="right carousel-control" href="#myCarousel" data-slide="next">
      <span class="glyphicon glyphicon-chevron-right"></span>
      <span class="sr-only">Next</span>
    </a>
  </div>


<div class="col-md-12">	<br>
	
		<p style=text-align:center;><b>This portal is a free online GNSS data processing facility provided by Geoinformatics Center Thailand. It takes advantage of both World-wide reference stations and user provided data files. This works with data collected anywhere on Earth.</b></p>

	<div class="col-md-12">
		<h2><b>POST-PROCESSING PORTAL SERVICES</b></h2>
		<h4><span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>  <b>POST-PROCESSING GNSS DATA</b></h4>

			<p style=text-align:justify;>For many applications, such as airborne survey, control point establishment corrected GNSS positions are not required in real-time. Post-processing  generally results in a more accurate, comprehensive positional solution. This project entirely relies on free and open source applications and provide free post-processing service for users in various processing modes 
</p>


			 <h4><span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>  <b>RTK SERVICE</b></h4>

			<p style=text-align:justify;>GIC operates a Trimble Reference Station system. The system includes a 12 channel Trimble Pro XR receiver capable of tracking 12 satellites simultaneously.This GPS base station is connected to the NTRIP Global Real-Time GPS Reference Stations Network on 2006 March 13th as First Base Station From Thailand. You can get access to the NTRIP Server by registering via this portal.</p>


			 <h4><span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>  <b>DOWNLOAD 24 HOURS OPERATING CORS DATA</b></h4>

			<p style=text-align:justify;>User friendly Geoinformatics center data download interface provide access to UNAVCO CORS data where community of geodetic scientists uses for quantifying the motions of rock, ice and water that are monitored by a variety of sensor types at or near the Earth's surface. After processing, these data enable millimeter-scale surface motion detection and monitoring at discrete points, and high-resolution strain imagery over areas of tens of square meters to hundreds of square kilometers. The data types include GPS/GNSS observation, navigation and meteorological data.</p>
	</div>
	</div>	
	</div>
	<!-- END MAIN -->
		<div class="clearfix"></div>
		{% include 'footer.php' %}
	</div>
	<!-- END WRAPPER -->
	<!-- Javascript -->
	<script src="/static/vendor/jquery/jquery.min.js"></script>
	<script src="/static/vendor/bootstrap/js/bootstrap.min.js"></script>
	<script src="/static/vendor/jquery-slimscroll/jquery.slimscroll.min.js"></script>
	<script src="/static/vendor/jquery.easy-pie-chart/jquery.easypiechart.min.js"></script>
	<script src="/static/vendor/chartist/js/chartist.min.js"></script>
	<script src="/static/js/klorofil-common.js"></script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

</body>

</html>
