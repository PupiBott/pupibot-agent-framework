# OpenAPI Snapshot Policy

This document describes the policy and procedures for managing OpenAPI contract snapshots in the CI/CD pipeline.

## Snapshot Location

The OpenAPI snapshot is stored at:
- **File**: `openapi.snapshot.json` (repository root)

The current OpenAPI spec is generated during CI runs and compared against this snapshot.

## When to Update the Snapshot

Update `openapi.snapshot.json` when:

1. **Intentional API Changes**: You've made deliberate changes to the API endpoints, request/response schemas, or other OpenAPI specifications
2. **New Features**: Adding new endpoints or extending existing ones
3. **Breaking Changes**: Modifying existing endpoints (coordinate with API consumers first)
4. **Schema Updates**: Changes to request/response models or validation rules

## Update Procedure

### 1. Generate the Current Spec

Run the following command to generate the current OpenAPI specification:

```bash
python -c "import json, pathlib; \
from services.agent_runner.src.main import app; \
current_spec = app.openapi(); \
pathlib.Path('openapi.current.json').write_text(\
json.dumps(current_spec, indent=2), encoding='utf-8')"
```

### 2. Review the Diff

Compare the current spec with the snapshot to understand what changed:

```bash
diff openapi.snapshot.json openapi.current.json
```

Or use a more readable diff tool:

```bash
git diff --no-index openapi.snapshot.json openapi.current.json
```

### 3. Update the Snapshot

If the changes are intentional and correct:

```bash
cp openapi.current.json openapi.snapshot.json
git add openapi.snapshot.json
git commit -m "chore: update OpenAPI snapshot for [reason]"
```

### 4. Document the Change

In your PR description, explain:
- What API changes were made
- Why the changes were necessary
- Impact on API consumers
- Whether this is a breaking change

## Artifact Retention

- **Current Specs**: Uploaded as CI artifacts with name `openapi-current-{run_id}`
- **Retention Period**: 30 days
- **Purpose**: Allow comparison and rollback if needed

## Contract Check Failures

If the `contract_check` job fails:

1. **Review the diff** in the CI logs to understand what changed
2. **Verify if the change was intentional**:
   - If YES: Update the snapshot following the procedure above
   - If NO: Fix your code to match the expected contract
3. **For unintentional changes**: This usually indicates an accidental breaking change that should be fixed

## Automation

The CI pipeline automatically:
- Generates the current OpenAPI spec
- Compares it with the snapshot
- Uploads the current spec as an artifact (retained for 30 days)
- Fails if there are differences (preventing accidental API changes)

## Best Practices

1. **Review diffs carefully** before updating snapshots
2. **Coordinate breaking changes** with API consumers
3. **Version your API** when making breaking changes
4. **Document changes** in PR descriptions and release notes
5. **Keep snapshots in sync** - don't commit changes without updating the snapshot if APIs changed
