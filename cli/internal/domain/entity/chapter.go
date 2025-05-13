package entity

type Chapter int
type SubChapter int

const (
	Chapter1 Chapter = iota + 1
	Chapter2
	Chapter3
	Chapter4
	Chapter5
	Chapter6
	Chapter7
	Chapter8
	Chapter9
	Chapter10
)

const (
	SubChapter1 SubChapter = iota + 1
	SubChapter2
	SubChapter3
	SubChapter4
	SubChapter5
)
