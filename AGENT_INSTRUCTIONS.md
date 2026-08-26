# Agent Instructions

Read this entire file before starting any task.

## Self-Correcting Rules Engine

This file contains an evolving ruleset that improves over time. **At session start, read the entire "Learned Rules" section before doing anything.**

### How it works

1. When the user corrects you, rejects an approach, or a mistake is identified, **immediately append a new rule** to the "Learned Rules" section at the bottom of this file.
2. Rules are numbered sequentially and written as clear, imperative instructions.
3. Format: `N. [CATEGORY] Never/Always do X — because Y.`
4. Categories: `[BRAND]`, `[CRO]`, `[CODE]`, `[ARCH]`, `[TOOL]`, `[PROCESS]`, `[DATA]`, `[UX]`, `[FINANCE]`, `[PRICING]`, `[SUPPLIER]`, `[LOGISTICS]`, `[OPPORTUNITY]`, `[OTHER]`
5. Before starting any task, silently verify that your plan complies with all rules below.
6. If two rules conflict, the higher-numbered (newer) rule strictly takes precedence.
7. Never delete rules. If a rule becomes obsolete, append a new rule that explicitly supersedes rule #N.

### When to add a rule

- User explicitly corrects your output ("no, do it this way")
- User rejects a file, approach, framework, or pattern
- You hit a bug caused by an invalid assumption about the stack or project
- User states a preference ("always use X", "never do Y")
- An audit fails during validation loops

---

## Learned Rules

<!-- Seed baseline rules -->
1. [BRAND] Always use PawPawDoo brand palette: Primary Terracotta (`#C86432`), Espresso Text (`#37281D`), Cream Background (`#FAF8F5`) — established brand identity.
2. [BRAND] Always use tagline 'Pawmily first.' in core value propositions and hero sections — official brand slogan.
3. [PROCESS] Never publish live changes or spend live ad budget without explicit human confirmation — system security and spend guardrail.
4. [CRO] Always design storefront layouts with mobile-first viewport constraints and sticky CTA bars — 85%+ DTC traffic is mobile.
5. [FINANCE] Never recommend dropshipping products with <3.0x markup multiplier — required to maintain ad CAC profitability.

<!-- New rules are appended below this line. Do not edit above this section. -->

6. [PRICING] Always price lower than top Amazon/eBay US listings while keeping landed markup >= 3.0x — competitive price advantage and customer value.
7. [SUPPLIER] Always filter suppliers: >=1 year on AliExpress, >=4.0 stars overall, fast tracked shipping (5-7 days) — supply chain reliability and low dispute rates.
8. [LOGISTICS] Always default to US warehouse for faster 3-5 day delivery if US vs China warehouse shipping cost diff <= $3.00 — superior customer experience and higher conversion.
9. [DATA] Always include AliExpress Product ID & DSers SKU mapping in all research outputs for 1-click Shopify import — frictionless fulfillment and automation.
10. [OPPORTUNITY] If a product fails the >=3.0x markup filter but has high viral/market demand, do not discard it — flag it as `[HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY]` (🟠 Amber) and generate an undercut pricing + multi-pack bundle strategy to recover margin — captures high-volume viral traffic with backend margin recovery.
11. [BRAND] Always position PawPawDoo as a warm, premium pet lifestyle brand for BOTH cats and dogs — avoid over-indexing solely on dogs or sounding like a clinical medical company.
12. [UX] Always position the tagline 'Pawmily first.' directly underneath the PawPawDoo logo title — established layout specification.
13. [CRO] Always require actual product showcase assets (including cat & dog lifestyle context, size/color variant selectors) on landing pages rather than standalone stock animal photos.
14. [SKILLS] Equip Storefront Architect with dedicated UI/UX Design Taste, Direct-Response Copy, and E-Commerce Conversion Optimization skills.

