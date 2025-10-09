# Branch Protection Configuration

After this PR is merged, configure branch protection for `main` to ensure code quality and prevent direct pushes.

## Steps to Configure

1. Go to your repository on GitHub
2. Navigate to **Settings** > **Branches**
3. Click **Add rule** (or edit existing rule for `main`)
4. Configure the following settings:

### Branch Name Pattern
```
main
```

### Protection Rules

#### ✅ Require a pull request before merging
- [x] Require approvals: **1** (adjust based on team size)
- [x] Dismiss stale pull request approvals when new commits are pushed
- [x] Require review from Code Owners (optional, if you have CODEOWNERS file)

#### ✅ Require status checks to pass before merging
- [x] Require branches to be up to date before merging
- **Required status checks**:
  - `validate`
  - `integration`
  - `contract_check`

#### ✅ Require conversation resolution before merging
- [x] All conversations must be resolved

#### ✅ Do not allow bypassing the above settings
- [x] Include administrators (recommended for strict enforcement)

#### ✅ Restrict who can push to matching branches
- [x] Restrict pushes that create matching branches
- Add specific users/teams who can push directly (typically only for emergency fixes)

### Additional Recommended Settings

#### Lock branch
- [ ] Make the branch read-only (only use if you want to completely prevent all direct pushes)

#### Allow force pushes
- [ ] **Do NOT enable** - Force pushes can break history

#### Allow deletions
- [ ] **Do NOT enable** - Prevents accidental branch deletion

## Testing the Configuration

After setting up branch protection:

1. Try to push directly to `main` - it should be rejected
2. Create a test PR and verify that:
   - All three CI jobs (`validate`, `integration`, `contract_check`) must pass
   - The merge button is disabled until checks pass
   - Reviews are required before merging

## Troubleshooting

### Status checks not appearing
- Ensure the workflow has run at least once on a PR
- Check that the job names in the workflow match exactly: `validate`, `integration`, `contract_check`

### Can't merge after checks pass
- Verify branch is up to date with `main`
- Check that required approvals are provided
- Ensure all conversations are resolved

## Emergency Procedures

If you need to bypass branch protection temporarily:

1. **Preferred**: Use the "Allow bypass" setting to grant temporary access
2. **Last resort**: Temporarily disable the rule, make the change, re-enable immediately

Document all bypass actions and the reason for the emergency.
