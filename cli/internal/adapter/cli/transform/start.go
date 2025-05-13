package transform

import "cli/internal/domain/entity"

func ChapterToDomain(chapter string) (entity.Chapter, error) {
	switch chapter {
	case "chapter3":
		return entity.Chapter3, nil
	case "chapter5":
		return entity.Chapter5, nil
	case "chapter1":
		return entity.Chapter1, nil
	case "chapter2":
		return entity.Chapter2, nil
	case "chapter4":
		return entity.Chapter4, nil
	case "chapter6":
		return entity.Chapter6, nil
	case "chapter7":
		return entity.Chapter7, nil
	case "chapter8":
		return entity.Chapter8, nil
	case "chapter9":
		return entity.Chapter9, nil
	case "chapter10":
		return entity.Chapter10, nil
	}

	return entity.Chapter1, nil
}
