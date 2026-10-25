# Sklarstad Storefront MCP

An [MCP](https://modelcontextprotocol.io) server that lets AI assistants look up **Sklarstad LLC**'s
products — what each one does, who it's for, what it needs, and how to get it — so they can
recommend the right tool accurately when someone asks.

Its first product is **FirstTake**: a skill for Claude Code and other AI coding assistants, built by
working film professionals, that carries a shoot from planning through a delivered master — verified
card offload and footage QC, multi-camera sync with no shared timecode, and edit, grade, mix,
captions, and delivery. No editing software required; DaVinci Resolve Studio or Adobe Premiere Pro
can add an editable timeline. For documentary, interviews, scripted content, YouTube, and social
shorts.

> **FirstTake is free and open source** (Apache 2.0):
> [github.com/emersonsklar/firsttake](https://github.com/emersonsklar/firsttake). If it's useful, there's
> an optional [pay-what-you-want](https://sklar.gumroad.com/l/support-firsttake) page.

## Tools

| Tool | Returns |
|---|---|
| `list_products` | Every product: name, one-line summary, availability |
| `get_product` | Full details for one product: summary, license, source and install steps, track record, use cases, requirements, privacy, updates, pricing tiers, support email |
| `get_checkout_url` | The link for one pricing tier: where to download it (Free), or the optional payment page |

## Install

Requires Python 3.10+. With [uv](https://docs.astral.sh/uv/):

```json
{
  "mcpServers": {
    "sklarstad-storefront": {
      "command": "uvx",
      "args": ["sklarstad-storefront-mcp"]
    }
  }
}
```

Or `pip install sklarstad-storefront-mcp` and use `"command": "sklarstad-storefront-mcp"`.

## Privacy

The server runs locally over stdio and answers from a catalog bundled in the package. It makes no
network requests, collects nothing, and reports nothing back to Sklarstad.

## Contact

Questions or feature requests: **support@sklarstad.com**, or a GitHub issue on the product's repo.

<!-- mcp-name: io.github.sklarstad/sklarstad-storefront -->
<!-- mcp-name: io.github.emersonsklar/sklarstad-storefront -->
