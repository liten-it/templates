#!/usr/bin/env python3
"""
Fix Template Validation Errors

This script automatically fixes common validation errors in template JSON files:
1. Adds 'default' field to TranslatedText objects that are missing it
2. Maps invalid property types to valid ones
3. Adds missing 'title' fields to export files
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


class TemplateFixer:
    """Fixes common validation errors in template files."""

    def __init__(self, templates_dir: Path, dry_run: bool = False):
        self.templates_dir = templates_dir
        self.dry_run = dry_run
        self.fixes_applied = 0
        self.files_modified = 0

        # Type mappings
        self.type_mappings = {
            'multiselect': 'checkbox',
            'select': 'dropdown',
            'textarea': 'text'
        }

    def load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, file_path: Path, data: Dict[str, Any]):
        """Save JSON file with pretty formatting."""
        if self.dry_run:
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')  # Add trailing newline

    def fix_translated_text(self, data: Any, field_path: str) -> tuple[Any, bool]:
        """
        Fix TranslatedText object by adding 'default' field if missing.
        Returns (fixed_data, was_modified).
        """
        if not isinstance(data, dict):
            return data, False

        # Check if this looks like a TranslatedText object
        has_translations = 'translations' in data
        has_language_keys = any(key in ['de', 'en', 'nb', 'fr', 'it', 'es'] for key in data.keys())

        if not (has_translations or has_language_keys):
            return data, False

        # If it has 'default', it's already valid
        if 'default' in data:
            return data, False

        # Need to add 'default' field
        default_value = None

        # Strategy 1: If translations object exists, use first value from translations
        if 'translations' in data and isinstance(data['translations'], dict):
            if 'de' in data['translations']:
                default_value = data['translations']['de']
            elif data['translations']:
                # Use first available translation
                default_value = next(iter(data['translations'].values()))

        # Strategy 2: If direct language keys, prefer 'de' or use first available
        if default_value is None:
            if 'de' in data:
                default_value = data['de']
                # Move other language keys to translations
                translations = {k: v for k, v in data.items() if k in ['en', 'nb', 'fr', 'it', 'es']}
                if translations:
                    data = {'default': default_value, 'translations': translations}
                else:
                    data = {'default': default_value}
                self.fixes_applied += 1
                print(f"  Fixed: Added 'default' to {field_path}")
                return data, True
            else:
                # Find first language key
                for key in ['en', 'nb', 'fr', 'it', 'es']:
                    if key in data:
                        default_value = data[key]
                        break

        if default_value is not None:
            data['default'] = default_value
            self.fixes_applied += 1
            print(f"  Fixed: Added 'default' to {field_path}")
            return data, True

        return data, False

    def fix_property_types(self, properties: List[Dict], file_path: str) -> bool:
        """
        Fix invalid property types in properties array.
        Returns True if any fixes were applied.
        """
        modified = False

        for i, prop in enumerate(properties):
            if not isinstance(prop, dict):
                continue

            # Fix property type
            if 'type' in prop and prop['type'] in self.type_mappings:
                old_type = prop['type']
                new_type = self.type_mappings[old_type]
                prop['type'] = new_type
                prop_id = prop.get('id', f'index_{i}')
                print(f"  Fixed: Property '{prop_id}' type '{old_type}' -> '{new_type}'")
                self.fixes_applied += 1
                modified = True

            # If type is 'checkbox' but no options exist, it should be 'boolean'
            if 'type' in prop and prop['type'] == 'checkbox':
                if 'options' not in prop or not prop.get('options'):
                    prop['type'] = 'boolean'
                    prop_id = prop.get('id', f'index_{i}')
                    print(f"  Fixed: Property '{prop_id}' type 'checkbox' -> 'boolean' (no options)")
                    self.fixes_applied += 1
                    modified = True

            # Fix label if it exists
            if 'label' in prop:
                prop['label'], label_fixed = self.fix_translated_text(
                    prop['label'],
                    f"properties[{i}].label"
                )
                if label_fixed:
                    modified = True

            # Fix options labels and add missing 'id' fields
            if 'options' in prop and isinstance(prop['options'], list):
                for j, option in enumerate(prop['options']):
                    if isinstance(option, dict):
                        # Add 'id' field if missing
                        if 'id' not in option:
                            if 'value' in option:
                                option['id'] = option['value']
                                prop_id = prop.get('id', f'index_{i}')
                                print(f"  Fixed: Added 'id' to option in property '{prop_id}' (id='{option['value']}')")
                                self.fixes_applied += 1
                                modified = True
                            else:
                                # Generate an id from the label or index
                                prop_id = prop.get('id', f'index_{i}')
                                option_id = f"option_{j}"
                                option['id'] = option_id
                                print(f"  Fixed: Added 'id' to option in property '{prop_id}' (id='{option_id}')")
                                self.fixes_applied += 1
                                modified = True

                        # Fix label
                        if 'label' in option:
                            option['label'], opt_fixed = self.fix_translated_text(
                                option['label'],
                                f"properties[{i}].options[{j}].label"
                            )
                            if opt_fixed:
                                modified = True

            # Fix placeholder if it exists
            if 'placeholder' in prop:
                prop['placeholder'], ph_fixed = self.fix_translated_text(
                    prop['placeholder'],
                    f"properties[{i}].placeholder"
                )
                if ph_fixed:
                    modified = True

            # Fix unit if it exists
            if 'unit' in prop:
                prop['unit'], unit_fixed = self.fix_translated_text(
                    prop['unit'],
                    f"properties[{i}].unit"
                )
                if unit_fixed:
                    modified = True

        return modified

    def fix_report_file(self, file_path: Path):
        """Fix report category or action file."""
        try:
            data = self.load_json(file_path)
            modified = False
            rel_path = file_path.relative_to(self.templates_dir)

            print(f"\nProcessing: {rel_path}")

            # Fix name field
            if 'name' in data:
                data['name'], name_fixed = self.fix_translated_text(data['name'], 'name')
                if name_fixed:
                    modified = True

            # Fix description field
            if 'description' in data:
                data['description'], desc_fixed = self.fix_translated_text(data['description'], 'description')
                if desc_fixed:
                    modified = True

            # Fix properties array
            if 'properties' in data and isinstance(data['properties'], list):
                if self.fix_property_types(data['properties'], str(rel_path)):
                    modified = True

            # Save if modified
            if modified:
                self.save_json(file_path, data)
                self.files_modified += 1
                if not self.dry_run:
                    print(f"  ✓ Saved changes to {rel_path}")

        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")

    def fix_export_file(self, file_path: Path):
        """Fix export file by adding missing title."""
        try:
            data = self.load_json(file_path)
            modified = False
            rel_path = file_path.relative_to(self.templates_dir)

            print(f"\nProcessing: {rel_path}")

            # Check if title is missing
            if 'title' not in data:
                # Try to derive title from 'name' field
                if 'name' in data:
                    data['title'] = data['name']
                    print(f"  Fixed: Added 'title' field (copied from 'name')")
                    self.fixes_applied += 1
                    modified = True
                # Otherwise use id as fallback
                elif 'id' in data:
                    # Create a title from the ID
                    title_text = data['id'].replace('-', ' ').replace('_', ' ').title()
                    data['title'] = title_text
                    print(f"  Fixed: Added 'title' field (generated from id: '{title_text}')")
                    self.fixes_applied += 1
                    modified = True

            # Fix title if it exists but needs default field
            if 'title' in data:
                data['title'], title_fixed = self.fix_translated_text(data['title'], 'title')
                if title_fixed:
                    modified = True

            # Fix name if it exists
            if 'name' in data:
                data['name'], name_fixed = self.fix_translated_text(data['name'], 'name')
                if name_fixed:
                    modified = True

            # Fix description if it exists
            if 'description' in data:
                data['description'], desc_fixed = self.fix_translated_text(data['description'], 'description')
                if desc_fixed:
                    modified = True

            # Fix unit if it exists
            if 'unit' in data:
                data['unit'], unit_fixed = self.fix_translated_text(data['unit'], 'unit')
                if unit_fixed:
                    modified = True

            # Save if modified
            if modified:
                self.save_json(file_path, data)
                self.files_modified += 1
                if not self.dry_run:
                    print(f"  ✓ Saved changes to {rel_path}")

        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")

    def fix_object_file(self, file_path: Path):
        """Fix object.json file."""
        try:
            data = self.load_json(file_path)
            modified = False
            rel_path = file_path.relative_to(self.templates_dir)

            print(f"\nProcessing: {rel_path}")

            # Fix each property definition
            for prop_id, prop_def in data.items():
                if not isinstance(prop_def, dict):
                    continue

                # Fix property type
                if 'type' in prop_def and prop_def['type'] in self.type_mappings:
                    old_type = prop_def['type']
                    new_type = self.type_mappings[old_type]
                    prop_def['type'] = new_type
                    print(f"  Fixed: Property '{prop_id}' type '{old_type}' -> '{new_type}'")
                    self.fixes_applied += 1
                    modified = True

                # Fix label
                if 'label' in prop_def:
                    prop_def['label'], label_fixed = self.fix_translated_text(
                        prop_def['label'],
                        f"{prop_id}.label"
                    )
                    if label_fixed:
                        modified = True

            # Save if modified
            if modified:
                self.save_json(file_path, data)
                self.files_modified += 1
                if not self.dry_run:
                    print(f"  ✓ Saved changes to {rel_path}")

        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")

    def fix_all(self):
        """Fix all template files."""
        print(f"🔧 Fixing templates in: {self.templates_dir}")
        if self.dry_run:
            print("   (DRY RUN - no files will be modified)\n")
        else:
            print()

        # Fix object.json
        object_file = self.templates_dir / 'object.json'
        if object_file.exists():
            self.fix_object_file(object_file)

        # Fix report files
        report_dir = self.templates_dir / 'report'
        if report_dir.exists():
            for json_file in report_dir.rglob('*.json'):
                self.fix_report_file(json_file)

        # Fix export files
        export_dir = self.templates_dir / 'export'
        if export_dir.exists():
            for json_file in export_dir.rglob('*.json'):
                self.fix_export_file(json_file)

        # Print summary
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Files modified: {self.files_modified}")
        print(f"  Total fixes applied: {self.fixes_applied}")
        if self.dry_run:
            print(f"\n  (DRY RUN - run without --dry-run to apply changes)")
        else:
            print(f"\n  ✓ All fixes have been applied!")
        print(f"{'='*60}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Fix validation errors in template JSON files'
    )
    parser.add_argument(
        'templates_dir',
        nargs='?',
        default='.',
        help='Path to templates directory (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without modifying files'
    )

    args = parser.parse_args()

    templates_dir = Path(args.templates_dir).resolve()

    if not templates_dir.exists():
        print(f"❌ Directory does not exist: {templates_dir}")
        sys.exit(1)

    fixer = TemplateFixer(templates_dir, dry_run=args.dry_run)
    fixer.fix_all()


if __name__ == '__main__':
    main()
