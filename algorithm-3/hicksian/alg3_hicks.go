package main

import (
	"fmt"
	"math"
	"sort"
)

var u float64
var t [2]float64
var p [2]float64

func e(x1, x2 float64) float64 {
	return x1*p[0] + x2*p[1]
}

func I(x1 float64) float64 {
	return math.Pow((u / math.Pow(x1, t[0])), (1 / t[1]))
}

// allows me to sort through a map as an ordered object
type kv struct {
	key float64
	val float64
}

func main() {
	var x1, x2 float64

	t[0], t[1] = .3, .7
	p[0], p[1] = 3, 2

	u = 24.035193953495487

	// monotonicity/convexity implies x1 is not bounded on an equivalence class
	m := p[0]*math.Pow(u, 1/(t[0]+t[1])) + p[1]*math.Pow(u, 1/(t[0]+t[1]))

	dnsty := int(math.Ceil((m / p[0]) * 1000))
	marshallian_set := make(map[float64]float64)

	for i := 1; i < int(dnsty); i++ {
		x1 = float64(i) / 1000
		x2 = I(x1)
		marshallian_set[x1] = e(x1, x2)
	}

	var md []kv
	for k, v := range marshallian_set {
		md = append(md, kv{k, v})
	}

	sort.Slice(md, func(i, j int) bool {
		return md[i].val < md[j].val
	})

	fmt.Println(md[0])
}
