#!/usr/bin/env node

/**
 * Skill Customization tests -- Zero-dependency test suite.
 *
 * Tests: override resolution, customization CRUD, diff generation,
 * payload construction, consent handling, config parsing, cross-platform paths.
 *
 * Uses a temp directory to avoid touching real ~/.cre-skills/.
 *
 * Run: node tests/test-customization.mjs
 */

import { mkdirSync, readFileSync, writeFileSync, rmSync, existsSync } from "fs";
import { join, dirname, resolve } from "path";
import { tmpdir } from "os";
import { randomUUID } from "crypto";
import { fileURLToPath } from "url";

// ---------------------------------------------------------------------------
// Test harness
// ---------------------------------------------------------------------------

let totalPass = 0;
let totalFail = 0;
const failedTests = [];

function assert(suite, label, condition) {
  const tag = `[${suite}] ${label}`;
  if (condition) {
    totalPass++;
    console.log(`  PASS: ${tag}`);
  } else {
    totalFail++;
    failedTests.push(tag);
    console.log(`  FAIL: ${tag}`);
  }
}

function assertEq(suite, label, actual, expected) {
  const condition = actual === expected;
  const tag = `[${suite}] ${label}`;
  if (condition) {
    totalPass++;
    console.log(`  PASS: ${tag}`);
  } else {
    totalFail++;
    failedTests.push(tag);
    console.log(`  FAIL: ${tag} -- expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

// ---------------------------------------------------------------------------
// Temp directory setup
// ---------------------------------------------------------------------------

const TEMP_DIR = join(tmpdir(), `cre-cust-test-${randomUUID().slice(0, 8)}`);
const TEMP_CUST_DIR = join(TEMP_DIR, "customizations");
const TEMP_INDEX_PATH = join(TEMP_CUST_DIR, "index.json");
const TEMP_SKILLS_DIR = join(TEMP_DIR, "skills");

mkdirSync(TEMP_SKILLS_DIR, { recursive: true });

// Create a fake base skill
const FAKE_SLUG = "test-skill";
const FAKE_SKILL_CONTENT = `---
name: test-skill
slug: test-skill
version: 0.1.0
status: deployed
category: reit-cre
description: A test skill for unit testing
targets:
  - claude_code
---

# Test Skill

You are a test analyst.

## When to Activate
- When running tests

## Input Schema
| Field | Required | Default |
| property_type | Yes | -- |
| location | Yes | -- |

## Process
### Step 1: Parse Input
Read the input and validate.

### Step 2: Analyze
Run the analysis.

### Step 3: Report
Generate the report.

## Output Format
A test report with findings.
`;

mkdirSync(join(TEMP_SKILLS_DIR, FAKE_SLUG), { recursive: true });
writeFileSync(join(TEMP_SKILLS_DIR, FAKE_SLUG, "SKILL.md"), FAKE_SKILL_CONTENT);

// ---------------------------------------------------------------------------
// Import modules (patch paths for customization module)
// ---------------------------------------------------------------------------

const __dirname_test = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ROOT = resolve(__dirname_test, "..");

// Import diff module (no patching needed, it's stateless)
const { computeDiff, summarizeDiff, formatDiffText, contentHash } = await import(
  join(PLUGIN_ROOT, "lib", "diff.mjs")
);

// Import customization module and patch paths
const custModule = await import(join(PLUGIN_ROOT, "lib", "customization.mjs"));
custModule._setTestPaths(TEMP_CUST_DIR, TEMP_INDEX_PATH);

const {
  hasCustomization, createCustomization, saveCustomization,
  getCustomization, listCustomizations, revertCustomization,
  resolveSkillPath, readIndex, CHANGE_CATEGORIES, getBaseSnapshot,
  exportCustomization, importCustomization, healthCheck, healthCheckAll,
  listTemplates, createFromTemplate,
} = custModule;

// Import feedback-payload module (reads from real config, but we test buildPayload/filterByMode directly)
const {
  buildPayload, filterByMode, previewPayload, FEEDBACK_MODES,
  buildUpstreamSuggestion, analyzeCustomizationFeedback,
} = await import(join(PLUGIN_ROOT, "lib", "feedback-payload.mjs"));

// ---------------------------------------------------------------------------
// 1. Diff tests
// ---------------------------------------------------------------------------

function testContentHash() {
  console.log("\n--- contentHash ---");
  const h1 = contentHash("hello world");
  const h2 = contentHash("hello world");
  const h3 = contentHash("hello world!");

  assert("hash", "deterministic", h1 === h2);
  assert("hash", "different content different hash", h1 !== h3);
  assert("hash", "is 64 hex chars", /^[a-f0-9]{64}$/.test(h1));
}

function testComputeDiff() {
  console.log("\n--- computeDiff ---");

  // No changes
  const same = computeDiff("line 1\nline 2\nline 3", "line 1\nline 2\nline 3");
  assertEq("diff-same", "no additions", same.stats.added, 0);
  assertEq("diff-same", "no removals", same.stats.removed, 0);
  assertEq("diff-same", "all unchanged", same.stats.unchanged, 3);
  assertEq("diff-same", "no hunks", same.hunks.length, 0);

  // Addition
  const added = computeDiff("line 1\nline 2", "line 1\nline 2\nline 3");
  assertEq("diff-add", "1 addition", added.stats.added, 1);
  assertEq("diff-add", "0 removals", added.stats.removed, 0);

  // Removal
  const removed = computeDiff("line 1\nline 2\nline 3", "line 1\nline 3");
  assertEq("diff-remove", "0 additions", removed.stats.added, 0);
  assertEq("diff-remove", "1 removal", removed.stats.removed, 1);

  // Replacement
  const replaced = computeDiff("line 1\nold line\nline 3", "line 1\nnew line\nline 3");
  assert("diff-replace", "has additions", replaced.stats.added > 0);
  assert("diff-replace", "has removals", replaced.stats.removed > 0);
}

function testSummarizeDiff() {
  console.log("\n--- summarizeDiff ---");

  const noChange = computeDiff("a\nb", "a\nb");
  const summary1 = summarizeDiff(noChange);
  assert("summary", "no changes message", summary1.includes("No changes"));

  const withChange = computeDiff("## Process\nStep 1\nStep 2", "## Process\nStep 1\nStep 2\nStep 3");
  const summary2 = summarizeDiff(withChange);
  assert("summary", "mentions added lines", summary2.includes("added"));
}

function testSectionsChanged() {
  console.log("\n--- sections changed ---");

  const original = "# Title\n\n## Process\nStep 1\nStep 2\n\n## Output\nFormat A";
  const modified = "# Title\n\n## Process\nStep 1\nStep 2\nStep 3\n\n## Output\nFormat A";
  const diff = computeDiff(original, modified);

  assert("sections", "detects Process section", diff.sections_changed.includes("Process"));
  assert("sections", "does not include Output", !diff.sections_changed.includes("Output"));
}

function testFormatDiffText() {
  console.log("\n--- formatDiffText ---");

  const diff = computeDiff("line 1\nold\nline 3", "line 1\nnew\nline 3");
  const text = formatDiffText(diff);

  assert("format", "contains @@ header", text.includes("@@"));
  assert("format", "contains - prefix", text.includes("- "));
  assert("format", "contains + prefix", text.includes("+ "));
}

// ---------------------------------------------------------------------------
// 2. Customization CRUD tests
// ---------------------------------------------------------------------------

function testCreateCustomization() {
  console.log("\n--- createCustomization ---");

  const record = createCustomization(FAKE_SLUG, FAKE_SKILL_CONTENT, "4.0.0");

  assert("create", "returns customization_id", record.customization_id.startsWith("cust_"));
  assertEq("create", "skill_slug", record.skill_slug, FAKE_SLUG);
  assertEq("create", "status is draft", record.status, "draft");
  assertEq("create", "base and modified hash match", record.base_content_hash, record.modified_content_hash);
  assert("create", "SKILL.md exists", existsSync(join(TEMP_CUST_DIR, FAKE_SLUG, "SKILL.md")));
  assert("create", "base-snapshot.md exists", existsSync(join(TEMP_CUST_DIR, FAKE_SLUG, "base-snapshot.md")));
  assert("create", "metadata.json exists", existsSync(join(TEMP_CUST_DIR, FAKE_SLUG, "metadata.json")));

  // Index updated
  const index = readIndex();
  assert("create", "index has entry", index.customizations[FAKE_SLUG] != null);
}

function testHasCustomization() {
  console.log("\n--- hasCustomization ---");

  assert("has", "returns true for existing", hasCustomization(FAKE_SLUG));
  assert("has", "returns false for missing", !hasCustomization("nonexistent-skill"));
}

function testResolveSkillPath() {
  console.log("\n--- resolveSkillPath ---");

  // With customization
  const resolved = resolveSkillPath(FAKE_SLUG, TEMP_SKILLS_DIR);
  assertEq("resolve", "source is customized", resolved.source, "customized");
  assert("resolve", "path points to customizations dir", resolved.path.includes("customizations"));

  // Without customization
  const base = resolveSkillPath("other-skill", TEMP_SKILLS_DIR);
  assertEq("resolve-base", "source is base", base.source, "base");
  assert("resolve-base", "path points to skills dir", base.path.includes("skills"));
}

function testSaveCustomization() {
  console.log("\n--- saveCustomization ---");

  const modified = FAKE_SKILL_CONTENT.replace("### Step 2: Analyze", "### Step 2: Deep Dive Analysis");
  const record = saveCustomization(FAKE_SLUG, modified, {
    rationale: "Our team calls it Deep Dive not Analyze",
    change_categories: ["terminology"],
  });

  assertEq("save", "status is active", record.status, "active");
  assert("save", "hashes differ", record.base_content_hash !== record.modified_content_hash);
  assertEq("save", "rationale saved", record.rationale, "Our team calls it Deep Dive not Analyze");
  assert("save", "categories saved", record.change_categories.includes("terminology"));

  // Content was written
  const content = readFileSync(join(TEMP_CUST_DIR, FAKE_SLUG, "SKILL.md"), "utf-8");
  assert("save", "content updated", content.includes("Deep Dive Analysis"));
}

function testGetCustomization() {
  console.log("\n--- getCustomization ---");

  const cust = getCustomization(FAKE_SLUG);
  assert("get", "returns content", cust.content != null);
  assert("get", "returns base", cust.base != null);
  assert("get", "returns metadata", cust.metadata != null);
  assert("get", "content is modified", cust.content.includes("Deep Dive"));
  assert("get", "base is original", cust.base.includes("### Step 2: Analyze"));

  const missing = getCustomization("nonexistent");
  assert("get-miss", "returns null for missing", missing === null);
}

function testListCustomizations() {
  console.log("\n--- listCustomizations ---");

  const list = listCustomizations();
  assert("list", "has at least one entry", list.length >= 1);
  const entry = list.find(e => e.slug === FAKE_SLUG);
  assert("list", "contains our skill", entry != null);
  assertEq("list", "has status", entry.status, "active");
}

function testGetBaseSnapshot() {
  console.log("\n--- getBaseSnapshot ---");

  const base = getBaseSnapshot(FAKE_SLUG);
  assert("base", "returns content", base != null);
  assert("base", "is original content", base.includes("### Step 2: Analyze"));
  assert("base", "is not modified content", !base.includes("Deep Dive"));
}

function testRevertCustomization() {
  console.log("\n--- revertCustomization ---");

  // Create a second customization to revert
  const slug2 = "revert-test-skill";
  mkdirSync(join(TEMP_SKILLS_DIR, slug2), { recursive: true });
  writeFileSync(join(TEMP_SKILLS_DIR, slug2, "SKILL.md"), "# Test\nOriginal content");
  createCustomization(slug2, "# Test\nOriginal content", "4.0.0");

  assert("revert-pre", "customization exists before", hasCustomization(slug2));

  const reverted = revertCustomization(slug2);
  assert("revert", "returns true", reverted);
  assert("revert", "customization removed", !hasCustomization(slug2));

  const index = readIndex();
  assert("revert", "removed from index", index.customizations[slug2] == null);

  // Revert nonexistent
  assert("revert-miss", "returns false for missing", !revertCustomization("nonexistent"));
}

// ---------------------------------------------------------------------------
// 3. Feedback payload tests
// ---------------------------------------------------------------------------

function testBuildPayload() {
  console.log("\n--- buildPayload ---");

  const cust = getCustomization(FAKE_SLUG);
  const diff = computeDiff(cust.base, cust.content);

  const payload = buildPayload({
    metadata: cust.metadata,
    diffSummary: summarizeDiff(diff),
    diffText: formatDiffText(diff),
    modifiedContent: cust.content,
    diffStats: diff.stats,
    sectionsChanged: diff.sections_changed,
    pluginVersion: "4.0.0",
    wantsUpstreamConsideration: true,
    consentedToContent: false,
  });

  assert("payload", "has feedback_id", payload.feedback_id.startsWith("cfb_"));
  assertEq("payload", "feedback_type", payload.feedback_type, "customization_feedback");
  assertEq("payload", "skill_slug", payload.skill_slug, FAKE_SLUG);
  assert("payload", "has timestamp", payload.timestamp != null);
  assert("payload", "has base_content_hash", /^[a-f0-9]{64}$/.test(payload.base_content_hash));
  assert("payload", "wants upstream", payload.wants_upstream_consideration);
  assert("payload", "not consented to content", !payload.consented_to_content);
}

function testFilterByMode() {
  console.log("\n--- filterByMode ---");

  const fullPayload = {
    feedback_id: "cfb_test123456789012",
    skill_slug: FAKE_SLUG,
    diff_summary: "2 lines added",
    diff_text: "- old\n+ new",
    diff_stats: { added: 2, removed: 1, unchanged: 10 },
    sections_changed: ["Process"],
    modified_content: "full content here",
    consented_to_content: false,
  };

  // metadata_only: strips everything extended
  const metaOnly = filterByMode(fullPayload, "metadata_only");
  assert("filter-meta", "no diff_summary", metaOnly.diff_summary === null);
  assert("filter-meta", "no diff_stats", metaOnly.diff_stats === null);
  assert("filter-meta", "no diff_text", metaOnly.diff_text === null);
  assert("filter-meta", "no content", metaOnly.modified_content === null);

  // metadata_and_summary: keeps summary, strips diff text and content
  const withSummary = filterByMode(fullPayload, "metadata_and_summary");
  assertEq("filter-summary", "has diff_summary", withSummary.diff_summary, "2 lines added");
  assert("filter-summary", "no diff_text", withSummary.diff_text === null);
  assert("filter-summary", "no content", withSummary.modified_content === null);

  // metadata_and_diff: keeps summary + diff text, strips content
  const withDiff = filterByMode(fullPayload, "metadata_and_diff");
  assert("filter-diff", "has diff_text", withDiff.diff_text != null);
  assert("filter-diff", "no content", withDiff.modified_content === null);

  // metadata_and_content without consent: strips content anyway
  const noConsent = filterByMode(fullPayload, "metadata_and_content");
  assert("filter-noconsent", "no content without consent", noConsent.modified_content === null);

  // metadata_and_content with consent
  const withConsent = filterByMode({ ...fullPayload, consented_to_content: true }, "metadata_and_content");
  assert("filter-consent", "has content with consent", withConsent.modified_content != null);
}

function testPreviewPayload() {
  console.log("\n--- previewPayload ---");

  const payload = {
    feedback_id: "cfb_test123456789012",
    skill_slug: FAKE_SLUG,
    change_categories: ["terminology", "required_steps"],
    rationale: "Our org uses different terms",
    base_content_hash: "a".repeat(64),
    modified_content_hash: "b".repeat(64),
    wants_upstream_consideration: true,
    diff_summary: "3 lines added",
    diff_stats: { added: 3, removed: 1, unchanged: 20 },
    sections_changed: ["Process"],
    diff_text: null,
    modified_content: null,
    consented_to_content: false,
  };

  const preview = previewPayload(payload, "metadata_and_summary");
  assert("preview", "mentions skill", preview.includes(FAKE_SLUG));
  assert("preview", "mentions categories", preview.includes("terminology"));
  assert("preview", "mentions rationale", preview.includes("different terms"));
  assert("preview", "mentions upstream", preview.includes("yes"));
}

function testChangeCategories() {
  console.log("\n--- CHANGE_CATEGORIES ---");

  assert("categories", "has terminology", CHANGE_CATEGORIES.includes("terminology"));
  assert("categories", "has compliance_governance", CHANGE_CATEGORIES.includes("compliance_governance"));
  assert("categories", "has other", CHANGE_CATEGORIES.includes("other"));
  assert("categories", "has 11 categories", CHANGE_CATEGORIES.length === 11);
}

function testFeedbackModes() {
  console.log("\n--- FEEDBACK_MODES ---");

  assert("modes", "has off", FEEDBACK_MODES.includes("off"));
  assert("modes", "has metadata_only", FEEDBACK_MODES.includes("metadata_only"));
  assert("modes", "has metadata_and_content", FEEDBACK_MODES.includes("metadata_and_content"));
  assert("modes", "has 5 modes", FEEDBACK_MODES.length === 5);
}

// ---------------------------------------------------------------------------
// 4. Config and consent tests
// ---------------------------------------------------------------------------

function testNoSendWhenDisabled() {
  console.log("\n--- no-send when feedback disabled ---");

  // filterByMode with "off" strips everything
  const payload = {
    diff_summary: "test",
    diff_stats: { added: 1, removed: 0, unchanged: 5 },
    sections_changed: ["Process"],
    diff_text: "- old\n+ new",
    modified_content: "content",
    consented_to_content: true,
  };

  const filtered = filterByMode(payload, "off");
  assert("disabled", "no diff_summary", filtered.diff_summary === null);
  assert("disabled", "no diff_stats", filtered.diff_stats === null);
  assert("disabled", "no diff_text", filtered.diff_text === null);
  assert("disabled", "no content", filtered.modified_content === null);
}

// ---------------------------------------------------------------------------
// 5. Cross-platform path tests
// ---------------------------------------------------------------------------

function testCrossPlatformPaths() {
  console.log("\n--- cross-platform paths ---");

  // Verify that paths use the platform separator
  const resolved = resolveSkillPath(FAKE_SLUG, TEMP_SKILLS_DIR);
  assert("paths", "resolved path is absolute", resolved.path.startsWith("/") || resolved.path.match(/^[A-Z]:\\/));
  assert("paths", "path contains slug", resolved.path.includes(FAKE_SLUG));
}

// ---------------------------------------------------------------------------
// 6. Diff with real skill content
// ---------------------------------------------------------------------------

function testDiffWithRealSkillStructure() {
  console.log("\n--- diff with real SKILL.md structure ---");

  const modified = FAKE_SKILL_CONTENT
    .replace("### Step 2: Analyze\nRun the analysis.", "### Step 2: Deep Dive\nRun the deep dive analysis.\nInclude market comps.")
    .replace("### Step 3: Report\nGenerate the report.", "### Step 3: Executive Summary\nGenerate the executive summary.\nInclude risk flags.");

  const diff = computeDiff(FAKE_SKILL_CONTENT, modified);

  assert("real-diff", "detected additions", diff.stats.added > 0);
  assert("real-diff", "detected removals", diff.stats.removed > 0);
  assert("real-diff", "detected Process section change", diff.sections_changed.includes("Process") || diff.sections_changed.some(s => s.includes("Step")));

  const summary = summarizeDiff(diff);
  assert("real-diff", "summary is non-empty", summary.length > 0);
  assert("real-diff", "summary mentions lines", summary.includes("line"));
}

// ---------------------------------------------------------------------------
// 7. Path traversal prevention tests
// ---------------------------------------------------------------------------

function testPathTraversalPrevention() {
  console.log("\n--- path traversal prevention ---");

  const maliciousSlugs = [
    "../../../etc/passwd",
    "..\\..\\windows\\system32",
    "..",
    ".",
    "foo/../../bar",
    "foo\\bar",
    "slug/../escape",
  ];

  for (const slug of maliciousSlugs) {
    let threw = false;
    try { hasCustomization(slug); } catch { threw = true; }
    assert("traversal", `rejects '${slug.slice(0, 20)}' in hasCustomization`, threw);
  }

  // Import with malicious slug
  let importThrew = false;
  try {
    importCustomization({
      format: "cre-skills-customization-v1",
      skill_slug: "../../.ssh/authorized_keys",
      customized_content: "malicious",
    });
  } catch { importThrew = true; }
  assert("traversal", "rejects malicious import slug", importThrew);

  // Valid slugs should still work
  let validOk = false;
  try { hasCustomization("deal-quick-screen"); validOk = true; } catch {}
  assert("traversal", "allows valid slug", validOk);
}

// ---------------------------------------------------------------------------
// 8. Export / Import tests
// ---------------------------------------------------------------------------

function testExportCustomization() {
  console.log("\n--- exportCustomization ---");

  const bundle = exportCustomization(FAKE_SLUG);
  assert("export", "returns a bundle", bundle != null);
  assertEq("export", "format version", bundle.format, "cre-skills-customization-v1");
  assertEq("export", "skill_slug", bundle.skill_slug, FAKE_SLUG);
  assert("export", "has metadata", bundle.metadata != null);
  assert("export", "has base_content", bundle.base_content != null);
  assert("export", "has customized_content", bundle.customized_content != null);
  assert("export", "base is original", bundle.base_content.includes("### Step 2: Analyze"));
  assert("export", "customized is modified", bundle.customized_content.includes("Deep Dive"));

  const missing = exportCustomization("nonexistent");
  assert("export-miss", "returns null for missing", missing === null);
}

function testImportCustomization() {
  console.log("\n--- importCustomization ---");

  // Export current, revert, then import
  const bundle = exportCustomization(FAKE_SLUG);
  revertCustomization(FAKE_SLUG);
  assert("import-pre", "reverted before import", !hasCustomization(FAKE_SLUG));

  const result = importCustomization(bundle);
  assertEq("import", "slug matches", result.slug, FAKE_SLUG);
  assert("import", "has customization_id", result.customization_id.startsWith("cust_"));
  assertEq("import", "status is active", result.status, "active");
  assert("import", "customization exists after", hasCustomization(FAKE_SLUG));

  // Verify content roundtripped
  const cust = getCustomization(FAKE_SLUG);
  assert("import", "content preserved", cust.content.includes("Deep Dive"));
  assert("import", "base preserved", cust.base.includes("### Step 2: Analyze"));

  // Invalid bundle
  let threw = false;
  try { importCustomization({ format: "wrong" }); } catch { threw = true; }
  assert("import-invalid", "rejects invalid format", threw);
}

// ---------------------------------------------------------------------------
// 8. Health Check tests
// ---------------------------------------------------------------------------

function testHealthCheck() {
  console.log("\n--- healthCheck ---");

  // Current: base hasn't changed
  const current = healthCheck(FAKE_SLUG, TEMP_SKILLS_DIR);
  assertEq("health", "status is current", current.status, "current");

  // Modify the base skill to simulate drift
  const basePath = join(TEMP_SKILLS_DIR, FAKE_SLUG, "SKILL.md");
  const driftedContent = FAKE_SKILL_CONTENT + "\n### Step 4: New Upstream Step\nDo something new.";
  writeFileSync(basePath, driftedContent);

  const drifted = healthCheck(FAKE_SLUG, TEMP_SKILLS_DIR);
  assertEq("health-drift", "status is drifted", drifted.status, "drifted");
  assert("health-drift", "has drift_stats", drifted.drift_stats != null);
  assert("health-drift", "has message about update", drifted.message.includes("updated"));

  // Restore base
  writeFileSync(basePath, FAKE_SKILL_CONTENT);

  // No customization
  const noCust = healthCheck("nonexistent", TEMP_SKILLS_DIR);
  assertEq("health-none", "status is no_customization", noCust.status, "no_customization");

  // Base missing
  const baseMissing = healthCheck(FAKE_SLUG, join(TEMP_DIR, "empty-skills"));
  assertEq("health-missing", "status is base_missing", baseMissing.status, "base_missing");
}

function testHealthCheckAll() {
  console.log("\n--- healthCheckAll ---");

  const results = healthCheckAll(TEMP_SKILLS_DIR);
  assert("health-all", "returns array", Array.isArray(results));
  assert("health-all", "has entries", results.length > 0);
  assert("health-all", "each has slug", results.every(r => r.slug));
  assert("health-all", "each has status", results.every(r => r.status));
}

// ---------------------------------------------------------------------------
// 9. Template tests
// ---------------------------------------------------------------------------

function testListTemplates() {
  console.log("\n--- listTemplates ---");

  // Create a temp templates dir with a fake template
  const tmplDir = join(TEMP_DIR, "templates");
  mkdirSync(join(tmplDir, "customizations"), { recursive: true });
  writeFileSync(join(tmplDir, "customizations", "test-template.json"), JSON.stringify({
    name: "Test Template",
    description: "A test template",
    target_skill: FAKE_SLUG,
    categories: ["terminology"],
    rationale: "Testing templates",
    replacements: [{ find: "### Step 2: Analyze", replace: "### Step 2: Template Step" }],
  }));

  const templates = listTemplates(tmplDir);
  assert("templates", "found template", templates.length === 1);
  assertEq("templates", "template id", templates[0].id, "test-template");
  assertEq("templates", "template name", templates[0].name, "Test Template");
  assertEq("templates", "target skill", templates[0].target_skill, FAKE_SLUG);

  // Empty directory
  const empty = listTemplates(join(TEMP_DIR, "no-templates"));
  assertEq("templates-empty", "no templates", empty.length, 0);
}

function testCreateFromTemplate() {
  console.log("\n--- createFromTemplate ---");

  // Revert any existing customization first
  revertCustomization(FAKE_SLUG);

  const tmplDir = join(TEMP_DIR, "templates");
  const record = createFromTemplate("test-template", TEMP_SKILLS_DIR, tmplDir, "4.0.0");

  assertEq("from-template", "slug matches", record.skill_slug, FAKE_SLUG);
  assertEq("from-template", "status is active", record.status, "active");
  assert("from-template", "has rationale", record.rationale.includes("template"));
  assert("from-template", "has categories", record.change_categories.includes("terminology"));

  // Verify the template replacements were applied
  const cust = getCustomization(FAKE_SLUG);
  assert("from-template", "replacement applied", cust.content.includes("Template Step"));
  assert("from-template", "original text replaced", !cust.content.includes("### Step 2: Analyze\n"));
}

// ---------------------------------------------------------------------------
// 10. Upstream suggestion tests
// ---------------------------------------------------------------------------

function testBuildUpstreamSuggestion() {
  console.log("\n--- buildUpstreamSuggestion ---");

  const cust = getCustomization(FAKE_SLUG);
  const diff = computeDiff(cust.base, cust.content);

  const suggestion = buildUpstreamSuggestion(cust.metadata, summarizeDiff(diff), formatDiffText(diff));
  assert("upstream", "has title", suggestion.title.includes(FAKE_SLUG));
  assert("upstream", "has body", suggestion.body.length > 0);
  assert("upstream", "body has skill slug", suggestion.body.includes(FAKE_SLUG));
  assert("upstream", "body has diff section", suggestion.body.includes("### Diff"));
  assert("upstream", "has labels array", Array.isArray(suggestion.labels));
  assert("upstream", "labels include skill-improvement", suggestion.labels.includes("skill-improvement"));
}

// ---------------------------------------------------------------------------
// 11. Analytics tests
// ---------------------------------------------------------------------------

function testAnalyzeCustomizationFeedback() {
  console.log("\n--- analyzeCustomizationFeedback ---");

  // Since we haven't written to the real feedback log, this should return 0
  const analytics = analyzeCustomizationFeedback();
  assertEq("analytics", "total is 0", analytics.total, 0);
  assert("analytics", "has message", analytics.message != null);
}

// ---------------------------------------------------------------------------
// Run all tests
// ---------------------------------------------------------------------------

testContentHash();
testComputeDiff();
testSummarizeDiff();
testSectionsChanged();
testFormatDiffText();

testCreateCustomization();
testHasCustomization();
testResolveSkillPath();
testSaveCustomization();
testGetCustomization();
testListCustomizations();
testGetBaseSnapshot();
testRevertCustomization();

testBuildPayload();
testFilterByMode();
testPreviewPayload();
testChangeCategories();
testFeedbackModes();
testNoSendWhenDisabled();

testCrossPlatformPaths();
testDiffWithRealSkillStructure();

testPathTraversalPrevention();
testExportCustomization();
testImportCustomization();
testHealthCheck();
testHealthCheckAll();
testListTemplates();
testCreateFromTemplate();
testBuildUpstreamSuggestion();
testAnalyzeCustomizationFeedback();

// Cleanup
custModule._resetPaths();
rmSync(TEMP_DIR, { recursive: true, force: true });

// Summary
console.log(`\n${"=".repeat(50)}`);
console.log(`TOTAL: ${totalPass} passed, ${totalFail} failed`);
if (failedTests.length > 0) {
  console.log("\nFailed tests:");
  for (const t of failedTests) console.log(`  - ${t}`);
  process.exit(1);
}
