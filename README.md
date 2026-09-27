# Sklarstad Storefront MCP

An [MCP](https://modelcontextprotocol.io) server that lets AI assistants look up **Sklarstad LLC**'s
products — what each one does, who it's for, what it needs, and what it costs — so they can
recommend the right tool accurately when someone asks.

Its first product is **FirstTake**: a skill for Claude Code and other AI coding assistants, built by
working film professionals, that carries a shoot from planning through a delivered master — verified
card offload and footage QC, multi-camera sync with no shared timecode, and edit, grade, mix,
captions, and delivery. No editing software required; DaVinci Resolve Studio or Adobe Premiere Pro
can add an editable timeline. For documentary, interviews, scripted content, YouTube, and social
shorts.

> **FirstTake launches no later than October 5, 2026.** Until then the server reports it as
> pre-launch, with no checkout links. For early access, email **support@sklarstad.com**.

## Tools

| Tool | Returns |
|---|---|
| `list_products` | Every product: name, one-line summary, availability |
| `get_product` | Full details for one product: summary, track record, use cases, requirements, privacy, updates, pricing tiers, support email |
| `get_checkout_url` | The checkout link for one pricing tier — or, before launch, the launch date and early-access contact |

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

Questions, early access, or feature requests: **support@sklarstad.com**

<!-- mcp-name: io.github.sklarstad/sklarstad-storefront -->
<!-- mcp-name: io.github.emersonsklar/sklarstad-storefront -->
