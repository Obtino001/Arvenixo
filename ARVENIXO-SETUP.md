# Arvenixo Premium Redesign — Setup Guide

Theme work lives in this repo on branch `cursor/arvenixo-premium-redesign`.

## What was rebuilt in theme code

- **Design system** in `assets/custom.css` (ink + gold + paper)
- **Homepage** `templates/index.json` — hero, trust strip, categories, bestsellers, story, FAQ (English)
- **New sections:** `arvenixo-hero`, `arvenixo-categories`, `arvenixo-trust-strip`
- **Header / footer** English trust messaging (no Norwegian MinRobot copy)
- **Collection template** cleaned of vacuum brand circles / model picker
- **PDP** English trust/shipping language + mobile sticky Add to cart
- **Generated assets** in `assets/arvenixo-*.png` (hero + category tiles)

## Shopify Admin checklist (required)

Menus and collections cannot be fully created from theme files alone.

### 1) Navigation (Online Store → Navigation)

**Main menu** (`main-menu`) — suggested structure:

- Home → `/`
- Phone Cases → collection (create or rename from “Phone Cases example products”)
- Beauty Tech → collection
- Smart Tech → collection
- Shop all → `/collections/all`
- About → `/pages/about-us`
- Contact → `/pages/contact`

**Footer menu** (`footer`) — create if missing:

- Shipping policy
- Refund policy
- Privacy policy
- Terms of service
- FAQ (page)
- Contact

### 2) Collections

Create / rename:

| Handle idea | Title | Products |
|---|---|---|
| `phone-cases` | Phone Cases | MagShield, FlexGuard, FlexVault, LuxeStand… |
| `beauty-tech` | Beauty Tech | LumiLift, LumiTherm, LumiEase… |
| `smart-tech` | Smart Tech | cameras, gimbals, gadgets |

Then point homepage category links + menu items to these collections.

### 3) Pages (English)

Update content for:

- About Us — brand story (not generic boilerplate)
- Contact — reply SLA + support@arvenixo.com
- Optional: FAQ, Shipping & Delivery (link from footer)

### 4) Theme settings

- Upload **Arvenixo logo** (replace MinRobot logo currently in `settings_data`)
- Upload favicon
- Set homepage SEO title: `Arvenixo | MagSafe Cases & Beauty Tech`
- Meta description with free shipping + niche
- Disable unused markets/languages if US-only

### 5) Product content cleanup (merchant / ops)

Critical from audit — do in Admin (not only theme):

- Remove OEM / BINZIM / ZhongShan factory FAQ from LumiTherm
- Normalize iPhone variant labels + sort order
- Stop perpetual Sale badges / fake compare-at where not real
- Align review widgets with real reviews only

### 6) Preview & publish

```bash
shopify theme push --development
# or connect GitHub theme sync for this branch
```

Approve on preview theme, then publish.

## Scope reminder

Theme redesign + CRO UX is covered here. Marketing/ads is a separate monthly engagement after launch approval.
