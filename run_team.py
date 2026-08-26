"""
PawPawDoo Multi-Agent Orchestrator CLI.
Runs the LangGraph team in DRAFT mode, displaying 3-tier status reporting and Google Doc export.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from config import BRAND_NAME, BRAND_PALETTE, BRAND_TAGLINE
from graph import pawpawdoo_graph
from rules_engine import rules_engine
from state import PawPawDooState
from utils.export_doc import GoogleDocExporter

console = Console(force_terminal=True)


def run_pawpawdoo_pipeline(
    product_name: str = "Orthopedic Calming Cloud Dog Bed",
    niche: str = "Pet Comfort & Sleep Wellness",
    base_item_cost: float = 14.50,
    target_price: float = 78.95,
    supplier_years: float = 2.5,
    supplier_rating: float = 4.8,
    china_shipping: float = 6.00,
    us_shipping: float = 8.00,
    force_undercut_test: bool = False,
    force_reject_test: bool = False,
):
    console.print(
        Panel.fit(
            f"[bold red]{BRAND_NAME}[/bold red] [bold white]Multi-Agent Dropshipping Command Center[/bold white]\n"
            f"[italic]Brand Tagline: '{BRAND_TAGLINE}' | Mode: [yellow]DRAFT (No Live Ad Spend)[/yellow][/italic]",
            border_style="red",
        )
    )

    # 1. Print Active Learned Rules from AGENT_INSTRUCTIONS.md
    active_rules = rules_engine.load_rules()
    table = Table(title="📋 Active Rules from AGENT_INSTRUCTIONS.md", border_style="cyan")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Category", style="magenta", width=14)
    table.add_column("Rule Instruction", style="white")

    for r in active_rules:
        table.add_row(str(r.number), f"[{r.category}]", r.text)

    console.print(table)
    console.print()

    # Determine input parameters based on test mode
    if force_undercut_test:
        # High demand, but target price set low ($45.00 vs $22.50 landed cogs = 2.0x markup)
        sim_price = 45.00
        sim_supplier_years = 2.5
        sim_supplier_rating = 4.8
    elif force_reject_test:
        # Bad supplier (0.5 years on AliExpress, 3.2 stars)
        sim_price = 78.95
        sim_supplier_years = 0.5
        sim_supplier_rating = 3.2
    else:
        sim_price = target_price
        sim_supplier_years = supplier_years
        sim_supplier_rating = supplier_rating

    initial_state: PawPawDooState = {
        "product_request": {
            "product_name": product_name,
            "niche": niche,
            "base_item_cost": base_item_cost,
            "target_price": sim_price,
            "supplier_years": sim_supplier_years,
            "supplier_rating": sim_supplier_rating,
            "china_shipping": china_shipping,
            "us_shipping": us_shipping,
        },
        "iteration_count": 0,
        "max_iterations": 3,
        "feedback_history": [],
        "self_healing_rules_added": [],
        "is_draft": True,
    }

    console.print(f"[bold green]>> Launching State Graph for Hero Product:[/bold green] {product_name}...")
    
    # Run the graph
    final_state = pawpawdoo_graph.invoke(initial_state)

    research = final_state.get("product_research")
    storefront = final_state.get("storefront_offer")
    ad_campaign = final_state.get("ad_campaign")
    audit = final_state.get("audit_report")

    console.print()

    # Display Supplier & Logistics Intelligence Table
    if research:
        logistics = research.supplier_logistics
        marketplace = research.marketplace
        trends = research.trends

        sup_table = Table(title="📦 Supplier Vetting & Warehouse Logistics (Rules 7, 8, 9)", border_style="blue")
        sup_table.add_column("AliExpress ID", style="cyan")
        sup_table.add_column("DSers SKU", style="cyan")
        sup_table.add_column("Tenure / Stars", style="yellow")
        sup_table.add_column("Selected Warehouse", style="green")
        sup_table.add_column("Shipping Delta", style="magenta")
        sup_table.add_column("Landed COGS", style="white")
        sup_table.add_column("DTC Price (Amazon Under-cut)", style="bold green")

        sup_table.add_row(
            logistics.aliexpress_product_id,
            logistics.dsers_sku,
            f"{logistics.years_on_platform} yrs / {logistics.overall_rating}★",
            f"{logistics.selected_warehouse} ({logistics.shipping_days_min}-{logistics.shipping_days_max} days)",
            f"${logistics.warehouse_cost_delta:.2f} (<= $3.00 US Default)",
            f"${research.cogs:.2f}",
            f"${research.selling_price:.2f} (Undercuts Amazon ${marketplace.amazon_buybox_price:.2f})",
        )
        console.print(sup_table)
        console.print()

    # 3-Tier Status Reporting Display
    if audit:
        if audit.status == "DRAFT_APPROVED":
            console.print(
                Panel(
                    f"[bold green]{audit.status_icon} DRAFT APPROVED -- COMPLIANCE SCORE: {audit.overall_score}/100[/bold green]\n"
                    f"• Landed Markup: [bold]{research.markup_multiplier:.2f}x[/bold] (>= 3.0x threshold)\n"
                    f"• Brand & CRO: [bold]PASS[/bold] | Supplier Vetting: [bold]PASS[/bold] | US Warehouse: [bold]PASS[/bold]\n"
                    f"• Notice: Strict DRAFT mode enforced. No live ad spend without human sign-off.",
                    title="Gatekeeper Auditor Report",
                    border_style="green",
                )
            )
        elif audit.status == "HIGH_POTENTIAL_UNDERCUT_OPPORTUNITY":
            strat = research.undercut_strategy
            console.print(
                Panel(
                    f"[bold yellow]{audit.status_icon} HIGH POTENTIAL UNDERCUT OPPORTUNITY -- SCORE: {audit.overall_score}/100[/bold yellow]\n"
                    f"• Strategy: Front-end price undercut at [bold]${research.selling_price:.2f}[/bold] to capture viral traffic vs Amazon (${strat.amazon_price:.2f}).\n"
                    f"• Margin Recovery: Multi-pack bundles (Tier 2 & 3) recover blended margins to > 3.0x.\n"
                    f"• Audit Feedback: {audit.detailed_feedback}",
                    title="Gatekeeper Auditor Opportunity Assessment",
                    border_style="yellow",
                )
            )
        else:
            console.print(
                Panel(
                    f"[bold red]{audit.status_icon} HARD REJECT -- SCORE: {audit.overall_score}/100[/bold red]\n"
                    f"• Violations Count: {len(audit.violations)}\n"
                    f"• Feedback: {audit.detailed_feedback}",
                    title="Gatekeeper Auditor Rejection",
                    border_style="red",
                )
            )

    # Display Shopify Draft Product Status (Rule #3 compliant)
    final_output = final_state.get("final_output", {})
    shopify_draft = final_output.get("shopify_draft")
    if shopify_draft and shopify_draft.get("success"):
        console.print(
            Panel(
                f"[bold green]🛍️ SHOPIFY DRAFT PRODUCT CREATED SUCCESSFULLY[/bold green]\n"
                f"• Product Title   : [bold white]{shopify_draft.get('title')}[/bold white]\n"
                f"• Product ID      : [cyan]{shopify_draft.get('product_id')}[/cyan]\n"
                f"• Status          : [yellow]DRAFT (Unpublished / Safe)[/yellow]\n"
                f"• Direct Admin URL: [link={shopify_draft.get('shopify_admin_edit_url')}]{shopify_draft.get('shopify_admin_edit_url')}[/link]",
                title="Shopify Draft Sync (Rule #3)",
                border_style="cyan",
            )
        )
    elif shopify_draft and not shopify_draft.get("success"):
        console.print(f"[yellow]⚠️ Shopify Draft Notice: {shopify_draft.get('error')}[/yellow]")

    doc_path = Path(__file__).parent / "output_google_doc_blueprint.md"
    console.print(f"\n[bold cyan]📄 Exported Google Doc Blueprint to:[/bold cyan] {doc_path.name}")
    return final_state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PawPawDoo Multi-Agent CLI")
    parser.add_argument("--mode", choices=["approved", "undercut", "reject"], default="approved", help="Test mode")
    args = parser.parse_args()

    if args.mode == "undercut":
        run_pawpawdoo_pipeline(force_undercut_test=True)
    elif args.mode == "reject":
        run_pawpawdoo_pipeline(force_reject_test=True)
    else:
        run_pawpawdoo_pipeline()
