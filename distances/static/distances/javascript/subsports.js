
function getSubSports() {
	var sport = document.getElementById("id_sport").value;
	var sport2 =setSubSports(sport);
	
}

function setSubSports(sport){
	var ss = document.getElementById("id_sub_sport");
	
	var choices = json_data;
	ss.options.length = 0;

	var data = choices[sport];
	for (var k in data) {
		opt = document.createElement('option');
		opt.value = data[k];
		opt.innerHTML = data[k];
		ss.appendChild(opt)
	}
	return data;
}

