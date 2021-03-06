window.onload = start;

function Point3D(x,y,z) {
    this.x = x;
    this.y = y;
    this.z = z;

    this.rotateX = function(angle) {
        var rad, cosa, sina, y, z
        rad = angle * Math.PI / 180
        cosa = Math.cos(rad)
        sina = Math.sin(rad)
        y = this.y * cosa - this.z * sina
        z = this.y * sina + this.z * cosa
        return new Point3D(this.x, y, z)
    }

    this.rotateY = function(angle) {
        var rad, cosa, sina, x, z
        rad = angle * Math.PI / 180
        cosa = Math.cos(rad)
        sina = Math.sin(rad)
        z = this.z * cosa - this.x * sina
        x = this.z * sina + this.x * cosa
        return new Point3D(x,this.y, z)
    }

    this.rotateZ = function(angle) {
        var rad, cosa, sina, x, y
        rad = angle * Math.PI / 180
        cosa = Math.cos(rad)
        sina = Math.sin(rad)
        x = this.x * cosa - this.y * sina
        y = this.x * sina + this.y * cosa
        return new Point3D(x, y, this.z)
    }

    this.project = function(viewWidth, viewHeight, fov, viewDistance) {
        var factor, x, y
        factor = fov / (viewDistance + this.z)
        x = this.x * factor + viewWidth / 2
        y = this.y * factor + viewHeight / 2
        return new Point3D(x, y, this.z)
    }
}

var vertices = [
    new Point3D(0.128722786176, -0.470689115479, -0.843124319319),
    new Point3D(0.664490836666, -0.542720627299, -0.513718063425),
    new Point3D(0.067231757421, -0.915424296288, -0.396835291472),
    new Point3D(-0.477827296216, -0.553660898741, -0.682012231706),
    new Point3D(-0.217433237995, 0.0426248458193, -0.97514404553),
    new Point3D(0.488558194092, 0.0493863054159, -0.871132529424),
    new Point3D(0.520357593389, -0.822770001559, 0.0354106830462),
    new Point3D(0.930056729699, -0.347522224561, 0.119259309811),
    new Point3D(0.496926398597, -0.599586646109, 0.627343612529),
    new Point3D(-0.0363287606101, -0.950569428715, 0.308379607526),
    new Point3D(-0.492944842901, -0.832474656843, -0.113876004978),
    new Point3D(-0.645391734284, -0.610526917545, 0.459049444249),
    new Point3D(-0.918252835272, -0.365223955596, -0.153046374577),
    new Point3D(-0.745459203897, 0.0173704973555, -0.626869410709),
    new Point3D(-0.930056729699, 0.34752222456, -0.119259309809),
    new Point3D(-0.496926398601, 0.599586646109, -0.627343612529),
    new Point3D(0.111780774649, 0.552308343107, -0.794630083428),
    new Point3D(0.0363287606109, 0.950569428716, -0.308379607527),
    new Point3D(0.645391734283, 0.610526917545, -0.459049444251),
    new Point3D(0.894098578903, 0.0330729594551, -0.385318475413),
    new Point3D(0.918252835273, 0.365223955594, 0.153046374575),
    new Point3D(0.492944842899, 0.832474656841, 0.11387600498),
    new Point3D(-0.0672317574218, 0.915424296287, 0.396835291473),
    new Point3D(0.477827296216, 0.553660898738, 0.682012231705),
    new Point3D(-0.52035759339, 0.82277000156, -0.0354106830472),
    new Point3D(-0.664490836666, 0.5427206273, 0.513718063425),
    new Point3D(-0.894098578901, -0.0330729594491, 0.385318475414),
    new Point3D(-0.488558194091, -0.0493863054145, 0.871132529424),
    new Point3D(-0.111780774649, -0.552308343108, 0.794630083427),
    new Point3D(0.217433237997, -0.0426248458174, 0.97514404553),
    new Point3D(0.745459203899, -0.0173704973539, 0.62686941071),
    new Point3D(-0.128722786178, 0.470689115477, 0.843124319319)
];

// Define the vertices that compose each of the 6 faces. These numbers are
// indices to the vertex list defined above.
var faces = [[0,1,2],[0,2,3],[0,3,4],[0,4,5],[0,5,1],[6,2,1],[6,1,7],[6,7,8],[6,8,9],[6,9,2],[10,3,2],[10,2,9],[10,9,11],[10,11,12],[10,12,3],[13,4,3],[13,3,12],[13,12,14],[13,14,15],[13,15,4],[16,5,4],[16,4,15],[16,15,17],[16,17,18],[16,18,5],[19,1,5],[19,5,18],[19,18,20],[19,20,7],[19,7,1],[21,22,23],[21,23,20],[21,20,18],[21,18,17],[21,17,22],[24,25,22],[24,22,17],[24,17,15],[24,15,14],[24,14,25],[26,27,25],[26,25,14],[26,14,12],[26,12,11],[26,11,27],[28,29,27],[28,27,11],[28,11,9],[28,9,8],[28,8,29],[30,23,29],[30,29,8],[30,8,7],[30,7,20],[30,20,23],[31,23,22],[31,22,25],[31,25,27],[31,27,29],[31,29,23]]

var angle = 0;

function start() {
    canvas = document.getElementById("canvas");
    if( canvas && canvas.getContext ) {
        ctx = canvas.getContext("2d");
        setInterval(loop,66);
    }
}

function loop() {
    var t = new Array();

    ctx.fillStyle = "#262E30";
    ctx.fillRect(0,0,1400,800);

    for( var i = 0; i < vertices.length; i++ ) {
        var v = vertices[i];
        var r = v.rotateX(angle).rotateY(angle).rotateZ(angle);
        var p = r.project(1400,2100,800,1.5);
        t.push(p)
    }

    ctx.strokeStyle = "#484e4e"
    ctx.lineWidth = 1.5;

    for( var i = 0; i < faces.length; i++ ) {
        var f = faces[i]
        ctx.beginPath()
        ctx.moveTo(t[f[0]].x,t[f[0]].y)
        ctx.lineTo(t[f[1]].x,t[f[1]].y)
        ctx.lineTo(t[f[2]].x,t[f[2]].y)
        ctx.closePath()
        ctx.stroke()
    }
    angle += 1
}