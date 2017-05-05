var p = {f: null, t: null, s: null, d: null};
var pl = payload.toString("utf-8");

p.payload = pl
p.f = parseInt(pl.substr(0, 1));
switch (p.f) {
   case 7:
      p.t = parseFloat(pl.substr(1, 5));
      p.s = parseFloat(pl.substr(6, 4));
      p.d = parseFloat(pl.substr(10, 3));
      break;
   case 3:
      p.s = parseFloat(pl.substr(1, 4));
      p.d = parseFloat(pl.substr(5, 3));
      break;
   case 5:
      p.t = parseFloat(pl.substr(1, 5));
      p.d = parseFloat(pl.substr(6, 3));
      break;
   case 6:
      p.t = parseFloat(pl.substr(1, 5));
      p.s = parseFloat(pl.substr(6, 4));
      break;
   case 4:
      p.t = parseFloat(pl.substr(1, 5));
      break;
   case 2:
      p.s = parseFloat(pl.substr(1, 4));
      break;
   case 1:
      p.d = parseFloat(pl.substr(1, 3));
      break;
}
return p;
