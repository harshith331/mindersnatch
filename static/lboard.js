// Modified Datatables ScrolLresize
(function (t) {
	"function" == typeof define && define.amd
		? define(["jquery", "datatables.net"], function (e) {
				return t(e, window, document);
		  })
		: "object" == typeof exports
		? (module.exports = function (e, n) {
				return (
					e || (e = window),
					(n && n.fn.dataTable) || (n = require("datatables.net")(e, n).$),
					t(n, e, e.document)
				);
		  })
		: t(jQuery, window, document);
})(function (t, e, n, o) {
	var i = function (e) {
		var n = this,
			o = e.table();
		(this.s = {
			dt: e,
			host: t(o.container()).parent(),
			header: t(o.header()),
			footer: t(o.footer()),
			body: t(o.body()),
			container: t(o.container()),
			table: t(o.node())
		}),
			"static" === (o = this.s.host).css("position") &&
				o.css("position", "relative"),
			e.on("draw", function () {
				n._size();
			}),
			this._attach(),
			this._size();
	};
	(i.prototype = {
		_size: function () {
			var e = this.s,
				n = e.dt,
				o = n.table(),
				i = t(e.table).offset().top,
				a = e.host.height(),
				s = t("div.dataTables_scrollBody", o.container());
			(a = a - i - (e.container.height() - (i + s.height()))),
				t("div.dataTables_scrollBody", o.container()).css({
					maxHeight: a - 40,
					height: a - 40
				}),
				n.fixedColumns && n.fixedColumns().relayout();
		},
		_attach: function () {
			var e = this,
				n = t("<iframe/>")
					.css({
						position: "absolute",
						top: 0,
						left: 0,
						height: "100%",
						width: "100%",
						zIndex: -1,
						border: 0
					})
					.attr("frameBorder", "0")
					.attr("src", "about:blank");
			(n[0].onload = function () {
				var t = this.contentDocument.body,
					n = t.offsetHeight,
					o = this.contentDocument;
				(o.defaultView || o.parentWindow).onresize = function () {
					var i = t.clientHeight || t.offsetHeight,
						a = o.documentElement.clientHeight;
					!i && a && (i = a), i !== n && ((n = i), e._size());
				};
			}),
				n.appendTo(this.s.host).attr("data", "about:blank");
		}
	}),
		(t.fn.dataTable.ScrollResize = i),
		(t.fn.DataTable.ScrollResize = i),
		t(n).on("init.dt", function (e, n) {
			"dt" === e.namespace &&
				((e = new t.fn.dataTable.Api(n)),
				(n.oInit.scrollResize || t.fn.dataTable.defaults.scrollResize) && new i(e));
		});
});

// JQUERY UI DRAGGABLE RESIZABLE
const scoreboard = $("#scoreboard");
const scoreboardTitle = $("#scoreboardTitle");

let scoreboardState = { left: 300, top: 180, width: 335, height: 150 };
scoreboard.css("left", scoreboardState.left);
scoreboard.css("top", scoreboardState.top);
scoreboard.css("width", scoreboardState.width);
scoreboard.css("height", scoreboardState.height);

scoreboard.resizable({
	handles: "n, e, s, w, ne, se, sw, nw",
	containment: "#scoreboardContainer"
});

scoreboard.draggable({
	scroll: true,
	containment: "#scoreboardContainer"
});

function toogleScoreboard() {
	$("#scoreboardContainer").toggle("slow", function () {});
}

//DATATABLE
let isResults = false;
let guesses = [];

const table = $("#datatable").DataTable({
	info: false,
	searching: false,
	paging: false,
	scrollY: true,
	scrollResize: true,
	scrollCollapse: true,
	language: { zeroRecords: " " },
	dom: "Bfrtip",
	buttons: [
		{
			extend: "colvis",
			text: "⚙️",
			className: "colvis-btn",
			columns: ":not(.noVis)"
		}
	],
	columns: [
		{ data: "Position" },
		{ data: "Player" },
		{ data: "Streak" },
		{
			data: "Distance",
			render: (data, type) => {
				if (type === "display" || type === "filter") {
					return toMeter(data);
				}
				return data;
			}
		},
		{ data: "Score" }
	],
	columnDefs: [
		{ targets: 0, width: "35px", className: "noVis" },
		{ targets: 1, width: "auto", className: "noVis" },
		{ targets: 2, width: "55px" },
		{ targets: 3, width: "85px" },
		{ targets: 4, width: "68px", type: "natural" }
	]
});

// Column Visisbility
let columnState = getCookie("CG_ColVis", [
	{ column: 2, state: true },
	{ column: 3, state: true },
	{ column: 4, state: true }
]);
restoreColVis();

function restoreColVis() {
	columnState.forEach((column) => {
		table.column(column.column).visible(column.state);
	});
}

// Handle ColVis change
table.on("column-visibility.dt", function (e, settings, column, state) {
	if (isResults) return;

	const i = columnState.findIndex((o) => o.column === column);
	if (columnState[i]) {
		columnState[i] = { column, state };
	} else {
		columnState.push({ column, state });
	}

	setCookie("CG_ColVis", JSON.stringify(columnState), 30);
});

// RESET SCOREBOARD
function resetScoreboard() {
	isResults = false;
	scoreboardTitle.text(`GUESSES (0)`);
	table.clear().draw();

	// Restore columns visibility
	restoreColVis();
}

// ADD GUESS
function addGuess() {
	const distance = genRand(0, 10, 2);
	const score = calculateScore(distance);
	const guess = {
		Position: "",
		Player: `<span class='username' style='color:${randomColor()}'>Super_Player</span>`,
		Streak: Math.floor(Math.random() * 10),
		Distance: distance,
		Score: score
	};
	guesses.push(guess);
	scoreboardTitle.text(`GUESSES (${guesses.length})`);

	const rowNode = table.row.add(guess).node();
	rowNode.classList.add("expand");
	setTimeout(() => {
		rowNode.classList.remove("expand");
	}, 200);

	table.order([3, "asc"]).draw(false);
	table
		.column(0)
		.nodes()
		.each((cell, i) => {
			cell.innerHTML = i + 1;
		});
}

function renderResults() {
	isResults = true;

	scoreboardTitle.text("RESULTS");

	table.clear().draw();

	table.rows.add(guesses);

	table.order([4, "desc"]).draw(false);

	let content;
	table
		.column(0)
		.nodes()
		.each((cell, i) => {
			if (i == 0) content = "<span class='icon'>🏆</span>";
			else if (i == 1) content = "<span class='icon'>🥈</span>";
			else if (i == 2) content = "<span class='icon'>🥉</span>";
			else content = i + 1;

			cell.innerHTML = content;
		});

	// Restore columns visibility
	table.columns().visible(true);

	toTop(".dataTables_scrollBody");
}

//SCROLLER
let isScrolling = false;
let speedDown = 50;

const sliderElem = `<input type="range" min="5" max="50" value="20" id="scrollSpeedSlider">`;
$(".dt-buttons").append(sliderElem);

const slider = document.getElementById("scrollSpeedSlider");
speedDown = slider.value;

slider.oninput = function () {
	speedDown = this.value;
	scroller(".dataTables_scrollBody");
};

const scrollBtn = `
	<div class="dt-button scrollBtn">
	   <label>
		  <input type="checkbox" id="scrollBtn"><span>⮃</span>
	   </label>
	</div>
`;

$(".dt-buttons").prepend(scrollBtn);

$("#scrollBtn").change(function () {
	if (this.checked != true) {
		isScrolling = $(this).is(":checked");
		stop(".dataTables_scrollBody");
		slider.style.display = "none";
	} else {
		isScrolling = $(this).is(":checked");
		scroller(".dataTables_scrollBody");
		slider.style.display = "inline";
	}
});

function toTop(elem) {
	stop(elem);
	setTimeout(() => {
		scroller(elem);
	}, 2000);
}

function scroller(elem) {
	const div = $(elem);

	(function loop() {
		if (!isScrolling) return;
		console.log(div[0].scrollHeight - div.scrollTop() - 84);
		div
			.stop()
			.animate(
				{ scrollTop: div[0].scrollHeight },
				(div[0].scrollHeight - div.scrollTop() - 84) * speedDown,
				"linear",
				() => {
					setTimeout(() => {
						div.stop().animate({ scrollTop: 0 }, 1000, "swing", () => {
							setTimeout(() => {
								loop();
							}, 2000);
						});
					}, 1000);
				}
			);
	})();
}

function stop(elem) {
	$(elem).stop();
}

/* UTILS */
function genRand(min, max, decimalPlaces) {
	return (Math.random() * (max - min) + min).toFixed(decimalPlaces) * 1;
}

function toMeter(distance) {
	return distance >= 1
		? parseFloat(distance.toFixed(1)) + "km"
		: parseInt(distance * 1000) + "m";
}

function calculateScore(distance, scale = 2000) {
	return Math.round(5000 * Math.pow(0.99866017, (distance * 1000) / scale));
}

function randomColor() {
	return "#" + Math.floor(Math.random() * 16777215).toString(16);
}

// Cookies
function setCookie(name, value, exdays = 60) {
	console.log(value);
	const d = new Date();
	d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
	const expires = "expires=" + d.toUTCString();
	document.cookie = name + "=" + value + ";" + expires + ";path=/";
	console.log(document.cookie);
}

function getCookie(name, defaultValue = {}) {
	const cname = name + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(";");
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == " ") {
			c = c.substring(1);
		}
		if (c.indexOf(cname) == 0) {
			return JSON.parse(c.substring(cname.length, c.length));
		}
	}
	return defaultValue;
}
