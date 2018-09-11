import shutil
import click
from tabulate import tabulate as _tabulate


def format_search_results(search_results, keys=None):
    _, height = shutil.get_terminal_size()
    height -= 4  # Accounting for prompt

    ret = ''
    for idx, result in enumerate(search_results[:height]):
        fmt = '{:2}'
        fmt += '  '.join('{:.20}' for i in range(len(keys)))
        fmt += '\n'
        # TODO: improve
        ret += fmt.format(idx+1, *[result[key] for key in keys])
        # ret += '{:2}: {:40.40}\t{:20.20}\n'.format(idx+1, result.title, meta)

    return ret


def tabulate(ret_dict, keys_colors=None):
    table = []
    for idx, val in enumerate(ret_dict):
        row = [idx+1, ]
        for key in keys_colors:
            if isinstance(key, list):
                # NOTE: Test on python 3.3
                row.append(click.style(val[key[0]], **key[1]))
            else:
                row.append(val[key])
        table.append(row)

    headers = ['No', ]
    for key in keys_colors:
        if isinstance(key, list):
            headers.append(click.style(key[0], **key[1]))
        else:
            headers.append(key)

    table = _tabulate(table, headers, tablefmt='psql')
    table = '\n'.join(reversed(table.split('\n')))
    return table


def select_one(ret_dict, keys_colors=None, msg='Select one'):
    table = tabulate(ret_dict, keys_colors=keys_colors)
    print(table)
    value = click.prompt(msg, type=int)
    return ret_dict[value-1]