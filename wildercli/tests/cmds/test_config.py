from cmds.dev import _set_test_server
from wilder.testutil import ignore_user_project_files
from wildercli.main import cli


def test_show_when_not_set_says_so(runner):
    @ignore_user_project_files
    def run_test():
        res = runner.invoke(cli, ["config", "show"])
        assert "Not using config." in res.output

    run_test()


def test_show_shows(runner):
    @ignore_user_project_files
    def run_test():
        _set_test_server()
        res = runner.invoke(cli, ["config", "show"])
        assert "Host: http://127.0.0.1, Port: 5000. IsEnabled: True" in res.output

    run_test()
