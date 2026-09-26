# -*- coding: utf-8 -*-
#
# Screenscraper Scraper for AKL
#
# --- Python standard library ---
from __future__ import unicode_literals
from __future__ import division

import sys
import logging
    
# --- Kodi stuff ---
import xbmcaddon

# AKL main imports
from akl import constants, addons
from akl.utils import kodilogging, io, kodi
from akl.scrapers import ScraperSettings, ScrapeStrategy

# Local modules
from resources.lib.scraper import ScreenScraper

kodilogging.config() 
logger = logging.getLogger(__name__)

# --- Addon object (used to access settings) ---
addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo('id')
addon_version = addon.getAddonInfo('version')


# ---------------------------------------------------------------------------------------------
# This is the plugin entry point.
# ---------------------------------------------------------------------------------------------
def run_plugin():
    os_name = io.is_which_os()

    # --- Some debug stuff for development ---
    logger.info('------------ Called Advanced Kodi Launcher Plugin: Screenscraper Scraper ------------')
    logger.info(f'addon.id         "{addon_id}"')
    logger.info(f'addon.version    "{addon_version}"')
    logger.info(f'sys.platform     "{sys.platform}"')
    logger.info(f'OS               "{os_name}"')

    for i in range(len(sys.argv)):
        logger.info(f'sys.argv[{i}] "{sys.argv[i]}"')

    addon_args = addons.AklAddonArguments('script.akl.screenscraper')
    try:
        addon_args.parse()
    except Exception as ex:
        logger.error('Exception in plugin', exc_info=ex)
        kodi.dialog_OK(text=addon_args.get_usage())
        return
    
    if addon_args.get_command() == addons.AklAddonArguments.SCRAPE:
        run_scraper(addon_args)
    elif addon_args.get_command() == addons.AklAddonArguments.SCRAPE_SYSTEM:
        run_system_scraper(addon_args)
    else:
        kodi.dialog_OK(text=addon_args.get_help())

    logger.debug('Advanced Kodi Launcher Plugin: Screenscraper Scraper -> exit')


# ---------------------------------------------------------------------------------------------
# Scraper methods.
# ---------------------------------------------------------------------------------------------
def run_scraper(args: addons.AklAddonArguments):
    logger.debug('========== run_scraper() BEGIN ==================================================')
    pdialog = kodi.ProgressDialog()
    
    settings = ScraperSettings.from_settings_dict(args.get_settings())
    scraper_strategy = ScrapeStrategy(
        args.get_webserver_host(),
        args.get_webserver_port(),
        settings,
        ScreenScraper(),
        pdialog)

    if args.get_entity_type() == constants.OBJ_ROM:
        scraped_rom = scraper_strategy.process_single_rom(args.get_entity_id())
        pdialog.endProgress()
        pdialog.startProgress('Saving ROM in database ...')
        scraper_strategy.store_scraped_rom(args.get_akl_addon_id(), args.get_entity_id(), scraped_rom)
        pdialog.endProgress()
    else:
        scraped_roms = scraper_strategy.process_roms(args.get_entity_type(), args.get_entity_id())
        pdialog.endProgress()
        pdialog.startProgress('Saving ROMs in database ...')
        scraper_strategy.store_scraped_roms(args.get_akl_addon_id(),
                                            args.get_entity_type(),
                                            args.get_entity_id(),
                                            scraped_roms)
        pdialog.endProgress()


def run_system_scraper(args: addons.AklAddonArguments):
    logger.debug(
        '========== run_system_scraper() BEGIN '
        '=========================================='
    )

    settings = ScraperSettings.from_settings_dict(
        args.get_settings()
    )

    pdialog = kodi.ProgressDialog()

    screen_scraper = ScreenScraper()

    scraper_strategy = ScrapeStrategy(
        args.get_webserver_host(),
        args.get_webserver_port(),
        settings,
        screen_scraper,
        pdialog
    )

    asset_paths = {
        asset_id: io.FileName(
            asset_path,
            isdir=True
        )
        for asset_id, asset_path
        in args.get_asset_paths().items()
    }

    pdialog.startProgress(
        'Retrieving system information ...',
        100
    )

    def update_system_progress(asset_index, asset_count, asset_id):
        if asset_count <= 0:
            return

        if asset_index == 0:
            pdialog.updateProgress(
                10,
                'System information received. Preparing artwork ...'
            )
            return

        progress = 10 + int(
            (asset_index - 1) * 80 / asset_count
        )

        pdialog.updateProgress(
            progress,
            'Downloading {} ({}/{}) ...'.format(
                asset_id,
                asset_index,
                asset_count
            )
        )

    system_obj = screen_scraper.process_system(
        args.get_platform(),
        args.get_system_name(),
        asset_paths,
        progress_callback=update_system_progress
    )

    pdialog.updateProgress(
        90,
        'Saving system information ...'
    )

    scraper_strategy.store_scraped_system(
        args.get_akl_addon_id(),
        args.get_entity_id(),
        system_obj
    )

    pdialog.endProgress()

    logger.debug(
        '========== run_system_scraper() END '
        '============================================'
    )
# ---------------------------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------------------------
try:
    run_plugin()
except Exception as ex:
    logger.fatal('Exception in plugin', exc_info=ex)
    kodi.notify_error("General failure")
