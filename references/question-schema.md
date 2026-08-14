# Question bank schema

Use a JSON object with bank metadata and a `questions` array. A flat array is acceptable when integrating with an existing project, but retain equivalent fields.

```json
{
  "name": "题库名称",
  "version": 1,
  "questions": [
    {
      "id": "official-187-001",
      "kind": "multiple_choice",
      "sourceType": "official",
      "sourceBank": "官方模拟题 187",
      "sourceRefs": [{"file": "source.pdf", "page": 4, "number": "1"}],
      "domain": "客户咨询与评估",
      "originalSection": "Chapter 1",
      "stem": "题干",
      "options": [{"label": "A", "text": "选项"}],
      "answer": "A",
      "explanation": "解析或空字符串",
      "confidence": "high",
      "reviewNote": ""
    }
  ]
}
```

## Required invariants

- `id` is unique and stable across updates.
- `kind` is `multiple_choice` or `recall`.
- `sourceType` is `official`, `recalled`, or `user_authored`.
- `sourceRefs` contains at least one traceable source.
- `stem` is non-empty.
- Multiple-choice questions have at least two options and an answer matching an option label.
- Recall questions use `answerText` instead of `options` and `answer`.
- `confidence` is `high`, `medium`, or `verify`.

## Deduplication record

When auditability matters, add `mergedFrom` with prior IDs or source-local identifiers. Never discard source citations during a merge.
