function nodeclick(){
	var group = d3.select(this);
	var circle = group.select('circle');

	var type = circle.attr("type");

	//console.log(group);
	//console.log(circle);

	if(group.classed('selected')){
		group.select('text').style('opacity',0);

		circle.attr("r",radius);

		group.classed('selected',false);
	}else{
		group.moveToFront();

		var text = group.select('text').html();

		group.classed('selected', true);

		circle.attr("r",3*radius);

		var nodeinfo = d3.select(".nodeinfo");
		var procinfo = d3.select(".procinfo");

		if(type == "procedure"){
			procinfo.html(text);
		}else{
			nodeinfo.html(text);
		}
	}
}

function nodehover(){
	var group = d3.select(this);
	var circle = group.select('circle');

	var type = circle.attr("type");

	//console.log(group);
	//console.log(circle);

	if(group.classed('selected')){
		group.select('text').style('opacity',0);

		group.classed('selected',false);
	}else{
		group.moveToFront();

		var text = group.select('text').html();

		group.classed('selected', true);

		var nodeinfo = d3.select(".nodeinfo");
		var procinfo = d3.select(".procinfo");

		if(type == "procedure"){
			procinfo.html(text);
		}else{
			nodeinfo.html(text);
		}
	}	
}

function loadColors(selectedChronics){
	//console.log("loadcolors");
	//console.log(chronicdata);
	console.log(selectedChronics);

	var chronics = ["cancer", "COPD", "osteo", "ischemicHeart", "arthritis", "heartFailure", "alzheimers", "stroke", "kidney",  "depression", "diabetes"];

	if(selectedChronics.length == 0){
		d3.selectAll("circle")
		.style("display","")
		.style("fill", color[color.length/2]);
	}else{
		d3.selectAll("circle")
		.style("fill", function(){
			d3.select(this).style("display","");

			code = d3.select(this).attr("code");
			var chronicKeys = d3.keys(diagdata[code]);
			var glyphdata = [{"label":"sel", "value":0},{"label":"else","value":0}];

			chronicKeys.forEach(function(cd){
				if(chronics.indexOf(cd) > -1){
					if(selectedChronics.indexOf(cd) > -1){
						glyphdata[0]['value'] += diagdata[code][cd]
					}else{
						glyphdata[1]['value'] += diagdata[code][cd]
					}
				}
			});

			//console.log(glyphdata);

			var distrib = (glyphdata[0]['value'] / (glyphdata[0]['value'] + glyphdata[1]['value']));

			if(glyphdata[0]['value'] != 0 && distrib >= 0.05){
				var colorsect = color[Math.round(distrib * (color.length-1))];	
				
				return colorsect;			
			}else{
				d3.select(this).style("display","none");
			}
		});
	}
}

d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

$(document).ready(function(){
	$('#chroncontent').slideUp(0);
	$('#diagcontent').slideUp(0);
	$('#proccontent').slideUp(0);
});

$(document).on("click","#chronbtn",function(){
	$(this).toggleClass("selected");
	$("#chroncontent").slideToggle();
});

$(document).on("click","#diagnosisbtn",function(){
	$(this).toggleClass("selected");
	$("#diagcontent").slideToggle();
});

$(document).on("click","#procbtn",function(){
	$(this).toggleClass("selected");
	$("#proccontent").slideToggle();
});

$(document).on("change","#chroncontent input",function(){
	var selectedChronics = [];
	$("#chroncontent input").each(function(){
		var c = $(this);
		if(c.prop( "checked" )){
			selectedChronics.push(c.attr("name"));
		}
	});

	loadColors(selectedChronics);
})

$(document).on("click","#avg-toggle", function(){
	if($(this).html() == "Show Average Cost"){
		$(".total_avg").toggle();
		$(this).html("Hide Average Cost");
	}else{
		$(".total_avg").toggle();
		$(this).html("Show Average Cost");
	}
})

$(document).on("change","#diagcontent input",function(){
	var c = $(this);
	var code = c.attr("name");

	if(code == "selectall"){
		if(c.prop("checked")){
			$("#diagcontent input").each(function(){
				var d = $(this);
				d.prop("checked", true)
			});
			d3.selectAll('circle').each(function(){
				var cir = d3.select(this);
				cir.style("display","");
			});
		}else{
			$("#diagcontent input").each(function(){
				var d = $(this);
				d.prop("checked", false)
			});
			d3.selectAll('circle').each(function(){
				var cir = d3.select(this);
				cir.style("display","none");
			});	
		}	
	}else{
		if(c.prop("checked")){
			d3.selectAll('circle').each(function(){
				var c = d3.select(this);
				if(c.attr("l1_code") == code){
					c.style("display","");
				}
			});	
		}else{
			d3.selectAll('circle').each(function(){
				var c = d3.select(this);
				if(c.attr("l1_code") == code){
					c.style("display","none");
				}
			});		
		}
	}
});

$(document).on("change","#proccontent input",function(){
	var c = $(this);
	var code = c.attr("name");

	if(code == "selectall"){
		if(c.prop("checked")){
			$("#proccontent input").each(function(){
				var d = $(this);
				d.prop("checked", true)
			});
			d3.selectAll('circle').each(function(){
				var cir = d3.select(this);
				cir.style("display","");
			});
		}else{
			$("#proccontent input").each(function(){
				var d = $(this);
				d.prop("checked", false)
			});
			d3.selectAll('circle').each(function(){
				var cir = d3.select(this);
				cir.style("display","none");
			});	
		}	
	}else{
		if(c.prop("checked")){
			d3.selectAll('circle').each(function(){
				var c = d3.select(this);
				if(c.attr("l1_code") == code){
					c.style("display","");
				}
			});	
		}else{
			d3.selectAll('circle').each(function(){
				var c = d3.select(this);
				if(c.attr("l1_code") == code){
					c.style("display","none");
				}
			});		
		}
	}
});

$(document).on("change",".typesel.smallmult",function(){
	var type = $(this).val();
	$(".graphwrap").empty();
	load_small_mult(type);
});

$(document).on("change",".typesel.l2",function(){
	var type = $(this).val();
	$(".graphwrap").empty();
	load_l2analysis(type);
});

$(document).on("change",".typesel.proc",function(){
	var type = $(this).val();
	$(".proc-wrap").empty();
	$(".diag-wrap").empty();
	load_procanalysis(type);
});