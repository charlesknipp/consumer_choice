package main

import (
	"fmt"
	"log"
	"math"
	"sort"
	"time"
)

var m, k, u float64
var t [2]float64
var p [2]float64

// this function is required to construct a range of feasible values given an
// arbitrary step size; similar to numpy's arange function

func arange(start, stop, step float64) []float64 {

	n := int(math.Ceil((stop - start) / step))
	rnge := make([]float64, n)

	for x := range rnge {
		rnge[x] = start + step*float64(x)
	}

	return rnge
}

// define the sublattice valued budget set; represents the equivalence class of
// affordable combinations of goods 1 and 2

func B(x1, income float64, prices [2]float64) float64 {

	x2 := (income - (prices[0] * x1)) / prices[1]
	return x2
}

// define the sublattice valued indifference set; represents the equivalence
// class of indifferent combinations of goods 1 and 2

func U(x1, utility float64, preferences [2]float64) float64 {

	a := preferences[0]
	b := preferences[1]

	x2 := math.Pow((utility / math.Pow(x1, a)), (1 / b))

	return x2
}

// define a new indifference curve using the mean value theorem onto a convex
// set of indifference

func adjust(lx, ux float64) float64 {

	x1 := (lx + ux) / 2
	x2 := B(x1, m, p)

	u := (math.Pow(x1, t[0])) * (math.Pow(x2, t[1]))

	return u
}

// calculate the points of intersection between the two curves which is then
// used to find a linear combination via the adjust function above

func findIntersection(x []float64, utility float64) []float64 {

	min_f := math.Abs(U(x[0], utility, t) - B(x[0], m, p))
	max_f := math.Abs(U(x[len(x)-1], utility, t) - B(x[len(x)-1], m, p))

	min_x := x[0]
	max_x := x[len(x)-1]

	// find the first point of intersection using increasing differences on a
	// convex equivalence class

	for i := 0; i < len(x); i++ {

		diff := U(x[i], utility, t) - B(x[i], m, p)
		next_diff := U(x[i]+k, utility, t) - B(x[i]+k, m, p)

		if diff < min_f {

			min_f = math.Abs(diff)
			min_x = x[i]

			if math.Abs(diff) <= math.Abs(next_diff) {
				break
			}
		}
	}

	for i := len(x) - 1; i >= 0; i-- {

		diff := U(x[i], utility, t) - B(x[i], m, p)
		prev_diff := U(x[i]-k, utility, t) - B(x[i]-k, m, p)

		if diff < max_f {

			max_f = math.Abs(diff)
			max_x = x[i]

			if math.Abs(diff) <= math.Abs(prev_diff) {
				break
			}
		}
	}

	bds := []float64{min_x, max_x}
	sort.Float64s(bds)
	return bds
}

// to bring it all together, assign each variable to their initiated selves and
// iterate until the lower bound and upper bound converge to a single value

func main() {
	start := time.Now()

	k = .001
	m = 100

	t[0], t[1] = .3, .7
	p[0], p[1] = 3, 2

	s := arange(0, m/p[0], .001)
	u = math.Pow(.5*(m/p[0]), t[0]) * math.Pow(.5*(m/p[1]), t[1])

	var bounds []float64
	bounds = findIntersection(s, u)

	for bounds[1]-bounds[0] > k {

		// find an average between the bounds and calibrate a new equivalence
		// class; then define new bounds based on the new curve

		u = adjust(bounds[0], bounds[1])
		bounds = findIntersection(s, u)
	}

	bundle := []float64{bounds[0], B(bounds[0], m, p)}

	for i := 0; i < len(bundle); i++ {
		fmt.Printf("%.3f\t", bundle[i])
	}

	elapsed := time.Since(start)
	log.Printf("\ntime: %dms", elapsed.Microseconds()/1000)
}
