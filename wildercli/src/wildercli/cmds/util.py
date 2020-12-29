from wildercli.output_formats import OutputFormatter


def echo_formatted_list(_format, _list):
    formatter = OutputFormatter(_format)
    formatter.echo_formatted_list(_list)
