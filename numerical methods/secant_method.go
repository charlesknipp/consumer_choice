package main

import (
	"fmt"
	"math"
)

// this is pretty broken so we're going to stick with python for now

var p [2]float64
var t [2]float64
var m, u float64

func intersection(x1, inc, utl float64) float64 {
	b := (inc - (p[0] * x1)) / p[1]
	i := math.Pow((utl / math.Pow(x1, t[0])), (1 / t[1]))

	return (i - b)
}

func secant(v float64) float64 {
	h := .0001
	top := intersection(v+h, m, u) - intersection(v, m, u)
	bottom := h
	slope := top / bottom

	return slope
}

func secantMethod(x0 float64, max_iters int) float64 {
	xn := x0
	var h float64
	fxn := intersection(xn, m, u)
	Dfxn := secant(fxn)

	for i := 0; i <= max_iters; i++ {
		fxn = intersection(xn, m, u)
		Dfxn = secant(fxn)

		h = fxn / Dfxn
		xn = xn - h
	}
	return xn
}

func main() {
	p[0], p[1] = 3, 2
	t[0], t[1] = .3, .2

	m = 100.0
	u = math.Pow(.5*(m/p[0]), t[0]) * math.Pow(.5*(m/p[1]), t[1])

	intr := make([]float64, 2)

	intr[0] = secantMethod(.001, 50)
	intr[1] = secantMethod(m/p[0], 50)

	fmt.Printf("%.6f\t%.6f", intr[0], intr[1])
}
