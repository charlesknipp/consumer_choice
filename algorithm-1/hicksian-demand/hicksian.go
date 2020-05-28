package main

import (
	"fmt"
	"math"
	"time"
)

var m, k, u float64
var t [2]float64
var p [2]float64

var income float64

// define the two intersecting curves:
func B(x1, income float64) float64 {
	x2 := (income - (p[0] * x1)) / p[1]
	return x2
}

func U(x1, utility float64) float64 {
	x2 := math.Pow((utility / math.Pow(x1, t[0])), (1 / t[1]))
	return x2
}

// now define the intersection closest to 0:
func findMin(x []float64, step, income float64) float64 {
	pos := len(x)
	min_f := U(x[0], u) - B(x[0], income)
	min_x := x[0]

	for i := 0; i < pos; i++ {

		diff := U(x[i], u) - B(x[i], income)
		next_diff := U(x[i]+step, u) - B(x[i]+step, income)
		// fmt.Printf("%.3f\t%.5f\t%.5f\n", x[i], diff, next_diff)

		if diff < min_f {

			min_f = math.Abs(diff)
			min_x = x[i] - step

			if math.Abs(diff) <= math.Abs(next_diff) {
				break
			}
		}
	}

	// fmt.Printf("\nmin\t%.5f\n", min_x)
	return min_x
}

// now define the intersection closest to +INF:
func findMax(x []float64, step, income float64) float64 {
	pos := len(x) - 1
	max_f := U(x[pos], u) - B(x[pos], income)
	max_x := x[pos]

	for i := pos; i >= 0; i-- {

		diff := U(x[i], u) - B(x[i], income)
		prev_diff := U(x[i]-step, u) - B(x[i]-step, income)
		// fmt.Printf("%.3f\t%.3f\t%.3f\n", x[i], diff, prev_diff)

		if diff < max_f {

			max_f = math.Abs(diff)
			max_x = x[i] - step

			if math.Abs(diff) <= math.Abs(prev_diff) {
				break
			}
		}
	}

	// fmt.Printf("\n=> max\t%.3f\n\n", max_x)
	return max_x
}

func findIntersection(income float64) []float64 {

	n := 4
	x := make([]float64, int(math.Floor(m/p[0])))

	for i := range x {
		x[i] = float64(1 + i)
	}

	// fmt.Println(x)

	min_x := make([]float64, n+1)
	min_x[0] = findMin(x, 1, income)

	max_x := make([]float64, n+1)
	max_x[0] = findMax(x, 1, income)

	for i := 1; i < n+1; i++ {

		k := math.Pow(10, float64(i))

		mnx := make([]float64, 20)
		mxx := make([]float64, 20)

		for j := 0; j < 20; j++ {

			mn := min_x[i-1] + (float64(j) / k)
			mx := max_x[i-1] + (float64(j) / k)

			round_mn := math.Round(mn*k) / k
			round_mx := math.Round(mx*k) / k

			mnx[j] = round_mn
			mxx[j] = round_mx
		}

		min_x[i] = findMin(mnx, 1/k, income)
		max_x[i] = findMax(mxx, 1/k, income)
	}

	final_min := min_x[n]
	final_max := max_x[n]

	bds := []float64{final_min, final_max}
	return bds
}

// define the adjustment to a new curve
func adjust(lx, ux float64) float64 {

	x1 := (lx + ux) / 2
	x2 := U(x1, u)

	m := x1*p[0] + x2*p[1]

	return m
}

func main() {
	start := time.Now()

	k = .001
	u = 24.03519395349548

	t[0], t[1] = .3, .7
	p[0], p[1] = 3, 2

	m = math.Pow(u, (1/(t[0]+t[1])))*p[0] + math.Pow(u, (1/(t[0]+t[1])))*p[1]

	// fmt.Print("\n")
	// fmt.Println(findIntersection(m))

	var bounds []float64
	bounds = findIntersection(m)

	for bounds[1]-bounds[0] > k {
		m = adjust(bounds[0], bounds[1])
		bounds = findIntersection(m)
	}

	bundle := []float64{bounds[0], B(bounds[0], m)}
	elapsed := time.Since(start)

	for i := 0; i < len(bundle); i++ {
		fmt.Printf("%.3f\t", bundle[i])
	}

	fmt.Printf("\ntime: %s", elapsed)
}
