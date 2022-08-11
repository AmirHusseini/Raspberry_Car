function FrontSensor(){
	$.ajax({
			type: "GET",
			url: baseuri + "/api/" + "frontsensor",
			dataType: "json",
			headers: {
				"Authorization": "Basic " + btoa(username + ":" + password)
			},
			success: function (data){
					$("#response").prepend(JSON.stringify(data) + '</br>');
					toastr.success(data.reading + " cms", 'IOT Robot Sensor');
			},
			error: function(xhr, status, error) {
				toastr.error("Status: " + status + " Error: " + error, "Oops!");
			}
	});
}

function Forward(){
	CallControlApi("forward");
}
function Left(){
	CallControlApi("left");
}
function Brake(){
	CallControlApi("brake");
}
function Right(){
	CallControlApi("right");
}
function pivot_left(){
	CallControlApi("pivot left");
}
function pivot_right(){
	CallControlApi("pivot right");
}
function Reverse(){
	CallControlApi("reverse");
}

function CallControlApi(control){
		alert (">>>>>>>>>>>>>>>>>>>>>>>> CallControlApi Click function" );

	$.ajax({
		type: "GET",
		url: baseuri + "/api/" + control,
		dataType: "json",
		headers: {
			"Authorization": "Basic " + btoa(username + ":" + password)
		},
		
		success: function (data){
			$("#response").prepend(JSON.stringify(data) + '</br>');
			var msg = '';
			if(control == 'brake'){
				msg = 'I am resting now!';
			}
			else{
				msg = 'I am moving ' + control;
			}
			toastr.success(msg, 'STI Raspberry-Pi IoT Robot');
	    },
		error: function(xhr, status, error) {
			toastr.error('Error in calling: ' + control + " Status: " + status + " Error: " + error, "Oops!")
		}
	});

		alert (">>>>>>>>END>>>>>>>>>>>>>>>> CallControlApi Click function" );
	
}