# Sample Template

This is a sample template demonstrating the hierarchical file structure for report, export, and graph configurations.

## File Structure

### Report Structure
```
report/
├── <category>.json          # Category metadata
└── <category>/
    └── <action>.json        # Action with properties
```

**Example:**
- `report/maintenance.json` - Maintenance category
- `report/maintenance/inspection.json` - Inspection action
- `report/maintenance/repair.json` - Repair action
- `report/incidents.json` - Incidents category
- `report/incidents/accident.json` - Accident action

### Export Structure
```
export/
├── <parent>.json            # Parent export node
└── <parent>/
    └── <child>.json         # Child export node
```

**Example:**
- `export/total-inspections.json` - Parent node
- `export/total-inspections/ok-inspections.json` - Child node
- `export/total-inspections/critical-inspections.json` - Child node
- `export/total-repairs.json` - Parent node
- `export/total-repairs/repair-hours.json` - Child node

### Graph Structure
```
graph/
├── <graph>.json             # Top-level graph
└── <graph>/
    └── <child-graph>.json   # Nested graph
```

**Example:**
- `graph/inspection-status-overview.json` - Standalone graph
- `graph/repair-activity.json` - Parent graph
- `graph/repair-activity/repair-hours-trend.json` - Child graph
- `graph/incident-severity.json` - Standalone graph

## Loading Logic

The template loader should:

1. **Reports**:
   - Load all `report/*.json` files as categories
   - For each category, load `report/<category-id>/*.json` files as actions
   - Actions contain their properties inline

2. **Exports**:
   - Load all `export/*.json` files as top-level nodes
   - For each node, recursively load `export/<node-id>/*.json` as children
   - Build the hierarchical tree structure

3. **Graphs**:
   - Load all `graph/*.json` files as top-level graphs
   - For each graph, recursively load `graph/<graph-id>/*.json` as children
   - Build the hierarchical graph structure

## Content Details

### Report Categories & Actions
- **Maintenance**: Inspection (status, photos, notes) and Repair (type, duration, location)
- **Incidents**: Accident (severity, media, people count)

### Export Nodes
- Total Inspections (with OK/Critical breakdown)
- Total Repairs (with repair hours)
- Incidents (with severity and people affected)
- Efficiency Score

### Graphs
- Inspection Status Overview (bar chart)
- Repair Activity (line chart with nested hours trend)
- Incident Severity Distribution (pie chart)
- Maintenance Per Object (per-object bar chart)

## Internationalization

All user-facing text uses `TranslatedText` format with support for:
- English (default)
- Norwegian Bokmål (nb)
- German (de)

## Validation

### Local Validation

Run the validation script to check the structure and schema of all template files:

```bash
python validate_structure.py .
```

The validator checks:
- JSON syntax and structure
- Required fields for each file type
- Valid property types and configurations
- TranslatedText format consistency
- ID uniqueness within files
- Formula and data series validity
- File organization and hierarchy

### Continuous Integration

A GitHub Actions workflow automatically validates the template structure on every push and pull request. The workflow runs:

1. JSON syntax validation for all `.json` files
2. Schema validation using `validate_structure.py`

See [.github/workflows/validate.yml](.github/workflows/validate.yml) for details.

### Supported Property Types

- `text` - Text input
- `number` - Numeric input (with optional min, max, step)
- `boolean` - True/false toggle
- `dropdown` - Single selection from options
- `radio` - Radio button selection
- `checkbox` - Multiple selection checkboxes
- `media` - Photo/video capture (with mode and sources)
- `image` - Image upload
- `date` - Date picker
- `time` - Time picker
- `datetime` - Date and time picker
- `location` - Location/GPS coordinates

## Usage

This structure allows for:
- Easy version control (each entity is a separate file)
- Partial template loading (load specific categories/actions)
- Clear parent-child relationships via folder structure
- Scalability for large templates
- Automated validation to catch errors early
