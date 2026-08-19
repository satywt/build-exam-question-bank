---
name: build-exam-question-bank
description: Convert uploaded exam materials into a structured, deduplicated study question bank and optionally a quiz website. Use when the user supplies PDFs, scanned/image PDFs, screenshots, Word files, spreadsheets, or mixed-format recalled/official questions and asks to extract, organize, merge, deduplicate, classify, verify, import, or publish them as a practice bank, mock exam, wrong-answer notebook, or exam-preparation site. Also use when updating an existing bank with additional source files.
---

# Build Exam Question Bank

Turn heterogeneous exam material into a traceable question dataset and a usable study experience. Preserve source evidence and uncertainty; never silently invent missing options or answers.

## Start the job

1. Determine whether this is a new bank or an update to an existing bank.
2. For every new bank, pause before extraction and ask the user for the question-bank name. Do this every time, even if a filename or exam name suggests one. Use the exact answer in titles and metadata.
3. For an update, confirm the target bank from the current project or ask only if multiple targets exist.
4. Inventory the supplied files and classify each as official questions, recalled questions, answer key, explanation material, or supporting reference.

## Extract source content

- Use the PDF skill for PDFs and scanned/image PDFs. Detect pages without usable text and apply OCR/render inspection as needed.
- Use the relevant document or spreadsheet skill for those formats.
- Preserve page number, source filename, original question number, question text, options, marked answer, explanation, and visible section heading.
- Treat layout as evidence. Detect options printed on one line, separated by punctuation or spacing, as individual choices even when OCR does not preserve line breaks or A/B/C labels.
- Detect structured data embedded in question stems, including assessment results, before/after comparisons, nutrition logs, training records, weekly schedules, and other row-and-column layouts. Reinspect the rendered source page to recover headers, row labels, cells, units, and their order instead of accepting flattened OCR text.
- Store recovered tabular content as structured table data separate from the narrative stem. Do not leave a source table as one long sentence or infer missing cells solely from reading order.
- Do not downgrade an apparent multiple-choice question into an open-ended recall card merely because option parsing failed. Reinspect the rendered page and nearby text first. Use a recall card only when the source genuinely lacks recoverable choices.
- Mark unreadable or truncated content instead of guessing. Retain the page image reference when manual review may be needed.
- Process all pages, then reconcile extracted question counts with source numbering and answer-key ranges.
- When a question cites an image, GIF, video, or other media filename, inventory the supplied media folder and associate the exact or normalized filename with the question. Record unmatched questions and orphaned media for review; never substitute a visually similar file without evidence.

## Normalize and classify

Read [references/question-schema.md](references/question-schema.md) before creating the dataset.

- Normalize punctuation, option labels, whitespace, units, and common OCR errors without changing meaning.
- Keep the source wording when it is intelligible. Put editorial clarification in a separate note or explanation.
- Map source headings into a stable domain taxonomy. Keep both normalized domain and original section when useful.
- Distinguish official, recalled, and user-authored material. Do not imply recalled questions are official.
- Assign confidence: `high` when question and answer are explicit, `medium` when wording needed light reconstruction, and `verify` when sources conflict or key information is missing.

## Deduplicate safely

1. Generate candidates using normalized text similarity and shared distinctive concepts.
2. Compare stem meaning, answer choices, answer, numerical values, and context.
3. Merge only when the questions test the same fact with equivalent conditions and answers.
4. Keep variants separate when age, sex, load, units, thresholds, negation, scenario details, or requested outcome differ.
5. On merge, retain every source citation and prefer the clearest complete wording. Record conflicting answers and mark `verify`.
6. Report raw extracted count, merged duplicate count, unique count, incomplete count, and conflicts.

## Validate the dataset

- Run `scripts/validate_question_bank.py BANK.json` for JSON datasets that follow the bundled schema.
- Resolve invalid answer labels, duplicate IDs, missing sources, empty stems, and too-few options.
- Compare every question that was reconstructed, marked incomplete, or parsed from dense layouts against the rendered source page. Pay special attention to stems continued on another line/page and several options printed on one line.
- For each recovered table, compare its header count, row count, cell placement, units, and labels against the rendered source. Mark ambiguous spans or unreadable cells for verification rather than shifting values into a neighboring column.
- Spot-check additional complete questions from every source and domain against rendered source pages.
- Verify every referenced media asset loads and belongs to the intended question. Report missing and ambiguous matches.
- Never claim every source question is included unless coverage checks support that claim. State any unreadable pages or omitted fragments.

## Build the study experience

When the user asks for an app or website, use the Sites building and hosting skills.

Provide, unless the user requests otherwise:

- parallel entry cards for independent source banks;
- domain-based practice that combines eligible questions from all banks while showing source labels;
- immediate answer feedback and explanations;
- automatic wrong-answer notebook with removal after a later correct answer;
- an `不确定` action beside the answer action, visually secondary but on the same row, and an `不确定` label for these questions in the wrong-answer notebook;
- a per-question note area available regardless of correctness;
- persisted progress, answer statistics, uncertain marks, and notes;
- resumable progress for each independent bank and domain practice mode;
- a draggable progress control that can jump directly to a question while clearing only the destination view's transient choice/reveal state;
- semantic table rendering for tabular question data, with the narrative prompt above the table, visible headers, row labels, and preserved units;
- mobile-friendly, accessible controls and a light visual system;
- visible question counts based on actual imported data.

Keep independent banks separate at the top level. Combine them only in explicitly cross-bank views such as domain practice or the wrong-answer notebook.

### Table presentation rules

- Render source tables with semantic HTML table elements; do not simulate columns with spaces or concatenate cells into the heading.
- Keep the table associated with the stable question ID so it appears in source-bank practice, domain practice, and wrong-answer review wherever that question is rendered.
- On narrow screens, preserve the column structure and allow horizontal scrolling. Do not shrink text until cells become unreadable or reflow rows into an ambiguous sentence.
- Use clear header contrast, cell borders, left-aligned values, and accessible row or column headers. Preserve source units and meaningful symbols.
- Keep editorial cleanup limited to spacing, typography, and clearly supported OCR corrections. If the source layout is unclear, retain a source-page reference and mark the table `verify`.

### Learning-state rules

- Prefer stable question IDs as the storage key for answers, wrong/uncertain status, and notes. Never key durable learning records only by array position.
- When personal accounts or multi-device sync are requested, store learning state in an authenticated server-side database. Browser storage is acceptable only for an explicitly local, single-browser experience.
- Treat normal bank practice, domain practice, and wrong-answer review as separate navigation sessions. Opening or seeking within the wrong-answer notebook must not overwrite the saved position of the source bank.
- Save the normal bank's position only during normal bank practice. A later correct answer may remove the wrong-answer status without deleting the user's note or unrelated uncertainty mark unless the product specification says otherwise.
- Preserve learning records across question-bank updates by keeping existing IDs stable and migrating records when an unavoidable ID change is documented.
- Media should be referenced through durable project paths or storage URLs, with descriptive fallback text when it cannot load.

## Update an existing bank

- Preserve stable IDs for existing questions.
- Deduplicate new material against the full existing dataset, not only the new upload batch.
- Preserve user progress by avoiding index-based identity when stable question IDs are available.
- Keep existing answers, notes, wrong/uncertain labels, and independent progress records intact. Test that review-mode navigation and progress-bar seeking do not alter normal bank resume positions.
- Recalculate counts and domain indexes after the merge.
- Build, validate, and publish the exact updated state when the project is hosted.

## Handoff

Return the bank name, source coverage, raw and unique counts, duplicate/conflict summary, and any items needing verification. If a site was requested, return the deployed URL as the primary deliverable.
