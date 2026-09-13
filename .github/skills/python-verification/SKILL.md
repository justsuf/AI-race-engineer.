---
name: python-verification
description: "Use when debugging Python code, reproducing a bug, tracing a root cause, fixing a regression, or validating a change with the smallest relevant test or command. Best for code issues in this repository and similar Python projects."
---

# Python Verification and Debugging

Use this skill to fix real bugs in Python code without guessing. It is optimized for small, evidence-driven changes and for validating results with the narrowest relevant command.

## Workflow

### 1. Define the symptom clearly
- Confirm the actual failure mode, error message, and expected behavior.
- Identify the specific file, function, or module involved.
- Check whether the issue is reproducible and whether it is a logic bug, environment problem, or configuration issue.

Decision point:
- If the failure is not reproduced, stop and gather the exact command, input, or stack trace before making any code change.
- If the failure is reproduced, continue with the smallest possible investigation.

### 2. Trace the root cause before patching
- Read the relevant code path and inspect the variables, control flow, or contracts involved.
- Follow the data flow from the trigger to the failing behavior.
- Prefer direct evidence from code, runtime output, stack traces, or diagnostics over assumptions.

Decision point:
- If the issue appears to be an environment mismatch, verify the selected Python interpreter and runtime dependencies before changing code.
- If it is a code logic issue, isolate the exact faulty condition, calculation, or API contract.

### 3. Add or run a focused failing check
- Write a minimal failing check or reproduction when practical.
- Prefer a targeted script, unit test, or runtime probe over broad project-wide validation.
- Keep the reproduction narrow enough to validate the specific behavior under investigation.

Decision point:
- If a test already exists and fails, use it as the ground truth and keep the fix narrow.
- If no check exists, create the smallest possible reproduction to validate the fix.

### 4. Apply the smallest correct fix
- Change only the code necessary to address the root cause.
- Avoid broad cleanup, refactors, or unrelated edits while debugging.
- Keep the fix aligned with the actual contract, data model, and surrounding code patterns.

Decision point:
- If a fix is speculative, stop and gather one missing fact before editing.
- If the bug is caused by a shared pattern, apply the fix only where the root cause occurs.

### 5. Verify with the narrowest relevant command
- Run the smallest command that checks the changed behavior.
- Prefer a focused test, script, or direct invocation over a full suite when a targeted check is sufficient.
- Check exit status and the actual output before claiming success.

Decision point:
- If the targeted verification passes, consider one nearby regression check only if the change might affect adjacent behavior.
- If the verification fails, return to the root cause step and refine the fix.

### 6. Summarize evidence and scope
- Report what was fixed, what was verified, and what command proved it.
- Note any residual risk or follow-up work explicitly.
- Keep the summary factual and tied to observed results.

## Quality criteria
A task is complete only when all of the following are true:
- The actual root cause has been identified and addressed.
- The change is minimal and limited to the relevant behavior.
- A relevant verification command was run and the output supports the fix.
- The result is reported with concrete evidence, not confidence alone.

## Branching guidance
- Bug is reproducible but unclear: collect the exact error output and narrow to the failing function.
- Bug is environment-related: validate interpreter, dependency, and config setup before editing code.
- Bug is not reproducible: gather more runtime context instead of patching blindly.
- Fix touches shared logic: validate adjacent scenarios that exercise the same contract.

## Completion checklist
- [ ] Symptom and expected behavior are clear.
- [ ] Root cause was traced to actual code or runtime evidence.
- [ ] A minimal failing check or reproduction was used when practical.
- [ ] The fix is minimal and directly addresses the root cause.
- [ ] A focused verification command was run successfully.
- [ ] The final status is reported with evidence.
