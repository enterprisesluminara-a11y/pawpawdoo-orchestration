"""
Automated Verification Suite for PawPawDoo Multi-Agent Architecture, Adapters & 3-Tier Status Engine.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE, MIN_MARKUP_MULTIPLIER
from graph import pawpawdoo_graph
from rules_engine import rules_engine
from state import PawPawDooState


class TestPawPawDooMultiAgent(unittest.TestCase):
    def setUp(self):
        self.instructions_path = Path(__file__).parent / "AGENT_INSTRUCTIONS.md"
        self.assertTrue(self.instructions_path.exists(), "AGENT_INSTRUCTIONS.md must exist")

    def test_01_rules_engine_loading(self):
        """Verify all 10 learned rules and categories are parsed correctly."""
        rules = rules_engine.load_rules()
        self.assertGreaterEqual(len(rules), 10, "Should have at least 10 active rules")
        categories = {r.category for r in rules}
        self.assertIn("BRAND", categories)
        self.assertIn("PROCESS", categories)
        self.assertIn("CRO", categories)
        self.assertIn("FINANCE", categories)
        self.assertIn("PRICING", categories)
        self.assertIn("SUPPLIER", categories)
        self.assertIn("LOGISTICS", categories)
        self.assertIn("DATA", categories)
        self.assertIn("OPPORTUNITY", categories)

    def test_02_standard_hero_product_run(self):
        """Verify full graph execution with 🟢 DRAFT_APPROVED status, US warehouse, and DSers mapping."""
        initial_state: PawPawDooState = {
            "product_request": {
                "product_name": "Orthopedic Calming Cloud Dog Bed",
                "niche": "Pet Comfort & Sleep Wellness",
                "base_item_cost": 14.50,
                "target_price": 78.95,
                "supplier_years": 2.5,
                "supplier_rating": 4.8,
                "china_shipping": 6.00,
                "us_shipping": 8.00,
            },
            "iteration_count": 0,
            "max_iterations": 3,
            "feedback_history": [],
            "self_healing_rules_added": [],
            "is_draft": True,
        }

        final_state = pawpawdoo_graph.invoke(initial_state)

        # Assert all agent components are populated
        research = final_state.get("product_research")
        storefront = final_state.get("storefront_offer")
        ad_campaign = final_state.get("ad_campaign")
        audit = final_state.get("audit_report")

        self.assertIsNotNone(research)
        self.assertIsNotNone(storefront)
        self.assertIsNotNone(ad_campaign)
        self.assertIsNotNone(audit)

        # 3-Tier Status Assertions
        self.assertEqual(audit.status, "DRAFT_APPROVED")
        self.assertEqual(audit.status_icon, "🟢")
        self.assertTrue(audit.passed)
        self.assertEqual(audit.overall_score, 100)

        # Rule #7: Supplier Vetting
        logistics = research.supplier_logistics
        self.assertTrue(logistics.vetting_passed)
        self.assertGreaterEqual(logistics.years_on_platform, 1.0)
        self.assertGreaterEqual(logistics.overall_rating, 4.0)

        # Rule #8: US Warehouse selected because delta is $2.00 <= $3.00
        self.assertEqual(logistics.selected_warehouse, "US")
        self.assertLessEqual(logistics.warehouse_cost_delta, 3.00)

        # Rule #9: AliExpress Product ID & DSers SKU mapped
        self.assertTrue(len(logistics.aliexpress_product_id) > 5)
        self.assertTrue(logistics.dsers_sku.startswith("DS-PPD-"))

        # Rule #6: Undercuts Amazon/eBay while markup >= 3.0x
        marketplace = research.marketplace
        self.assertLess(research.selling_price, marketplace.amazon_buybox_price)
        self.assertGreaterEqual(research.markup_multiplier, MIN_MARKUP_MULTIPLIER)

    def test_03_undercut_opportunity_tier(self):
        """Verify 🟠 HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY (Rule #10) triggers on high-demand lower initial margin."""
        opportunity_state: PawPawDooState = {
            "product_request": {
                "product_name": "Orthopedic Calming Cloud Dog Bed",
                "niche": "Pet Comfort & Sleep Wellness",
                "base_item_cost": 14.50,
                "target_price": 45.00,  # Below 3.0x landed markup ($45 / $22.50 = 2.0x)
                "supplier_years": 2.5,
                "supplier_rating": 4.8,
                "china_shipping": 6.00,
                "us_shipping": 8.00,
            },
            "iteration_count": 0,
            "max_iterations": 3,
            "feedback_history": [],
            "self_healing_rules_added": [],
            "is_draft": True,
        }

        final_state = pawpawdoo_graph.invoke(opportunity_state)
        audit = final_state.get("audit_report")
        research = final_state.get("product_research")

        self.assertEqual(audit.status, "HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY")
        self.assertEqual(audit.status_icon, "🟠")
        self.assertTrue(audit.passed)
        self.assertIsNotNone(research.undercut_strategy)
        self.assertTrue(research.undercut_strategy.is_applicable)
        self.assertGreaterEqual(len(research.undercut_strategy.bundle_margin_recovery), 2)

    def test_04_hard_reject_tier(self):
        """Verify 🔴 HARD_REJECT when supplier vetting fails (Rule #7)."""
        bad_supplier_state: PawPawDooState = {
            "product_request": {
                "product_name": "Unvetted Pet Leash",
                "niche": "Pet Accessories",
                "base_item_cost": 5.00,
                "target_price": 25.00,
                "supplier_years": 0.3,  # Failed Rule 7 (< 1.0 yr)
                "supplier_rating": 3.4,  # Failed Rule 7 (< 4.0 stars)
                "china_shipping": 4.00,
                "us_shipping": 6.00,
            },
            "iteration_count": 0,
            "max_iterations": 1,
            "feedback_history": [],
            "self_healing_rules_added": [],
            "is_draft": True,
        }

        final_state = pawpawdoo_graph.invoke(bad_supplier_state)
        audit = final_state.get("audit_report")

        self.assertEqual(audit.status, "HARD_REJECT")
        self.assertEqual(audit.status_icon, "🔴")
        self.assertFalse(audit.passed)
        self.assertFalse(audit.supplier_vetting_check)

    def test_05_google_doc_export(self):
        """Verify Google Doc structured markdown blueprint is created and non-empty."""
        doc_file = Path(__file__).parent / "output_google_doc_blueprint.md"
        self.assertTrue(doc_file.exists())
        content = doc_file.read_text(encoding="utf-8")
        self.assertIn("PAWPAWDOO PRODUCT LAUNCH BLUEPRINT", content)
        self.assertIn("DSERS / SHOPIFY LOGISTICS", content)
        self.assertIn("VIRAL DIRECT-RESPONSE VIDEO AD FRAMEWORKS", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
