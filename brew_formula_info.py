#!/usr/bin/env python

import sys
import subprocess
import json
import argparse


def get_all_formula_info():
    proc = subprocess.Popen(['brew', 'list'], stdout=subprocess.PIPE)
    (raw_list, err) = proc.communicate()
    formula_list = raw_list.strip().split('\n')

    formula_list_info_cmd = ['brew', 'info', '--json=v1']
    formula_list_info_cmd.extend(formula_list)
    proc = subprocess.Popen(formula_list_info_cmd, stdout=subprocess.PIPE)
    (info, err) = proc.communicate()
    formula_info = json.loads(info)

    return formula_info


def get_all_non_kegonly_formula_info():
    formula_info = get_all_formula_info()

    non_kegonly_formula = []
    for info in formula_info:
        if not info['keg_only']:
            non_kegonly_formula.append(info)

    return non_kegonly_formula


def get_all_kegonly_formula_info():
    formula_info = get_all_formula_info()
    kegonly_formula = []

    for info in formula_info:
        if info['keg_only']:
            kegonly_formula.append(info)

    return kegonly_formula


def parse_argv(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--kegonly', help='List keg-only formula info',
                        metavar='KEGONY', dest='kegonly')
    parser.add_argument('-e', '--exclude-kegonly',
                        help='List non-keg-only formula info',
                        metavar='KEGONY', dest='kegonly')
    parser.add_argument('-a', '--all', help='List all formula info',
                        metavar='ALL', dest='all')

    return parser.parse_args(argv)


def main(argv):
    args = parse_argv(argv[1:])
    formulas = get_all_non_kegonly_formula_info()
    for formula in formulas:
        print formula['name']

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
