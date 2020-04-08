anime({
    targets: ".question",
    translateY: ["-10%", "0%"],
    direction: "alternate",
    loop: true,
    easing: "linear"
})

$("hr.upperline").css("width", `${(100 / $("ul.options").children().length)}%`);

$(".options li").hover(function () {
    anime({
        targets: "hr.upperline",
        left: $(this).index() * (100 / $(this).parent().children().length) + "%"
    })
})

var length = 0;

$(".options li").each(function () {
    let temp = $(this).html().split(" ").length
    if (temp > length) length = temp;
})

if (length > 2) {
    $("ul.options li").css("font-size", "0.6rem");
    $(".options").css("height", "100px");
    $("hr.upperline").css("bottom", "87px");
}

$(".options li").click(function() {
    let id = $(this).data("id");
    document.getElementById("mainForm").value = id;
    console.log($("#mainForm").val());
    $("#form-main").submit();
})
/////////////////////////////////////////////////
const $target = $('.thumb__image');
const $thumb = $('.thumb');
const numPoints = 10;
const pts = [];
const delaunay_multiplier = 10;
const svgNS = "http://www.w3.org/2000/svg";
const width = $target.width();
const height = $target.height();

// Add corners
pts.push([0, 0]);
pts.push([0, height * delaunay_multiplier]);
pts.push([width * delaunay_multiplier, height * delaunay_multiplier]);
pts.push([width * delaunay_multiplier, 0]);

// Half
pts.push([width * delaunay_multiplier * 0.5, 0]);
pts.push([width * delaunay_multiplier * 0.5, height * delaunay_multiplier]);
pts.push([0, height * delaunay_multiplier * 0.5]);
pts.push([width * delaunay_multiplier, height * delaunay_multiplier * 0.5]);

for (var i = Math.floor(numPoints); i > 0; i--) {
    if (window.CP.shouldStopExecution(0)) break;
    // Multiply the points by a constant factor to avoid numerical imprecision
    pts.push([(5 + Math.random() * (width - 10)) * delaunay_multiplier, (5 + Math.random() * (height - 10)) * delaunay_multiplier]);
} window.CP.exitedLoop(0);

var d = new Delaunay(pts);
var faces = d.triangulate();
const imageurl = $target.attr('src');
console.log(faces);

function addFace(faces, i) {
    var svg = document.createElementNS(svgNS, "svg");

    var defs = document.createElementNS(svgNS, "defs");
    svg.appendChild(defs);
    var clip = document.createElementNS(svgNS, "clipPath");
    clip.setAttribute('id', 'test-clip-' + i);
    defs.appendChild(clip);

    var p = document.createElementNS(svgNS, "path");
    const x1 = faces[i][0] / delaunay_multiplier;
    const y1 = faces[i][1] / delaunay_multiplier;
    const x2 = faces[i + 1][0] / delaunay_multiplier;
    const y2 = faces[i + 1][1] / delaunay_multiplier;
    const x3 = faces[i + 2][0] / delaunay_multiplier;
    const y3 = faces[i + 2][1] / delaunay_multiplier;

    p.setAttributeNS(null, "d", `M ${x1} ${y1} L ${x2} ${y2} L ${x3} ${y3}`);
    clip.appendChild(p);

    var imageItem = document.createElementNS(svgNS, "image");
    imageItem.setAttributeNS('http://www.w3.org/1999/xlink', "href", imageurl);
    imageItem.setAttributeNS(null, "width", "100%");
    imageItem.setAttributeNS(null, "height", "100%");
    imageItem.setAttributeNS(null, "clip-path", "url(#test-clip-" + i + ")");
    //clip-path=

    svg.appendChild(imageItem);
    //$(svg).css('opacity', Math.random() * 0.8 + 0.2);
    $thumb.append(svg);
}


for (i = 0; i < faces.length; i += 3) {
    if (window.CP.shouldStopExecution(1)) break;
    addFace(faces, i);
} window.CP.exitedLoop(1);

let depth = 700;
$thumb.hover(() => {
    $thumb.find('svg').each((i, el) => {

        let z = Math.random() * depth - depth / 2 + 'px';
        if (Math.random() < 0.4) {
            $(el).css({
                //opacity: 0.9,
                transform: `translateZ(${z})`
            });

        } else {
            $(el).css({
                opacity: Math.random() * 0.2,
                transitionDelay: Math.random() * 0.5 + 's',
                transitionDuration: Math.random() * 0.5 + 0.2 + 's'
            });

        }

    });
}, () => {
    $thumb.find('svg').each((i, el) => {
        $(el).css({
            opacity: 1,
            transform: 'none',
            transitionDelay: Math.random() * 0.6 + 's',
            transitionDuration: Math.random() * 0.8 + 0.6 + 's'
        });

    });
});
