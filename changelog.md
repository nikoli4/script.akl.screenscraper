## 1.3.1

- Updated icon and fanart to the AKL Revival artwork.
- Renamed the artwork assets so Kodi refreshes cached add-on artwork.

## 1.3.0

- Updated the Advanced Kodi Launcher Library Module dependency to version 1.4.0.
- Improved ScreenScraper title-search fallback matching across supported platforms.
- Improved Windows shortcut title matching by reusing the common ScreenScraper search variants.
- Improved candidate handling so ambiguous Windows title matches can be handled by AKL's normal scraper selection flow.
- Added additional conservative title variants for difficult game-name matches.
- Improved Nintendo 3DS fallback matching for titles stored with a 3D suffix.
- Improved scraper log privacy by preventing system artwork URLs and local artwork paths from being written to debug logs.
- Fixed ScreenScraper credential sanitization for logged URLs.
- Fixed the ScreenScraper password setting heading.

## 1.2.1

- Updated the AKL module dependency to version 1.3.1.
- Updated the release metadata to reference changelog.md.

## 1.1.16

- Added Windows `.lnk` game-name scraping using ScreenScraper title searches instead of hashing shortcut files.
- Added improved Windows title matching with punctuation, numbering, leading-article, and manual-search fallbacks.
- Preserved original Windows shortcut titles in AKL metadata.
- Added RPCS3 disc-folder support for Sony PlayStation 3 `PS3_GAME/USRDIR/EBOOT.BIN` entries using the parent game-folder name.
- Added Nintendo Switch ScreenScraper platform mapping.
- Corrected Microsoft Windows / PC Windows ScreenScraper platform mapping.
- Added gameplay video support mapped to AKL Trailer assets.
- Added selected-game cache recovery for metadata and artwork retrieval.
- Improved media asset naming and handling.

# Current
- Updated to new version of AKL
- Support for sources