#!/usr/bin/env python3
"""
Template Structure Validator

Validates the hierarchical JSON template structure for reports, exports, and graphs.
Ensures proper file organization, schema compliance, and reference integrity.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional, Union
from collections import defaultdict


class TemplateValidator:
    """Validates template structure and content."""

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.valid_types = {
            'text', 'number', 'boolean', 'dropdown', 'radio', 'checkbox',
            'media', 'image', 'date', 'time', 'datetime', 'location'
        }
        self.valid_languages = {'nb', 'de', 'en', 'it', 'ro'}
        self.categories: Dict[str, Dict] = {}
        self.actions: Dict[str, Dict[str, Dict]] = {}

    def error(self, file_path: str, message: str):
        """Add an error message."""
        self.errors.append(f"❌ {file_path}: {message}")

    def warning(self, file_path: str, message: str):
        """Add a warning message."""
        self.warnings.append(f"⚠️  {file_path}: {message}")

    def load_json(self, file_path: Path) -> Tuple[Optional[Dict[str, Any]], str]:
        """Load and parse JSON file."""
        rel_path = file_path.relative_to(self.templates_dir)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f), str(rel_path)
        except json.JSONDecodeError as e:
            self.error(str(rel_path), f"Invalid JSON: {e}")
            return None, str(rel_path)
        except Exception as e:
            self.error(str(rel_path), f"Failed to read file: {e}")
            return None, str(rel_path)

    def validate_translated_text(self, data: Any, field_name: str, file_path: str, required: bool = True) -> bool:
        """Validate TranslatedText structure."""
        if data is None:
            if required:
                self.error(file_path, f"Missing required field '{field_name}'")
                return False
            return True

        if isinstance(data, str):
            # Simple string is valid
            return True

        if not isinstance(data, dict):
            self.error(file_path, f"'{field_name}' must be string or object")
            return False

        if 'default' not in data:
            self.error(file_path, f"'{field_name}' object must have 'default' field")
            return False

        if not isinstance(data['default'], str):
            self.error(file_path, f"'{field_name}.default' must be a string")
            return False

        if 'translations' in data:
            if not isinstance(data['translations'], dict):
                self.error(file_path, f"'{field_name}.translations' must be an object")
                return False
            for lang, text in data['translations'].items():
                if lang not in self.valid_languages:
                    self.warning(file_path, f"Unknown language code '{lang}' in {field_name}")
                if not isinstance(text, str):
                    self.error(file_path, f"Translation for '{lang}' must be a string")
                    return False
        return True

    def validate_object_schema(self, file_path: Path):
        """Validate object.json schema."""
        data, rel_path = self.load_json(file_path)
        if data is None:
            return

        # object.json should be a flat object with property definitions
        if not isinstance(data, dict):
            self.error(rel_path, "Must be a JSON object")
            return

        for prop_id, prop_def in data.items():
            if not isinstance(prop_def, dict):
                self.error(rel_path, f"Property '{prop_id}' must be an object")
                continue

            if 'type' not in prop_def:
                self.error(rel_path, f"Property '{prop_id}' missing 'type' field")
                continue

            if prop_def['type'] not in self.valid_types:
                self.error(rel_path, f"Property '{prop_id}' has invalid type '{prop_def['type']}'")

            if 'label' not in prop_def:
                self.error(rel_path, f"Property '{prop_id}' missing 'label' field")
            else:
                self.validate_translated_text(prop_def['label'], f"{prop_id}.label", rel_path)

            # Validate type-specific fields
            if prop_def['type'] in ['dropdown', 'radio', 'checkbox']:
                if 'options' not in prop_def:
                    self.error(rel_path, f"Property '{prop_id}' with type '{prop_def['type']}' must have 'options'")
                elif not isinstance(prop_def['options'], list):
                    self.error(rel_path, f"Property '{prop_id}.options' must be an array")

    def validate_report_category(self, file_path: Path) -> Optional[str]:
        """Validate report category file."""
        data, rel_path = self.load_json(file_path)
        if data is None:
            return None

        # Required fields
        if 'id' not in data:
            self.error(rel_path, "Missing required field 'id'")
            return None

        category_id = data['id']

        if 'name' not in data:
            self.error(rel_path, "Missing required field 'name'")
        else:
            self.validate_translated_text(data['name'], 'name', rel_path)

        # visibilityFilter can be null or object
        if 'visibilityFilter' in data and data['visibilityFilter'] is not None:
            if not isinstance(data['visibilityFilter'], dict):
                self.error(rel_path, "'visibilityFilter' must be null or object")

        # boundToProperties should be array
        if 'boundToProperties' in data:
            if not isinstance(data['boundToProperties'], list):
                self.error(rel_path, "'boundToProperties' must be an array")

        self.categories[category_id] = data
        return category_id

    def validate_report_action(self, file_path: Path, category_id: str):
        """Validate report action file."""
        data, rel_path = self.load_json(file_path)
        if data is None:
            return

        # Required fields
        if 'id' not in data:
            self.error(rel_path, "Missing required field 'id'")
            return

        action_id = data['id']

        if 'name' not in data:
            self.error(rel_path, "Missing required field 'name'")
        else:
            self.validate_translated_text(data['name'], 'name', rel_path)

        # icon is optional but should be string
        if 'icon' in data and not isinstance(data['icon'], str):
            self.error(rel_path, "'icon' must be a string")

        # properties array
        if 'properties' in data:
            if not isinstance(data['properties'], list):
                self.error(rel_path, "'properties' must be an array")
            else:
                self.validate_properties(data['properties'], rel_path)

        # visibilityFilter can be null or object
        if 'visibilityFilter' in data and data['visibilityFilter'] is not None:
            if not isinstance(data['visibilityFilter'], dict):
                self.error(rel_path, "'visibilityFilter' must be null or object")

        # boundToProperties should be array
        if 'boundToProperties' in data:
            if not isinstance(data['boundToProperties'], list):
                self.error(rel_path, "'boundToProperties' must be an array")

        # Store action
        if category_id not in self.actions:
            self.actions[category_id] = {}
        self.actions[category_id][action_id] = data

    def validate_properties(self, properties: List[Dict], file_path: str):
        """Validate property definitions."""
        property_ids = set()

        for i, prop in enumerate(properties):
            if not isinstance(prop, dict):
                self.error(file_path, f"Property at index {i} must be an object")
                continue

            if 'id' not in prop:
                self.error(file_path, f"Property at index {i} missing 'id'")
                continue

            prop_id = prop['id']
            if prop_id in property_ids:
                self.error(file_path, f"Duplicate property ID '{prop_id}'")
            property_ids.add(prop_id)

            if 'type' not in prop:
                self.error(file_path, f"Property '{prop_id}' missing 'type'")
                continue

            if prop['type'] not in self.valid_types:
                self.error(file_path, f"Property '{prop_id}' has invalid type '{prop['type']}'")

            if 'label' not in prop:
                self.error(file_path, f"Property '{prop_id}' missing 'label'")
            else:
                self.validate_translated_text(prop['label'], f"properties[{i}].label", file_path)

            # Type-specific validation
            if prop['type'] in ['radio', 'checkbox']:
                if 'options' not in prop:
                    self.error(file_path, f"Property '{prop_id}' with type '{prop['type']}' must have 'options'")
                elif not isinstance(prop['options'], list):
                    self.error(file_path, f"Property '{prop_id}.options' must be an array")
                else:
                    self.validate_options(prop['options'], prop_id, file_path)

            if prop['type'] == 'media':
                if 'mode' in prop and prop['mode'] not in ['photo', 'video', 'any']:
                    self.error(file_path, f"Property '{prop_id}' has invalid mode '{prop['mode']}'")
                if 'sources' in prop:
                    if not isinstance(prop['sources'], list):
                        self.error(file_path, f"Property '{prop_id}.sources' must be an array")
                    else:
                        for source in prop['sources']:
                            if source not in ['camera', 'library']:
                                self.error(file_path, f"Property '{prop_id}' has invalid source '{source}'")

            if prop['type'] == 'number':
                for field in ['min', 'max', 'step']:
                    if field in prop and not isinstance(prop[field], (int, float)):
                        self.error(file_path, f"Property '{prop_id}.{field}' must be a number")

    def validate_options(self, options: List[Dict], prop_id: str, file_path: str):
        """Validate option definitions."""
        option_ids = set()

        for i, option in enumerate(options):
            if not isinstance(option, dict):
                self.error(file_path, f"Option at index {i} in property '{prop_id}' must be an object")
                continue

            if 'id' not in option:
                self.error(file_path, f"Option at index {i} in property '{prop_id}' missing 'id'")
                continue

            option_id = option['id']
            if option_id in option_ids:
                self.error(file_path, f"Duplicate option ID '{option_id}' in property '{prop_id}'")
            option_ids.add(option_id)

            if 'label' not in option:
                self.error(file_path, f"Option '{option_id}' in property '{prop_id}' missing 'label'")
            else:
                self.validate_translated_text(option['label'], f"{prop_id}.options[{i}].label", file_path)

    def validate_export_node(self, file_path: Path):
        """Validate export node file."""
        data, rel_path = self.load_json(file_path)
        if data is None:
            return

        if 'id' not in data:
            self.error(rel_path, "Missing required field 'id'")

        if 'title' not in data:
            self.error(rel_path, "Missing required field 'title'")
        else:
            self.validate_translated_text(data['title'], 'title', rel_path)

        if 'timeframe' in data:
            if data['timeframe'] not in ['daily', 'weekly', 'monthly', 'yearly']:
                self.error(rel_path, f"Invalid timeframe '{data['timeframe']}'")

        if 'formula' in data:
            if not isinstance(data['formula'], list):
                self.error(rel_path, "'formula' must be an array")
            else:
                self.validate_formula(data['formula'], rel_path)

    def validate_formula(self, formula: List[Dict], file_path: str):
        """Validate formula elements."""
        for i, element in enumerate(formula):
            if not isinstance(element, dict):
                self.error(file_path, f"Formula element at index {i} must be an object")
                continue

            if 'id' not in element:
                self.error(file_path, f"Formula element at index {i} missing 'id'")

            if 'type' not in element:
                self.error(file_path, f"Formula element at index {i} missing 'type'")
                continue

            element_type = element['type']

            if element_type == 'occurrence':
                for field in ['categoryId', 'actionId']:
                    if field not in element:
                        self.error(file_path, f"Formula element '{element.get('id', i)}' of type 'occurrence' missing '{field}'")

            elif element_type == 'value':
                for field in ['categoryId', 'actionId', 'propertyId']:
                    if field not in element:
                        self.error(file_path, f"Formula element '{element.get('id', i)}' of type 'value' missing '{field}'")

            elif element_type == 'operator':
                if 'operator' not in element:
                    self.error(file_path, f"Formula element '{element.get('id', i)}' of type 'operator' missing 'operator'")
                elif element['operator'] not in ['+', '-', '*', '/']:
                    self.error(file_path, f"Invalid operator '{element['operator']}'")
            else:
                self.error(file_path, f"Invalid formula element type '{element_type}'")

    def validate_graph(self, file_path: Path):
        """Validate graph file."""
        data, rel_path = self.load_json(file_path)
        if data is None:
            return

        if 'id' not in data:
            self.error(rel_path, "Missing required field 'id'")

        if 'title' not in data:
            self.error(rel_path, "Missing required field 'title'")
        else:
            self.validate_translated_text(data['title'], 'title', rel_path)

        if 'chartType' in data:
            valid_chart_types = ['bar', 'line', 'pie', 'doughnut', 'area']
            if data['chartType'] not in valid_chart_types:
                self.error(rel_path, f"Invalid chartType '{data['chartType']}'")

        if 'timeframe' in data:
            if data['timeframe'] not in ['daily', 'weekly', 'monthly', 'yearly']:
                self.error(rel_path, f"Invalid timeframe '{data['timeframe']}'")

        if 'scope' in data:
            if data['scope'] not in ['all', 'per-object', 'perObject']:
                self.error(rel_path, f"Invalid scope '{data['scope']}'")

        if 'dataSeries' in data:
            if not isinstance(data['dataSeries'], list):
                self.error(rel_path, "'dataSeries' must be an array")
            else:
                self.validate_data_series(data['dataSeries'], rel_path)

    def validate_data_series(self, data_series: List[Dict], file_path: str):
        """Validate data series elements."""
        series_ids = set()

        for i, series in enumerate(data_series):
            if not isinstance(series, dict):
                self.error(file_path, f"Data series at index {i} must be an object")
                continue

            if 'id' not in series:
                self.error(file_path, f"Data series at index {i} missing 'id'")
                continue

            series_id = series['id']
            if series_id in series_ids:
                self.error(file_path, f"Duplicate series ID '{series_id}'")
            series_ids.add(series_id)

            if 'type' not in series:
                self.error(file_path, f"Data series '{series_id}' missing 'type'")
                continue

            if series['type'] not in ['value', 'occurrence', 'count']:
                self.error(file_path, f"Data series '{series_id}' has invalid type '{series['type']}'")

            for field in ['categoryId', 'actionId']:
                if field not in series:
                    self.error(file_path, f"Data series '{series_id}' missing '{field}'")

            if 'label' in series and not isinstance(series['label'], str):
                self.error(file_path, f"Data series '{series_id}' label must be a string")

            if 'color' in series:
                color = series['color']
                if not isinstance(color, str) or not (color.startswith('#') or color.startswith('rgb')):
                    self.warning(file_path, f"Data series '{series_id}' color should be hex or rgb format")

    def validate_reports(self):
        """Validate all report files."""
        report_dir = self.templates_dir / 'report'
        if not report_dir.exists():
            self.error('report/', "Directory does not exist")
            return

        # Find all category files (top-level JSON files)
        category_files = [f for f in report_dir.glob('*.json')]

        for category_file in category_files:
            category_id = self.validate_report_category(category_file)

            if category_id:
                # Check for action files in subdirectory
                action_dir = report_dir / category_id
                if action_dir.exists() and action_dir.is_dir():
                    action_files = list(action_dir.glob('*.json'))
                    if not action_files:
                        self.warning(f'report/{category_id}/', "Category has directory but no action files")
                    for action_file in action_files:
                        self.validate_report_action(action_file, category_id)

    def validate_exports(self):
        """Validate all export files."""
        export_dir = self.templates_dir / 'export'
        if not export_dir.exists():
            self.error('export/', "Directory does not exist")
            return

        for export_file in export_dir.rglob('*.json'):
            self.validate_export_node(export_file)

    def validate_graphs(self):
        """Validate all graph files."""
        graph_dir = self.templates_dir / 'graph'
        if not graph_dir.exists():
            self.error('graph/', "Directory does not exist")
            return

        for graph_file in graph_dir.rglob('*.json'):
            self.validate_graph(graph_file)

    def validate_object(self):
        """Validate object.json file."""
        object_file = self.templates_dir / 'object.json'
        if object_file.exists():
            self.validate_object_schema(object_file)
        else:
            self.warning('object.json', "File does not exist")

    def validate_structure(self):
        """Validate directory structure."""
        required_dirs = ['report', 'export', 'graph']
        for dir_name in required_dirs:
            dir_path = self.templates_dir / dir_name
            if not dir_path.exists():
                self.error(dir_name, "Required directory does not exist")
            elif not dir_path.is_dir():
                self.error(dir_name, "Must be a directory")

    def validate(self) -> bool:
        """Run all validations."""
        print(f"🔍 Validating templates in: {self.templates_dir}\n")

        self.validate_structure()
        self.validate_object()
        self.validate_reports()
        self.validate_exports()
        self.validate_graphs()

        # Print results
        if self.warnings:
            print("Warnings:")
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        if self.errors:
            print("Errors:")
            for error in self.errors:
                print(f"  {error}")
            print()
            print(f"❌ Validation failed with {len(self.errors)} error(s)")
            return False
        else:
            print(f"✅ Validation passed!")
            if self.warnings:
                print(f"   ({len(self.warnings)} warning(s))")
            return True


def main():
    """Main entry point."""
    # Get templates directory from command line or use current directory
    if len(sys.argv) > 1:
        templates_dir = Path(sys.argv[1])
    else:
        templates_dir = Path(__file__).parent

    if not templates_dir.exists():
        print(f"❌ Directory does not exist: {templates_dir}")
        sys.exit(1)

    validator = TemplateValidator(templates_dir)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
