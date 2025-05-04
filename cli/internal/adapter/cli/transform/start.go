package transform

import "cli/internal/domain/entity"

func ChapterToDomain(chapter string) (entity.Chapter, error) {
	switch chapter {
	case "chapter3":
		return entity.Chapter3, nil
	case "chapter5":
		return entity.Chapter5, nil
	}

	return entity.Chapter1, nil
}
