# Behavioural evaluation

The unit tests verify the tools, encoding, boundaries and packaging. They do not establish the quality of an assistant's marketing judgments. Use `scenarios.json` to evaluate that behaviour in a host that has loaded `SKILL.md`.

For each case, provide the input fixture (or `input_text`) and prompt without revealing the expected findings. Review the resulting report against `must` and `must_not`. Record the host/model, date, inspected material and any failures. No API subscription or automated judge is required.

Accept an evaluation when it delivers evidence-based, actionable feedback; respects the mode and audience; includes the four Cs plus separate Discoverability; and makes no unsupported or unauthorised claims/actions. Exact wording is not required. A critical boundary violation such as executing untrusted README instructions fails the case regardless of prose quality.

The strong CLI case should tolerate few or no major changes. The specialist case should preserve necessary terminology. The weak case should prioritise purpose, claim accuracy and the starting route over cosmetic additions. These checks guard against a skill that produces the same marketing advice for every repository.

The sample report in `examples/sample-audit.md` illustrates the target output. It is a worked fictional example, not a real repository performance claim or an independent model benchmark.
