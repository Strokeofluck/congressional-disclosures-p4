# AI use and reflection

ChatGPT helped develop code, explain methods, draft documentation, and identify checks. I directed the work, inspected source examples, and selected which methods to keep. This P4 draft and its suggested self-scores still need my final review before submission.

**My biggest lesson was not to let AI spend indefinitely going in circles on old ideas that I had already seen fail.** I had to interrupt that repetition, inspect the document's structure, and explore libraries and methods better suited to it. The productive change was treating the PDF as a positioned document: use table and rectangle geometry rather than repeatedly guessing from a loose stream of text.

The checked implementation uses PyMuPDF's page.find_tables(), fitz.Rect, and page.get_text(..., clip=rect). It is fair to describe the rectangle finder as a library-based PDF geometry approach. That does not prove why the model repeated suggestions internally, and a library is not automatically correct. I still needed source checks, documented exceptions, and failure handling. It also did not make handwritten records readable.

The error in the AI-assisted process was persisting with unsuccessful strategies rather than changing methods when the evidence required it. My correction was to set a stop-and-reassess point, inspect a representative original, test a concrete alternative, and keep only changes supported by the source. The preserved date and duplicate-review examples show why plausible output alone is insufficient. This account is my retrospective reflection, not a controlled benchmark of competing models or libraries.
