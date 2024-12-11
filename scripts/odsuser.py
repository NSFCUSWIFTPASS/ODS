#! /usr/bin/env python
import argparse
from odsutils import ods_engine

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--ods_file', help="Name of ods json file to read.", default=None)
ap.add_argument('-d', '--defaults', help="Name of json file holding default values or descriptor", default=None)
ap.add_argument('--override', help="Flag to allow new record be added even if failed checking", action='store_true')
ap.add_argument('-q', '--quiet', help="Flag to quiet printing.", action='store_true')
ap.add_argument('--version', help="Version to use", default='latest')
ap.add_argument('--alert', help="Level for checking ('[n]one', '[w]arn', '[e]rror').", default='warn')
# Data file options
ap.add_argument('-f', '--data_file', help="Name of data file to read", default=None)
ap.add_argument('--sep', help="Separator for the data file", default='\s+')
ap.add_argument('--replace_char', help="Replace character in data file column header names", default=None)
ap.add_argument('--header_map', help="Name of json file that maps data file headers to ODS keys", default=None)
# Types of "culling/updating"
ap.add_argument('-u', '--update_el', help="Update flag for above elevation limit)", action='store_true')
ap.add_argument('--el_lim', help="Elevation limit in deg", type=float, default=10.0)
ap.add_argument('--dt_sec', help="Time step in seconds to do elevation check.", type=float, default=120.)
ap.add_argument('-c', '--continuity', help="Check and update based on record continuity", action='store_true')
ap.add_argument('--adjust', help="Adjust start or stop for continuity", choices=['start', 'stop'], default='start')
ap.add_argument('-t', '--time_cull', help="Cull existing ods file on time - 'now' or isoformat", default=False)
ap.add_argument('-i', '--invalid_cull', help="Cull ods of invalid entries", action='store_true')
# Output
ap.add_argument('-w', '--write', help="Write ods to this file name", default=False)
ap.add_argument('-v', '--view', help="View ods", action='store_true')
ap.add_argument('--block', help="Number of ods records to show in each view block", default=7)
ap.add_argument('-s', '--std_show', help="Show the tems of an ODS record", action='store_true')
# ODS fields
ap.add_argument('--site_id', help="ODS field", default=None)
ap.add_argument('--site_lat_deg', help="ODS field", default=None)
ap.add_argument('--site_lon_deg', help="ODS field", default=None)
ap.add_argument('--site_el_m', help="ODS field", default=None)
ap.add_argument('--src_id', help="ODS field", default=None)
ap.add_argument('--src_is_pulsar_bool', help="ODS field", default=None)
ap.add_argument('--corr_integ_time_sec', help="ODS field", default=None)
ap.add_argument('--src_ra_j2000_deg', help="ODS field", default=None)
ap.add_argument('--src_dec_j2000_deg', help="ODS field", default=None)
ap.add_argument('--src_radius', help="ODS field", default=None)
ap.add_argument('--src_start_utc', help="ODS field", default=None)
ap.add_argument('--src_end_utc', help="ODS field", default=None)
ap.add_argument('--slew_sec', help="ODS field", default=None)
ap.add_argument('--trk_rate_dec_deg_per_sec', help="ODS field", default=None)
ap.add_argument('--trk_rate_ra_deg_per_sec', help="ODS field", default=None)
ap.add_argument('--freq_lower_hz', help="ODS field", default=None)
ap.add_argument('--freq_upper_hz', help="ODS field", default=None)
ap.add_argument('--notes', help="ODS field", default=None)

args = ap.parse_args()

ods = ods_engine.ODS(quiet=args.quiet, version=args.version, alert=args.alert)
if args.std_show:
    print(ods.standard)

if args.ods_file:
    ods.read_ods(ods_file_name=args.ods_file)
    if args.defaults is None:
        args.defaults = 'from_ods'  # If nothing else defined, at least use this
ods.get_defaults_dict(args.defaults)

if args.data_file:
    ods.add_from_file(data_file_name=args.data_file, override=args.override,
                         sep=args.sep, replace_char=args.replace_char, header_map=args.header_map)

if args.src_end_utc is not None:  # Assume that this one will always be used outside of defaults
    ods.add_new_record_from_namespace(ns=args, override=args.override)

if args.time_cull:
    ods.cull_ods_by_time(cull_time=args.time_cull)

if args.invalid_cull:
    ods.cull_ods_by_invalid()

if args.continuity:
    ods.update_by_continuity(adjust=args.adjust)

if args.update_el:
    ods.update_by_elevation(el_lim_deg=args.el_lim, dt_sec=args.dt_sec)

if args.view:
    ods.view_ods(number_per_block=args.block)

if args.write:
    ods.write_ods(file_name=args.write)