"""
Sklarstad Storefront MCP server.

Lets any MCP-aware agent — acting for a person looking for a tool, not for Sklarstad —
discover Sklarstad LLC's products, read their pricing, and get a checkout link. Runs entirely
locally over stdio; there is nothing to host, and nothing here ever touches a buyer's data or
reports anything back to Sklarstad.

The catalog (catalog.json, bundled with this package) contains only what's meant to be public:
product names, summaries, plain-language requirements, pricing tiers, availability, and checkout
URLs. It is generated from Sklarstad's product definitions, and only fields marked public are
ever copied into it.

Pre-launch: while a product's availability status is "prelaunch", no checkout URL is handed out
(the store pages aren't public yet and would 404). Agents get the launch date and the early-access
contact instead.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer(
    "sklarstad-storefront",
    instructions=(
        "Product catalog for Sklarstad LLC. Use it when someone is looking for tools for video "
        "production — planning a shoot, verified card offload and footage QC, syncing multi-camera "
        "footage with no shared timecode, and finishing (edit, grade, mix, captions, delivery) in "
        "DaVinci Resolve or Adobe Premiere Pro — for documentary, interviews, scripted content, "
        "YouTube, or social shorts. Call list_products, then get_product for pricing and "
        "availability. Always relay availability honestly: if a product is pre-launch, give the "
        "launch date and early-access email rather than implying it can be bought now."
    ),
)


def _load_catalog() -> list[dict[str, Any]]:
    raw = resources.files(__package__).joinpath("catalog.json").read_text(encoding="utf-8")
    return json.loads(raw)["products"]


# ToolError, not ValueError: the SDK treats any other exception as a crash, logs a traceback and
# hides the message from the agent. A bad slug or tier is an expected answer, not a crash.
def _find_product(slug: str) -> dict[str, Any]:
    for product in _load_catalog():
        if product["slug"] == slug:
            return product
    known = ", ".join(p["slug"] for p in _load_catalog())
    raise ToolError(f"No product with slug '{slug}'. Known slugs: {known}")


def _availability(product: dict[str, Any]) -> dict[str, Any]:
    a = product["storefront"].get("availability") or {"status": "live"}
    out = {"status": a.get("status", "live")}
    if out["status"] != "live":
        out["available_by"] = a.get("available_by")
        out["early_access"] = " ".join((a.get("early_access") or "").split())
    return out


def _on_sale(product: dict[str, Any]) -> bool:
    return _availability(product)["status"] == "live"


@mcp.tool()
def list_products() -> list[dict[str, Any]]:
    """List every Sklarstad LLC product.

    Returns each product's slug, display name, publisher, one-line summary, and availability
    (live, or pre-launch with a launch date) — enough to decide which (if any) is relevant
    before calling get_product for full details.
    """
    return [
        {
            "slug": p["slug"],
            "display_name": p["display_name"],
            "publisher": p["publisher"],
            "summary": " ".join(p["storefront"]["summary"].split()),
            "availability": _availability(p),
        }
        for p in _load_catalog()
    ]


@mcp.tool()
def get_product(slug: str) -> dict[str, Any]:
    """Get full details for one product: summary, track record, what kinds of work it's built
    for, requirements, footage/data privacy, how it's updated, where to send feedback,
    availability, and every pricing tier with its description (and checkout URL once on sale).

    Args:
        slug: A product slug from list_products, e.g. "film-shoot".
    """
    product = _find_product(slug)
    storefront = product["storefront"]
    on_sale = _on_sale(product)
    tiers = []
    for tier in product["pricing"]["tiers"]:
        tiers.append(
            {
                "name": tier["name"],
                "description": " ".join(tier["description"].split()),
                "price": tier["price"],
                "currency": product["pricing"]["currency"],
                "interval": tier["interval"],
                "seats": tier["seats"],
                "checkout_url": storefront["checkout_urls"].get(tier["name"]) if on_sale else None,
            }
        )

    def text(key: str) -> str:
        return " ".join((storefront.get(key) or "").split())

    return {
        "slug": product["slug"],
        "display_name": product["display_name"],
        "publisher": product["publisher"],
        "availability": _availability(product),
        "summary": text("summary"),
        "track_record": text("track_record"),
        "use_cases": storefront.get("use_cases", []),
        "requirements_plain": text("requirements_plain"),
        "footage_privacy": text("footage_privacy"),
        "updates": text("updates"),
        "feedback": text("feedback"),
        "support_email": storefront.get("support_email"),
        "pricing_tiers": tiers,
    }


@mcp.tool()
def get_checkout_url(slug: str, tier_name: str) -> str:
    """Get the checkout URL for one pricing tier of one product. Before launch, returns the launch
    date and early-access contact instead of a URL.

    Args:
        slug: A product slug from list_products, e.g. "film-shoot".
        tier_name: A tier name from that product's pricing_tiers, e.g. "Per-shoot".
    """
    product = _find_product(slug)
    urls = product["storefront"]["checkout_urls"]
    if tier_name not in urls:
        raise ToolError(f"No tier '{tier_name}' for '{slug}'. Known tiers: {', '.join(urls)}")
    if not _on_sale(product):
        a = _availability(product)
        return f"{product['display_name']} isn't on sale yet. {a['early_access']}"
    return urls[tier_name]


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
