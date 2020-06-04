#!/usr/bin/env python

#####################################################################################################################################################################
# Copyright (c) 2017 by Cisco Systems, Inc.  #
#
# Date       Who               Version Description
#----------- ----------------- ------- --------------------------------------------------------------------------------------------------------------------------
# 02/20/2019 Edward Mazurek    v1.0    Created
#
# 02/15/2020 Edward Mazurek    v1.1    Added support for FC port-channels
# 04/16/2020 Edward Mazurek    v1.2    Added --errorsonly parameter
# 04/16/2020 Edward Mazurek    v1.3    Changed "--statistics" to "--general-stats", "--physical-errors" to "--link-stats" and "congestion-errors" to "--congestion-stats" 
# 04/18/2020 Edward Mazurek    v1.4    Added OLS, LRR, BB_SCs, BB_SCr to link stats and LR while active to congestion stats
# 04/20/2020 Edward Mazurek    v1.5    Added version in --help 
# 04/21/2020 Edward Mazurek    v1.6    Added --transceiver-stats, --sfp-stats, --transceiver-detail-stats,  --sfp-detail-stats
# 06/04/2020 Edward Mazurek    v1.7    Added support for the new format of the "show interface counters detailed" command in NX-OS 8.4(2)
# 06/04/2020 Edward Mazurek    v1.7    Removed framing errors since HW does not increment this counter
#####################################################################################################################################################################

import sys
sys.path.append('/isan/bin/cli-scripts/')
import argparse
import json
from prettytable import *

import cli

def validateArgs (args) : 

   if  int(args.type_link_stats) + int(args.type_congestion_stats) + int(args.type_general_stats) + int(args.type_sfp_stats) + int(args.type_sfp_detail_stats) == 0:
       args.type_link_stats = True
       #print('Defaulting to link stats')
   elif  int(args.type_link_stats) + int(args.type_congestion_stats) + int(args.type_general_stats) + int(args.type_sfp_stats) + int(args.type_sfp_detail_stats) > 1:
        print "\n Please choose a single type to display via --general-stats or --link-stats or --congestion-stats or --transceiver(sfp)-stats or --transceiver(sfp)-detail-stats\n"
        return False

   if args.fc_interface :
        try :
            intf_range = args.fc_interface
        except ValueError:
            print "Please enter a valid fc or port-channel interface, interface range or interface list"
            return False
   else:
       intf_range = ''
   return True
##############################################################################
# Main
##############################################################################
global intf_range
# argument parsing
parser = argparse.ArgumentParser(prog='show_int_tabular', description='show_int_tabular v1.7')
parser.add_argument('--version', action='version', help='version', version='%(prog)s 1.0')
parser.add_argument('fc_interface', nargs='*', default = '', help='fc interface, port-channel interface, interface range or interface list')
parser.add_argument('--general-stats', action="store_true", dest='type_general_stats', help = 'Display general statistics (non errors).')
parser.add_argument('--link-stats', action="store_true",  dest='type_link_stats', help = 'Display physical link statistics. Default')
parser.add_argument('--congestion-stats', action="store_true",  dest='type_congestion_stats', help = 'Display congestion statistics')
parser.add_argument('--transceiver-stats', action="store_true",  dest='type_sfp_stats', help = 'Display transceiver(SFP) statistics')
parser.add_argument('--sfp-stats', action="store_true",  dest='type_sfp_stats', help = 'Display transceiver(SFP) statistics')
parser.add_argument('--transceiver-detail-stats', action="store_true",  dest='type_sfp_detail_stats', help = 'Display transceiver(SFP) detailed statistics')
parser.add_argument('--sfp-detail-stats', action="store_true",  dest='type_sfp_detail_stats', help = 'Display transceiver(SFP) detailed statistics')
parser.add_argument('--e', action="store_true", dest='filter_e_port', help='Display only (T)E ports in interface range or list')
parser.add_argument('--f', action="store_true", dest='filter_f_port', help='Display only (T)F ports in interface range or list')
parser.add_argument('--np', action="store_true", dest='filter_np_port', help='Display only (T)NP ports in interface range or list')
parser.add_argument('--edge', action="store_true", dest='filter_edge_port', help='Display only logical-type edge ports in interface range or list')
parser.add_argument('--core', action="store_true", dest='filter_core_port', help='Display only logical-type core ports in interface range or list')
parser.add_argument('--errorsonly', action='store_true', dest='filter_errorsonly', help='Display only interfaces with non-zero counts.')

#
# Handle arguments
#
args = parser.parse_args()

if not validateArgs (args) :
    sys.exit() 

#if not (args.type_link_stats or args.type_congestion_stats or args.type_general_stats):
#    args.type_link_stats = True

if len(args.fc_interface) > 0:
    intf_range = args.fc_interface[0] + ' '
else:
    intf_range = ''

#if args.filter_e_port == True:
#print('args.filter_e_port: ' + str(args.filter_e_port))

#
# Issue show interface brief if any filter is specified
#
# port_type_filter == True indicates one of the port types(e, f, np, core, edge) is requested
#
if args.filter_e_port | args.filter_f_port | args.filter_np_port | args.filter_edge_port | args.filter_core_port:
    port_type_filter = True
    show_int_brief_cmd = 'show interface ' + str(intf_range) + 'brief'
    try :
        show_int_brief_str = cli.cli(show_int_brief_cmd)
    except :
        print('Error issuing ' + show_int_brief_cmd + ' command...')
        pass
    show_int_brief_dict = {}
    show_int_brief_list = show_int_brief_str.splitlines()
    #print('show_int_brief_list: ' + str(len(show_int_brief_list)) + ' bytes')
    for line in show_int_brief_list:
        #print('show interface brief line: ' + line)
        line_toks = line.split()
        #if len(line_toks) >= 1:
            #print('line_toks[0]:' + line_toks[0])
            #print("line.startswith('fc'): " + str(line.startswith('fc')))
            #print('split: ' + str(line_toks[0].split('/')))
        if (line.startswith('fc') and len(line_toks[0].split('/')) == 2):
            intf = line_toks[0]
            show_int_brief_dict[intf] = {}
            show_int_brief_dict[intf]['oper_mode'] = line_toks[6]
            show_int_brief_dict[intf]['logical_type'] = line_toks[9]
            #print('Adding intf: ' + intf + ' to show_int_brief_dict: oper_mode: ' + line_toks[6] + ' logical_type: ' + line_toks[9])
        elif line.startswith('port-channel'):
            intf = line_toks[0]
            show_int_brief_dict[intf] = {}
            show_int_brief_dict[intf]['oper_mode'] = line_toks[4]
            show_int_brief_dict[intf]['logical_type'] = line_toks[7]
            #print('Adding intf: ' + intf + ' to show_int_brief_dict: oper_mode: ' + line_toks[6] + ' logical_type: ' + line_toks[9])
else:
    port_type_filter = False
    
#
# Determine NX-OS version
# At 8.4(2) the output of the "show interface counters details" command has completely changed
#
ver_maj = ''
ver_min = ''
show_int_counter_detail_new = False
try :
    show_ver_str = cli.cli('show version')
except :
    print('Error issuing "show version" command...')
    pass
show_ver_list = show_ver_str.splitlines()
for ver_entry in show_ver_list:
    ver_entry_toks = ver_entry.split()
    if len(ver_entry_toks) >= 3 and ver_entry_toks[0] == 'system:' and ver_entry_toks[1] == 'version':
        version = ver_entry_toks[2]
        ver_maj_toks = version.split('.')
        ver_maj = ver_maj_toks[0]
        ver_min_toks = ver_maj_toks[1].split('(')
        ver_min = ver_min_toks[0]
        ver_maint_toks = ver_min_toks[1].split(')')
        ver_maint = ver_maint_toks[0]
        #print('ver_maj: ' + ver_maj + ' ver_min: ' + ver_min + ' ver_maint: ' + ver_maint)
        if int(ver_maj) > 8 or (int(ver_maj) == 8 and (int(ver_min) > 4 or (int(ver_min) == 4 and ver_maint >= '2'))):
            show_int_counter_detail_new = True

#
# Initialize show_int_varibles_dict where all variables are stored
#
show_int_variables_dict = {}
#
# If general-stats, link-stats or congestion-stats issue show interface counters detailed command
#
if args.type_link_stats or args.type_congestion_stats or args.type_general_stats:
    show_int_str = ""  
    #print('intf_range: ' + str(intf_range))
    #print('show interface command: ' + 'show interface ' + str(intf_range) + ' counters detail')
    show_int_cmd = 'show interface ' + str(intf_range) + 'counters detailed'
    try :
        show_int_str = cli.cli(show_int_cmd)
    except :
        print('Error issuing ' + show_int_cmd + ' command...')
        pass
    
    intf_list = []
    show_int_list = show_int_str.splitlines()
    intf = ''
    #
    # Counter_list = [
    #                [number of tokens on line, [[Heading, [%variable_name, match keyword 1, match keyword 2, ..., match keyword n]]]],
    #                ...
    #                ]
    #
    # --link-stats
    #
    if args.type_link_stats:
        header_line = 'Link Stats:'
        if show_int_counter_detail_new:
            counter_list = [ 
                            [[4], [['Link Failure', ['Rx', 'Link', 'failures:', '%intf_link_failures:']]]],
                            [[4], [['Sync Loss', ['Rx', 'Sync' , 'losses:', '%intf_sync_losses']]]], 
                            [[4], [['Signal Loss', ['Rx', 'Signal', 'losses:', '%intf_sig_loss']]]],
                            [[5], [['Invalid Words', ['Rx', 'Invalid', 'transmission', 'words:', '%intf_invalid_tx_words']]]],
                            [[4], [['Invalid CRC', ['Rx', 'Invalid', 'CRCs:', '%intf_invalid_crcs']]]],
                            [[4], [['NOS Rx', ['Rx', 'Non-Operational', 'Sequences(NOS):', '%intf_nos_rx']]]],
                            [[4], [['NOS Tx', ['Tx', 'Non-Operational', 'Sequences(NOS):', '%intf_nos_tx']]]],
                            [[4], [['OLS Rx', ['Rx', 'Offline', 'Sequences(OLS):', '%intf_ols_rx']]]],
                            [[4], [['OLS Tx', ['Tx', 'Offline', 'Sequences(OLS):', '%intf_ols_tx']]]],
                            [[5], [['LRR Rx', ['Rx', 'Link', 'Reset', 'Responses(LRR):', '%intf_lrr_rx']]]],
                            [[5], [['LRR Tx', ['Tx', 'Link', 'Reset', 'Responses(LRR):', '%intf_lrr_tx']]]],
                            [[5], [['FEC corrected', ['Rx', 'FEC', 'corrected', 'blocks:', '%intf_fec_corrected']]]],
                            [[5], [['FEC uncorrected', ['Rx', 'FEC', 'uncorrected', 'blocks:', '%intf_fec_uncorrected']]]],
                            [[5], [['BB_SCs', ['BB_SCs', 'credit', 'resend', 'actions:', '%intf_bbscs']]]], 
                            [[6], [['BB_SCr', ['BB_SCr', 'Tx', 'credit', 'increment', 'actions:', '%intf_bbscr']]]],
                            ]
        
        else:
            counter_list = [ 
                            [[9], [['Link Failure', ['%intf_link_failures', 'link', 'failures,']], ['Sync Loss', ['.', '.', '.', '%intf_sync_losses', 'sync' , 'losses,']], ['Signal Loss', ['.', '.', '.', '.', '.', '.','%intf_sig_loss', 'signal', 'losses']]]],
                            [[4], [['Invalid Words', ['%intf_invalid_tx_words', 'invalid', 'transmission', 'words']]]],
                            [[6], [['Invalid CRC', ['%intf_invalid_crcs', 'invalid', 'CRCs,']]]],
                            [[4], [['NOS Rx', ['%intf_nos_rx', 'non-operational', 'sequences', 'received']]]],
                            [[4], [['NOS Tx', ['%intf_nos_tx', 'non-operational', 'sequences', 'transmitted']]]],
                            [[5], [['OLS Rx', ['%intf_ols_rx', 'Offline', 'Sequence', 'errors', 'received']]]],
                            [[5], [['OLS Tx', ['%intf_ols_tx', 'Offline', 'Sequence', 'errors', 'transmitted']]]],
                            [[5], [['LRR Rx', ['%intf_lrr_rx', 'link', 'reset', 'responses', 'received']]]],
                            [[5], [['LRR Tx', ['%intf_lrr_tx', 'link', 'reset', 'responses', 'transmitted']]]],
                            [[4], [['FEC corrected', ['%intf_fec_corrected', 'fec', 'corrected', 'blocks']]]],
                            [[4], [['FEC uncorrected', ['%intf_fec_uncorrected', 'fec', 'uncorrected', 'blocks']]]],
                            [[11], [['BB_SCs', ['%intf_bbscs', 'BB_SCs', 'credit', 'resend', 'actions,']], ['BB_SCr', ['.', '.', '.', '.', '.', '%intf_bbscr', 'BB_SCr', 'Tx', 'credit', 'increment', 'actions']]]],
                            ]
    #       
    # --congestion-stats
    #
    elif args.type_congestion_stats:
        header_line = 'Congestion Stats:'
        if show_int_counter_detail_new:
            counter_list = [
                            [[7], [['TBBZ', ['Tx',  'B2B', 'credit', 'transitions', 'to', 'zero:', '%intf_tbbz']]]],
                            [[7], [['RBBZ', ['Rx', 'B2B', 'credit', 'transitions', 'to', 'zero:', '%intf_rbbz']]]],
                            [[9], [['TxWait', ['TxWait', '2.5us', 'due', 'to', 'lack', 'of', 'transmit', 'credits:', '%intf_txwait', ]]]],
                            [[4], [['Timeout Discards', ['Timeout', 'discards:', '%intf_timeout_discards']]]], 
                            [[4], [['Credit Loss', ['Tx', 'Credit' , 'loss:', '%intf_credit_loss']]]],
                            [[8], [['Active LR Rx', ['Rx', 'Link', 'Reset(LR)', 'while', 'link', 'is', 'active:', '%intf_lr_rx_act']]]],
                            [[8], [['Active LR Tx', ['Tx', 'Link', 'Reset(LR)', 'while', 'link', 'is', 'active:', '%intf_lr_tx_act']]]],
                            [[5], [['LRR Rx', ['Rx', 'Link', 'Reset', 'Responses(LRR):', '%intf_lrr_rx']]]],
                            [[5], [['LRR Tx', ['Tx', 'Link', 'Reset', 'Responses(LRR):', '%intf_lrr_tx']]]],
                           ]
        else:
            counter_list = [
                            [[7], [['TBBZ', ['%intf_tbbz', 'Transmit',  'B2B', 'credit', 'transitions', 'to', 'zero']]]],
                            [[7], [['RBBZ', ['%intf_rbbz', 'Receive', 'B2B', 'credit', 'transitions', 'to', 'zero']]]],
                            [[9], [['TxWait', ['%intf_txwait', '2.5us', 'TxWait', 'due', 'to', 'lack', 'of', 'transmit', 'credits']]]],
                            [[6], [['Timeout Discards', ['%intf_timeout_discards', 'timeout', 'discards,']], ['Credit Loss', ['.', '.', '.', '%intf_credit_loss', 'credit' , 'loss']]]],
                            [[8], [['Active LR Rx', ['%intf_lr_rx_act', 'link', 'reset', 'received', 'while', 'link', 'is', 'active']]]],
                            [[8], [['Active LR Tx', ['%intf_lr_tx_act', 'link', 'reset', 'transmitted', 'while', 'link', 'is', 'active']]]],
                            [[5], [['LRR Rx', ['%intf_lrr_rx', 'link', 'reset', 'responses', 'received']]]],
                            [[5], [['LRR Tx', ['%intf_lrr_tx', 'link', 'reset', 'responses', 'transmitted']]]],
                           ]
    #
    # --general-stats
    #  
    else:
        header_line = 'General Stats:'
        if show_int_counter_detail_new:
            counter_list = [
        #                   [5, [['Frames Rx',['%intf_frames_received', 'frames,', '.', 'bytes', 'received']], ['Bytes Rx', ['.', '.', '%intf_bytes_received', 'bytes', 'received']]]], 
        #                   [5, [['Frames Tx', ['%intf_frames_transmitted', 'frames,', '.', 'bytes', 'transmitted']],   ['Bytes Tx', ['.', '.', '%intf_bytes_transmitted', 'bytes', 'transmitted']]]],
        #                   [6, [['Class 3 Frames Rx', ['%intf_class_3_frames_received', 'class-3', 'frames,', '.', 'bytes', 'received']], ['Class 3 Bytes Rx', ['.', 'class-3', 'frames,', '%intf_class_3_bytes_received', 'bytes', 'received']]]],
        #                   [6, [['Class 3 Frames Tx', ['%intf_class_3_frames_transmitted', 'class-3', 'frames,', '.', 'bytes', 'transmitted']], ['Class 3 Bytes Tx', ['.', 'class-3', 'frames,', '%intf_class_3_bytes_transmitted', 'bytes', 'transmitted']]]],
        #                   [6, [['Class 2 Frames Rx', ['%intf_class_2_frames_received', 'class-2', 'frames,', '.', 'bytes', 'received']], ['Class 2 Bytes Rx', ['.', 'class-2', 'frames,', '%intf_class_2_bytes_received', 'bytes', 'received']]]],
        #                   [6, [['Class 2 Frames Tx', ['%intf_class_2_frames_transmitted', 'class-2', 'frames,', '.', 'bytes', 'transmitted']], ['Class 2 Bytes Tx', ['.', 'class-2', 'frames,', '%intf_class_2_bytes_transmitted', 'bytes', 'transmitted']]]],
                            [[4], [['Frames Rx',['Rx', 'total', 'frames:', '%intf_frames_received']]]], 
                            [[4], [['Frames Tx', ['Tx', 'total', 'frames:', '%intf_frames_transmitted',]]]],
                            [[4], [['C3 Frames Rx', ['Rx', 'class-3', 'frames:', '%intf_class_3_frames_received']]]],
                            [[4], [['C3 Frames Tx', ['Tx', 'class-3', 'frames:', '%intf_class_3_frames_transmitted']]]],
                            [[4], [['C2 Frames Rx', ['Rx', 'class-2', 'frames:', '%intf_class_2_frames_received']]]],
                            [[4], [['C2 Frames Tx', ['Tx', 'class-2', 'frames:', '%intf_class_2_frames_transmitted']]]],
                            [[4], [['CF Frames Rx', ['Rx', 'class-f', 'frames:', '%intf_class_f_frames_received']]]],
                            [[4], [['CF Frames Tx', ['Tx', 'class-f', 'frames:', '%intf_class_f_frames_transmitted']]]],
                            [[4], [['Mcast Frames Rx', ['Rx', 'total', 'multicast:', '%intf_multicast_frames_received',]]]], 
                            [[4], [['Mcast Frames Tx', ['Tx', 'total', 'multicast:', '%intf_multicast_frames_transmitted']]]],
                            [[4], [['Bcast Frames Rx', ['Rx', 'total', 'broadcast:', '%intf_broadcast_frames_received',]]]], 
                            [[4], [['Bcast Frames Tx', ['Tx', 'total', 'broadcast:', '%intf_broadcast_frames_transmitted']]]],
                            [[4], [['Ucast Frames Rx', ['Rx', 'total', 'unicast:', '%intf_unicast_frames_received',]]]], 
                            [[4], [['Ucast Frames Tx', ['Tx', 'total', 'unicast:', '%intf_unicast_frames_transmitted']]]],
                           ]
        else:
            counter_list = [
        #                   [5, [['Frames Rx',['%intf_frames_received', 'frames,', '.', 'bytes', 'received']], ['Bytes Rx', ['.', '.', '%intf_bytes_received', 'bytes', 'received']]]], 
        #                   [5, [['Frames Tx', ['%intf_frames_transmitted', 'frames,', '.', 'bytes', 'transmitted']],   ['Bytes Tx', ['.', '.', '%intf_bytes_transmitted', 'bytes', 'transmitted']]]],
        #                   [6, [['Class 3 Frames Rx', ['%intf_class_3_frames_received', 'class-3', 'frames,', '.', 'bytes', 'received']], ['Class 3 Bytes Rx', ['.', 'class-3', 'frames,', '%intf_class_3_bytes_received', 'bytes', 'received']]]],
        #                   [6, [['Class 3 Frames Tx', ['%intf_class_3_frames_transmitted', 'class-3', 'frames,', '.', 'bytes', 'transmitted']], ['Class 3 Bytes Tx', ['.', 'class-3', 'frames,', '%intf_class_3_bytes_transmitted', 'bytes', 'transmitted']]]],
        #                   [6, [['Class 2 Frames Rx', ['%intf_class_2_frames_received', 'class-2', 'frames,', '.', 'bytes', 'received']], ['Class 2 Bytes Rx', ['.', 'class-2', 'frames,', '%intf_class_2_bytes_received', 'bytes', 'received']]]],
        #                   [6, [['Class 2 Frames Tx', ['%intf_class_2_frames_transmitted', 'class-2', 'frames,', '.', 'bytes', 'transmitted']], ['Class 2 Bytes Tx', ['.', 'class-2', 'frames,', '%intf_class_2_bytes_transmitted', 'bytes', 'transmitted']]]],
                            [[5], [['Frames Rx',['%intf_frames_received', 'frames,', '.', 'bytes', 'received']]]], 
                            [[5], [['Frames Tx', ['%intf_frames_transmitted', 'frames,', '.', 'bytes', 'transmitted']]]],
                            [[6], [['C3 Frames Rx', ['%intf_class_3_frames_received', 'class-3', 'frames,', '.', 'bytes', 'received']]]],
                            [[6], [['C3 Frames Tx', ['%intf_class_3_frames_transmitted', 'class-3', 'frames,', '.', 'bytes', 'transmitted']]]],
                            [[6], [['C2 Frames Rx', ['%intf_class_2_frames_received', 'class-2', 'frames,', '.', 'bytes', 'received']]]],
                            [[6], [['C2 Frames Tx', ['%intf_class_2_frames_transmitted', 'class-2', 'frames,', '.', 'bytes', 'transmitted']]]],
                            [[6], [['CF Frames Rx', ['%intf_class_f_frames_received', 'class-f', 'frames,', '.', 'bytes', 'received']]]],
                            [[6], [['CF Frames Tx', ['%intf_class_f_frames_transmitted', 'class-f', 'frames,', '.', 'bytes', 'transmitted']]]],
                            [[6], [['Mcast Frames Rx', ['%intf_multicast_frames_received', 'multicast', 'packets', 'received,']], ['Mcast Frames Tx', ['.', 'multicast', 'packets', '.', '%intf_multicast_frames_transmitted', 'transmitted']]]],
                            [[6], [['Bcast Frames Rx', ['%intf_broadcast_frames_received', 'broadcast', 'packets', 'received,']], ['Bcast Frames Tx', ['.', 'broadcast', 'packets', '.', '%intf_broadcast_frames_transmitted', 'transmitted']]]],
                            [[6], [['Ucast Frames Rx', ['%intf_unicast_frames_received', 'unicast', 'packets', 'received,']], ['Ucast Frames Tx', ['.', 'unicast', 'packets', '.', '%intf_unicast_frames_transmitted', 'transmitted']]]],
                           ]
      
#
# --transceiver-stats
# --sfp-stats
#
else:
    show_int_str = ""  
    #print('intf_range: ' + str(intf_range))
    #print('show interface command: ' + 'show interface ' + str(intf_range) + ' transceiver')
    show_int_cmd = 'show interface ' + str(intf_range) + ' transceiver'
    try :
        show_int_str = cli.cli(show_int_cmd)
    except :
        print('Error issuing ' + show_int_cmd + ' command...')
        pass
    
    show_int_transceiver_dict = {}
    
    intf_list = []
    show_int_list = show_int_str.splitlines()
    intf = ''
    if args.type_sfp_stats:
        
        #
        # '&' in column header indicates no column header
        # '&' in front of variable name indicates append to variable name
        #
        # Counter_list = [
        #                [number of tokens on line, [[Heading, [%variable_name, match keyword 1, match keyword 2, ..., match keyword n]]]],
        #                ...
        #                ]
        #
        # --transceiver-stats
        #
        header_line = 'Transceiver(SFP) Stats:'
        counter_list = [ 
                        [[3], [['Name', ['Name', 'is', '%intf_sfp_name']]]],
                        [[4], [['PID', ['Cisco', 'pid', 'is', '%intf_sfp_pid']]]],
                        [[13,14], [['Sync?', ['.', '.', '.', '.', '.', '%intf_sfp_sync', 'sync', 'exists,']], ['&', ['.', '.', '.', '.', '.', '.','&intf_sfp_sync', 'sync', 'exists,']], ['&', ['.', '.', '.', '.', '.', '.', '&intf_sfp_sync', 'sync', 'state,']]]],
                        [[4,5], [['Temp', ['Temperature', ':', '%intf_sfp_temp']], ['&', ['Temperature', ':', '.', '&intf_sfp_temp']], ['&', ['Temperature', ':', '.', '.', '&intf_sfp_temp']]]],
                        [[4,5], [['Voltage', ['Voltage', ':', '%intf_sfp_volt']], ['&', ['Voltage', ':', '.', '&intf_sfp_volt']], ['&', ['Voltage', ':', '.', '.', '&intf_sfp_volt']]]],
                        [[4,5], [['Current', ['Current', ':', '%intf_sfp_curr']], ['&', ['Current', ':', '.', '&intf_sfp_curr']], ['&', ['Current', ':', '.', '.', '&intf_sfp_curr']]]],
                        [[6,7], [['TxPower', ['Optical', 'Tx', 'Power', ':', '%intf_sfp_tx_power']], ['&', ['Optical', 'Tx', 'Power', ':', '.', '&intf_sfp_tx_power']], ['&', ['Optical', 'Tx', 'Power', ':', '.', '.', '&intf_sfp_tx_power']]]],
                        [[6,7], [['RxPower', ['Optical', 'Rx', 'Power', ':', '%intf_sfp_rx_power']], ['&', ['Optical', 'Rx', 'Power', ':', '.', '&intf_sfp_rx_power']], ['&', ['Optical', 'Rx', 'Power', ':', '.', '.', '&intf_sfp_rx_power']]]],
                        [[5], [['TxFault', ['Tx', 'Fault', 'count', ':', '%intf_sfp_tx_fault']]]],
                        
     
                       ]
    
    #
    # --transceiver-detail-stats
    # --sfp-detail-stats
    #         
    else:
        header_line = 'Transceiver(SFP) Detail Stats:'
        counter_list = [ 
                        [[3], [['Name', ['Name', 'is', '%intf_sfp_name']]]],
                        [[4], [['PID', ['Cisco', 'pid', 'is', '%intf_sfp_pid']]]],
                        [[4], [['Serial', ['Serial', 'number', 'is', '%intf_sfp_sn']]]],
                        [[13,14], [['Sync?', ['.', '.', '.', '.', '.', '%intf_sfp_sync', 'sync', 'exists,']], ['&', ['.', '.', '.', '.', '.', '.','&intf_sfp_sync', 'sync', 'exists,']], ['&', ['.', '.', '.', '.', '.', '.', '&intf_sfp_sync', 'sync', 'state,']]]],
                        [[6], [['Bit Rate', ['Nominal', 'bit', 'rate', 'is', '%intf_sfp_brate']], ['&', ['Nominal', 'bit', 'rate', 'is', '.', '&intf_sfp_brate']]]], 
                        [[4,5], [['Temp', ['Temperature', ':', '%intf_sfp_temp']], ['&', ['Temperature', ':', '.', '&intf_sfp_temp']], ['&', ['Temperature', ':', '.', '.', '&intf_sfp_temp']]]],
                        [[4,5], [['Voltage', ['Voltage', ':', '%intf_sfp_volt']], ['&', ['Voltage', ':', '.', '&intf_sfp_volt']], ['&', ['Voltage', ':', '.', '.', '&intf_sfp_volt']]]],
                        [[4,5], [['Current', ['Current', ':', '%intf_sfp_curr']], ['&', ['Current', ':', '.', '&intf_sfp_curr']], ['&', ['Current', ':', '.', '.', '&intf_sfp_curr']]]],
                        [[6,7], [['TxPower', ['Optical', 'Tx', 'Power', ':', '%intf_sfp_tx_power']], ['&', ['Optical', 'Tx', 'Power', ':', '.', '&intf_sfp_tx_power']], ['&', ['Optical', 'Tx', 'Power', ':', '.', '.', '&intf_sfp_tx_power']]]],
                        [[6,7], [['RxPower', ['Optical', 'Rx', 'Power', ':', '%intf_sfp_rx_power']], ['&', ['Optical', 'Rx', 'Power', ':', '.', '&intf_sfp_rx_power']], ['&', ['Optical', 'Rx', 'Power', ':', '.', '.', '&intf_sfp_rx_power']]]],
                        [[5], [['TxFault', ['Tx', 'Fault', 'count', ':', '%intf_sfp_tx_fault']]]],
                        
                       ]

         
magnatude_list = [[1000000000000, 'TB'], [1000000000, 'GB'], [1000000, 'MB'], [1000,'KB'], [0, 'B']]

#
# Build column list and initialize variables in default_intf_dict to 'NF'
#
default_intf_dict = {}
#
# Build column_name_list
# Initialize default variable name values to 'NF' in default_intf_dict
#
column_name_list = ['Intf']
for line_entry in counter_list:
    for counter_entry in line_entry[1]:
        column_name = counter_entry[0]
        if column_name != '&':
            column_name_list.append(column_name)
            for pattern_entry in counter_entry[1]:
                if pattern_entry[0:1] == '%':
                    var_name = pattern_entry[1:]
                    default_intf_dict[var_name] = 'NF'
                    break

#
# Go through show interface counters detailed output and build show_int_variables_dict dictionary for each interface
#
intf = ''
for line in show_int_list:
    #print('show interface detail line: ' + line)
    if ((line.startswith('fc') and len(line[2:].split('/')) == 2) or line.startswith('port-channel')):
        # mod_port = line[2:].split('/')
        #if len(mod_port) == 2 :
        #and mod_port[0].isdecimal() and mod_port[1].isdecimal():
        intf = line.strip().split()[0]
        #print('show interface detail intf: ' + intf)
        #
        # Check if filtering is needed
        #
        if port_type_filter:
            include_intf = False
            if intf in show_int_brief_dict:
                if args.filter_e_port: 
                    if show_int_brief_dict[intf]['oper_mode'][-1] == 'E':
                        include_intf = True
                elif args.filter_f_port:
                    if show_int_brief_dict[intf]['oper_mode'][-1] == 'F':
                        include_intf = True
                elif args.filter_np_port:
                    if show_int_brief_dict[intf]['oper_mode'][-1] == 'P':
                        include_intf = True
                elif args.filter_edge_port:
                    if show_int_brief_dict[intf]['logical_type'][-2:] == 'ge':
                        include_intf = True
                elif args.filter_core_port:
                    if show_int_brief_dict[intf]['logical_type'][-2:] == 're':
                        include_intf = True
            else:
                print('intf: ' + intf + ' not in show_int_brief_dict. Unable to filter.')
                include_intf = True
        else:
            include_intf = True
        if include_intf:
            intf_list.append(intf)
            show_int_variables_dict[intf] = dict(default_intf_dict)
        else:
            intf = ''
        #
        # Special case for when SFP not present
        #
        if line.endswith('sfp not present'):
            intf = ''
            continue
    #
    # Process non interface name line
    #
    elif intf != '':
        toks = line.split()
        for line_entry in counter_list:
            #
            # Check if length matches
            #
            #print('intf: ' + intf + ' len(toks): ' + str(len(toks)) + ' line_entry[1]: ' + str(line_entry[1]) + ' line: ' + line)
            #
            # Allow two counts of tokens for '-' Warning and '--' Alarm which may or may not be present
            #            
            if len(toks) == line_entry[0][0] or (len(line_entry[0]) == 2 and len(toks) == line_entry[0][1]):
                #
                # Go through each pattern entry
                #
                idx = 0

                for counter_entry in line_entry[1]:
                    idx = 0
                    #print('intf: ' + intf + ' counter_entry: ' + str(counter_entry))
                    pattern_match = False
                    for pattern_entry in counter_entry[1]:
                        #print('intf: ' + intf + ' toks[' + str(idx) + ']: "' + toks[idx] + '" pattern_entry: "' + str(pattern_entry) + '"')
                        #continue
                        if pattern_entry == '.':
                            pass
                        elif pattern_entry.startswith('%'):
                            var_name = pattern_entry[1:]
                            #print('Found var_name: ' + '%' + var_name)
                            if len(toks) > idx:
                                var_value = toks[idx]
                                #print('Found var_value: ' + var_value)
                            else:
                                var_value = ''
                            #pattern_match = False
                        #
                        # Variable names prepended with '&' means append to variable var_value if not 'NF'
                        #
                        elif pattern_entry.startswith('&'):
                            var_name = pattern_entry[1:]
                            #print('Found var_name: ' + '&' + var_name)
                            if len(toks) > idx:
                                var_value = show_int_variables_dict[intf][var_name]
                                if var_value != 'NF':
                                    var_value = var_value + toks[idx]
                                else:
                                    var_value = toks[idx]
                                #print('Found var_value: ' + var_value)
                            #pattern_match = False
                        elif toks[idx] == pattern_entry:
                            #print('Found matching pattern entry: ' + pattern_entry)
                            pattern_match = True
                        else:
                            pattern_match = False
                            #print('Found non matching pattern entry: ' + pattern_entry + ' toks[' + str(idx) + ']: ' + toks[idx])
                            break
                        idx += 1
                    #
                    # If matching update dictionary
                    #
                    if pattern_match:
                        show_int_variables_dict[intf][var_name] = var_value
                        #print('Setting show_int_variables_dict[' + intf + '][' + var_name + ']: ' + show_int_variables_dict[intf][var_name]) 
                        

if show_int_variables_dict :
    #
    # Build table
    #
    # For each counter, find pattern and set key name and values
    # Append each variable value to col_values
    # Once interface is completely processes add the row to the table
    #
    output_table = PrettyTable(column_name_list)
    
    #
    # Set columns to left justified
    #	
    for column_name in column_name_list:
        output_table.align[column_name] = 'l'
    #
    # Build each row in table
    #
    for intf in intf_list:
        col_values = [intf]
        intf_non_zero_count_found = False
        #
        # Build column values list
        #
        for line_entry in counter_list:
            for counter_entry in line_entry[1]:
                #column_name = counter_entry[0]
                #column_name_list.append(column_name)
                for pattern_entry in counter_entry[1]:
                    if pattern_entry[0:1] == '%':
                        var_name = pattern_entry[1:]
                        var_value = show_int_variables_dict[intf][var_name]
                        col_values.append(var_value)
                        #
                        # The check for if a value is an "error" is different for sfp stats
                        #
                        # Three checks
                        # 1 - var_value is not equal to 'NF'
                        # 2 - var_value contains a decimal point '.' and there is a trailing '-' or '+'
                        # 3 - var_value is a decimal integer that is not zero
                        if args.type_sfp_stats or args.type_sfp_detail_stats:
                            if var_value != 'NF' and ((var_value.find('.') != -1 and (var_value[-1:] == '-' or var_value[-1:] == '+')) or (var_value.isdigit() and var_value != '0')):
                                intf_non_zero_count_found = True
                        elif show_int_variables_dict[intf][var_name] != '0':
                            intf_non_zero_count_found = True
                        break
        if not args.filter_errorsonly or (args.filter_errorsonly and intf_non_zero_count_found):
            output_table.add_row(col_values)
    #
    # All done print out table
    print(header_line)
    output_table.title = 'show interface ' + str(intf_range) + ' counters detail'
    print output_table