from wilder.cli.output_formats import OutputFormatter


def echo_formatted_list(_format, _list, header=None):
    formatter = OutputFormatter(_format, header=header)
    formatter.echo_formatted_list(_list)
