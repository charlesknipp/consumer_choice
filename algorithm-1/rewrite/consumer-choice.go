package main

import (
	"errors"
	"fmt"
	"math"
	"time"
)

/*
	this version should rewrite the intersection without the use of separate
	functions to find min and max, and should find all points

	additionally it is worth using the given bundle to eliminate the need to
	find both since we already have one of the two (under strict convexity/IDs)
*/

// define parameters and variables present in the optimization problem

var m, u float64
var t [2]float64
var p [2]float64

func B(x1, income float64) float64 {
	x2 := (income - (p[0] * x1)) / p[1]
	return x2
}

func I(x1, utility float64) float64 {
	x2 := math.Pow((utility / math.Pow(x1, t[0])), (1 / t[1]))
	return x2
}

// the rest of the functions are replacements for findIntersection

func difference(x1, income, utility float64) float64 {
	return I(x1, utility) - B(x1, income)
}

func derive(value, utility float64) float64 {
	h := 0.0001
	top := difference(value+h, m, utility) - difference(value, m, utility)
	bottom := h

	return top / bottom
}

func newtonsMethod(guess, utility float64) (float64, error) {
	xn := guess

	for n := 0; n <= 20; n++ {
		fxn := difference(xn, m, utility)
		Dfxn := derive(xn, utility)

		if math.Abs(fxn) < .001 {
			return xn, nil
		}

		if Dfxn == 0 {
			return -100, errors.New("newtonsMethod: zero division")
		}

		xn = xn - (fxn / Dfxn)
	}

	return -100, errors.New("newtonsMethod: exceeded max interations")
}

func adjust(lx, ux float64) float64 {

	x1 := (lx + ux) / 2
	x2 := B(x1, m)

	u := (math.Pow(x1, t[0])) * (math.Pow(x2, t[1]))

	return u
}

// close but nah, but still really close

func main() {
	// this is for the Marshallian case
	start := time.Now()

	m = 100

	t[0], t[1] = .3, .7
	p[0], p[1] = 3, 2

	u = math.Pow(.5*(m/p[0]), t[0]) * math.Pow(.5*(m/p[1]), t[1])

	var bounds [2]float64
	bounds[0], _ = newtonsMethod(.0001, u)
	bounds[1], _ = newtonsMethod(m/p[0], u)

	ctr := 0
	for bounds[1]-bounds[0] > .001 {
		u = adjust(bounds[0], bounds[1])
		bounds[0], _ = newtonsMethod(bounds[0], u)
		bounds[1], _ = newtonsMethod(bounds[1], u)
		fmt.Println(bounds)
		if ctr > 20 {
			break
		}
		ctr += 1
	}

	bundle := []float64{bounds[0], B(bounds[0], m)}
	elapsed := time.Since(start)

	for i := 0; i < 2; i++ {
		fmt.Printf("%.3f\t", bundle[i])
	}

	fmt.Printf("\ntime: %s", elapsed)
}
