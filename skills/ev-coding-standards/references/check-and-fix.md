# Check And Fix

## Check

- Load `ev-code-review` and use its complete scope, selection, evidence, and coverage contracts.
- Honor explicit files, repository scope, commits, branch baseline, or PR. Otherwise inspect staged,
  unstaged, and untracked non-ignored changes. A clean tree means no changes, not the latest commit.
- Record the standards revision/dirty state and exact applied paths. Keep inspection read-only;
  discover non-writing checks from project scripts/CI. Report unavailable checks as gaps.
- Use the existing coverage validator when practical; its success validates completeness, not truth.

## Fix

1. Establish the same scope/baseline and read full applicable rules before editing. Review it first;
   fix only evidenced violations in requested scope. Existing user changes are not disposable.
2. Apply the smallest consistent correction, including affected callers/imports/contracts/tests.
   Preserve exceptions, public behavior, and security controls. Resolve ambiguous policy intent before
   affected edits; API pagination implementation still requires the user's choice.
3. Run relevant checks. Formatter write modes are allowed only for requested fix scope; otherwise
   preserve the review's non-writing checks. Recheck the resulting diff against the original baseline.
4. Return fixed and remaining findings, checks/evidence, and gaps. Do not claim compliance when a
   check could not run. Do not stage, commit, discard, or publish application changes.
