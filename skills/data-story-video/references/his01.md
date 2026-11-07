# HIS01 reference composition

The reference answers one question using related charts, rather than attaching an unrelated anecdote to each chart. It is a reusable style, not a claim about the new user's development history.

|Segment|Reference duration|Purpose|
|---|---:|---|
|Opening|3 seconds|One question and the sequence to follow|
|Example before each chart|5 seconds|Familiar analogy and technical definition|
|Each moving chart|12 seconds|Actual measured changes; two 6-second explanations below|
|Ending|5 seconds|A grounded takeaway with the correct interpretation|

Four chapters take 76 seconds. The included one-chapter synthetic demo takes 25 seconds. Set `timing` in episode.json to change the pace; allow enough time to read. The reference's chart sequence was code growth → folder appearance → commit types → test code share. Those are possible subjects, not universal requirements.

- 1080×1350, 30fps, silent H.264/yuv420p.
- Background #10181c; body #f4f1e8; secondary #97a6a9; accent #fb744c.
- Header identifies episode and chapter, middle holds the moving data, lower area explains the current scene and its source.
- Dates, categories, denominators and caveats survive animation and cropping.
- Familiar examples are marked as analogies, never invented personal history.

No original private project, historical CSV, local home path, or original video is required. See `assets/his01-starter/episode.json` for a runnable, explicitly synthetic example, and rendering.md for the full workflow.
