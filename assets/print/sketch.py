#!/usr/bin/env python3
"""A tiny 'hand-drawn' pen for reportlab: wraps a canvas and renders every stroke as a
slightly wobbly, double-passed line (Rough.js-ish), so vector motifs read as sketched by
hand rather than geometric. Motifs keep their normal reportlab-style calls (line, circle,
ellipse, roundRect, beginPath/curveTo, drawPath); only the strokes get roughened.
"""
import math, random


class RoughPath:
    def __init__(self):
        self.subs = []; self.closed = []; self.cur = None

    def moveTo(self, x, y):
        self.cur = [(x, y)]; self.subs.append(self.cur); self.closed.append(False)

    def lineTo(self, x, y):
        self.cur.append((x, y))

    def curveTo(self, c1x, c1y, c2x, c2y, x, y):
        x0, y0 = self.cur[-1]
        for i in range(1, 11):
            t = i/10; mt = 1-t
            self.cur.append((mt**3*x0+3*mt**2*t*c1x+3*mt*t**2*c2x+t**3*x,
                             mt**3*y0+3*mt**2*t*c1y+3*mt*t**2*c2y+t**3*y))

    def close(self):
        if self.closed:
            self.closed[-1] = True


class Pen:
    """Delegates styling/text to the real canvas; roughens geometric strokes."""
    def __init__(self, c, rough=1.3, seed=7):
        object.__setattr__(self, "c", c)
        object.__setattr__(self, "rough", rough)
        object.__setattr__(self, "rng", random.Random(seed))

    def __getattr__(self, name):
        return getattr(self.c, name)

    def _j(self, amp):
        return (self.rng.random()*2-1)*amp

    def _stroke(self, pts, closed=False, passes=2):
        c = self.c
        if len(pts) < 2:
            return
        for pi in range(passes):
            amp = self.rough*(1.0 if pi == 0 else 0.72)
            seq = list(pts) + ([pts[0]] if closed else [])
            p = c.beginPath()
            x0, y0 = seq[0]; p.moveTo(x0+self._j(amp), y0+self._j(amp))
            for (x, y) in seq[1:]:
                p.lineTo(x+self._j(amp), y+self._j(amp))
            c.drawPath(p, stroke=1, fill=0)

    def line(self, x0, y0, x1, y1):
        self._stroke([(x0, y0), ((x0+x1)/2, (y0+y1)/2), (x1, y1)])

    def circle(self, cx, cy, r, stroke=1, fill=0):
        self.ellipse(cx-r, cy-r, cx+r, cy+r)

    def ellipse(self, x0, y0, x1, y1, stroke=1, fill=0):
        cx, cy = (x0+x1)/2, (y0+y1)/2; rx, ry = abs(x1-x0)/2, abs(y1-y0)/2
        n = 24; a0 = self.rng.random()*6.28
        pts = [(cx+math.cos(a0+2*math.pi*i/n)*rx, cy+math.sin(a0+2*math.pi*i/n)*ry) for i in range(n)]
        self._stroke(pts, closed=True)

    def roundRect(self, x, y, w, h, r, stroke=1, fill=0):
        pts = []; st = 5
        for (ccx, ccy, a0, a1) in [(x+r, y+r, math.pi, 1.5*math.pi),
                                   (x+w-r, y+r, 1.5*math.pi, 2*math.pi),
                                   (x+w-r, y+h-r, 0, 0.5*math.pi),
                                   (x+r, y+h-r, 0.5*math.pi, math.pi)]:
            for i in range(st+1):
                a = a0+(a1-a0)*i/st
                pts.append((ccx+math.cos(a)*r, ccy+math.sin(a)*r))
        self._stroke(pts, closed=True)

    def beginPath(self):
        return RoughPath()

    def drawPath(self, path, stroke=1, fill=0):
        for sub, closed in zip(path.subs, path.closed):
            self._stroke(sub, closed=closed)
