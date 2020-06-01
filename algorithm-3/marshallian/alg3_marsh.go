package main

import (
	"fmt"
	"math"
	"sort"
)

var m float64
var t [2]float64
var p [2]float64

func u(x1, x2 float64) float64 {
	return math.Pow(x1, t[0]) * math.Pow(x2, t[1])
}

func B(x1 float64) float64 {
	return (m - (p[0] * x1)) / p[1]
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

	m = 100

	dnsty := int(math.Ceil((m / p[0]) * 1000))
	marshallian_set := make(map[float64]float64)

	for i := 1; i < int(dnsty); i++ {
		x1 = float64(i) / 1000
		x2 = B(x1)
		marshallian_set[x1] = u(x1, x2)
	}

	var md []kv
	for k, v := range marshallian_set {
		md = append(md, kv{k, v})
	}

	sort.Slice(md, func(i, j int) bool {
		return md[i].val > md[j].val
	})

	fmt.Println(md[0])
}
