# Credits Update Note

All Python code files have been updated with new credits:
- Modified by @Shadowedtomb and @Hail_Arka

## Module Rename

The main module has been renamed from `TechVJ` to `HailArka`:
- Directory: `TechVJ/` → `HailArka/`
- All imports updated: `from TechVJ.*` → `from HailArka.*`
- Bot class: `TechVJBot` → `HailArkaBot`
- Session name: `TechVJBot` → `HailArkaBot`
- Database name: `techvjclonefilterbot` → `hailarkafilterbot`
- Collection name: `vjcollection` → `hailarkacollection`

## HTML Template Files

The following HTML template files still contain old social media links and need manual updating if you want to customize them:

- `HailArka/template/req.html`
- `HailArka/template/dl.html`

These files contain references to:
- YouTube: @Tech_VJ
- Telegram: @kingvj01, @vj_bots
- Instagram: tech.vj
- GitHub: VJBots

You can update these links to your own social media accounts by editing the HTML files directly.

## Configuration

The default configuration in `info.py` has been updated to:
- CHNL_LNK: https://t.me/shadowedtomb
- SUPPORT_CHAT: shadowedtomb
- OWNER_LNK: https://t.me/Hail_Arka
- SESSION: HailArkaBot
- DATABASE_NAME: hailarkafilterbot
- COLLECTION_NAME: hailarkacollection

You can override these by setting environment variables.
