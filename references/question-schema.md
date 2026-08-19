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
      "table": {
        "headers": ["项目", "训练前", "训练后"],
        "rows": [
          ["体重", "130 lb（59 kg）", "124 lb（56 kg）"],
          ["身体脂肪", "30%", "25%"]
        ]
      },
      "media": [{"type": "gif", "file": "exercise-01.gif", "alt": "动作演示"}],
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
- Options may originate on one source line; their source layout does not change the multiple-choice kind.
- Recall questions use `answerText` instead of `options` and `answer`.
- `confidence` is `high`, `medium`, or `verify`.
- `table`, when present, keeps source headers and rows as separate cells. Every row has the same number of cells as `headers`; keep units inside their corresponding cells.
- `media`, when present, contains a verified `type`, durable `file` or URL, and accessible `alt` text. Keep the cited source filename when it differs from the stored filename.

## Deduplication record

When auditability matters, add `mergedFrom` with prior IDs or source-local identifiers. Never discard source citations during a merge.

## Learning-state schema

Keep user-specific state separate from the question dataset so content updates do not overwrite study history. A practical record is keyed by authenticated user and stable question ID:

```json
{
  "userId": "account-id",
  "questionId": "official-187-001",
  "selectedAnswer": "B",
  "isCorrect": false,
  "isUncertain": true,
  "note": "复习心率控制模式",
  "updatedAt": "ISO-8601 timestamp"
}
```

Store resume positions separately by user and practice context, for example `bank:official-187` or `domain:nutrition`. Wrong-answer review uses its own context and must not write the source bank's resume position.
