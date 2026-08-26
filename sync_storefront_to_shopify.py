"""
PawPawDoo Storefront & Landing Page Shopify Sync Script.
Syncs the revamped high-converting landing page into Shopify Pages as a Draft page.
"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from adapters.shopify_adapter import ShopifyAdapter
from config import BRAND_NAME, BRAND_TAGLINE

console = Console()


def sync_landing_page_to_shopify():
    console.print(
        Panel.fit(
            f"[bold red]{BRAND_NAME}[/bold red] [bold white]Storefront & Landing Page Shopify Syncer[/bold white]\n"
            f"[italic]Brand Tagline: '{BRAND_TAGLINE}' | Mode: [yellow]DRAFT (Unpublished)[/yellow][/italic]",
            border_style="red",
        )
    )

    landing_html_path = Path(__file__).parent / "storefront" / "index.html"
    if not landing_html_path.exists():
        console.print(f"[bold red]Error:[/bold red] Landing page file {landing_html_path} does not exist.")
        return

    html_content = landing_html_path.read_text(encoding="utf-8")
    adapter = ShopifyAdapter()

    console.print("Syncing revamped landing page to Shopify Pages...")
    res = adapter.create_or_update_page(
        title="PawPawDoo Orthopedic Calming Cloud Dog Bed — High Converting Landing Page",
        body_html=html_content,
        handle="orthopedic-cloud-dog-bed",
        published=False,  # Rule #3 compliance
    )

    if res.get("success"):
        console.print(
            Panel(
                f"[bold green]✨ SHOPIFY LANDING PAGE SYNCED SUCCESSFULLY[/bold green]\n"
                f"• Page Title      : [bold white]{res.get('title')}[/bold white]\n"
                f"• Page ID         : [cyan]{res.get('page_id')}[/cyan]\n"
                f"• Handle          : [yellow]{res.get('handle')}[/yellow]\n"
                f"• Direct Admin URL: [link={res.get('shopify_admin_edit_url')}]{res.get('shopify_admin_edit_url')}[/link]\n"
                f"• Public URL (when published): [link={res.get('public_url')}]{res.get('public_url')}[/link]",
                title="Shopify Page Sync (Rule #3)",
                border_style="cyan",
            )
        )
    else:
        console.print(f"[bold red]Sync Failed:[/bold red] {res.get('error')}")


if __name__ == "__main__":
    sync_landing_page_to_shopify()

