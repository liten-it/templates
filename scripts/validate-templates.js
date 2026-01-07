#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");

const { TemplateV2Schema } = require("@liten/template-validator");

const repoRoot = process.cwd();
const templatesRoot = repoRoot;
const report = {
    summary: {
        totalFiles: 0,
        valid: 0,
        invalid: 0,
        parseErrors: 0,
    },
    files: [],
};

const findDataJsonFiles = (dir) => {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    const results = [];
    for (const entry of entries) {
        if (entry.name === "node_modules" || entry.name.startsWith(".")) {
            continue;
        }
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            results.push(...findDataJsonFiles(fullPath));
            continue;
        }
        if (entry.isFile() && entry.name === "data.json") {
            results.push(fullPath);
        }
    }
    return results;
};

const formatIssue = (issue) => ({
    path: issue.path.join("/"),
    message: issue.message,
    code: issue.code,
});

const validateFile = (filePath) => {
    const relativePath = path.relative(templatesRoot, filePath);
    report.summary.totalFiles += 1;
    try {
        const raw = fs.readFileSync(filePath, "utf-8");
        const json = JSON.parse(raw);
        const result = TemplateV2Schema.safeParse(json);
        if (result.success) {
            report.summary.valid += 1;
            report.files.push({ path: relativePath, valid: true });
            return;
        }
        report.summary.invalid += 1;
        report.files.push({
            path: relativePath,
            valid: false,
            errors: result.error.issues.map(formatIssue),
        });
    } catch (error) {
        report.summary.parseErrors += 1;
        report.summary.invalid += 1;
        report.files.push({
            path: relativePath,
            valid: false,
            errors: [
                {
                    path: "",
                    message: error instanceof Error ? error.message : "Unknown JSON parse error",
                    code: "parse_error",
                },
            ],
        });
    }
};

const main = () => {
    const files = findDataJsonFiles(templatesRoot);
    if (files.length === 0) {
        console.log("No data.json files found.");
        process.exit(0);
    }

    files.forEach(validateFile);

    const reportJsonPath = path.join(repoRoot, "validation-report.json");
    const reportMdPath = path.join(repoRoot, "validation-report.md");

    fs.writeFileSync(reportJsonPath, JSON.stringify(report, null, 2));

    const lines = [];
    lines.push("# Template Validation Report");
    lines.push("");
    lines.push(`- Total files: ${report.summary.totalFiles}`);
    lines.push(`- Valid: ${report.summary.valid}`);
    lines.push(`- Invalid: ${report.summary.invalid}`);
    lines.push(`- Parse errors: ${report.summary.parseErrors}`);
    lines.push("");

    for (const file of report.files) {
        if (file.valid) {
            continue;
        }
        lines.push(`## ${file.path}`);
        for (const err of file.errors || []) {
            const issuePath = err.path ? `\`${err.path}\`` : "`<root>`";
            lines.push(`- ${issuePath}: ${err.message} (${err.code})`);
        }
        lines.push("");
    }

    fs.writeFileSync(reportMdPath, lines.join("\n"));

    if (report.summary.invalid > 0) {
        console.error(`Validation failed: ${report.summary.invalid} file(s) invalid.`);
        console.error(`Report: ${reportMdPath}`);
        process.exit(1);
    }

    console.log("All templates valid.");
    console.log(`Report: ${reportMdPath}`);
};

main();
