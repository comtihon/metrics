import pkg_resources
import yaml
from colorama import Fore

from tester.system.test_factory import get_all_tests
from tester.test.test import Test


class TestsRunner:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        test_names = conf.get('--test', '').split(',')
        conf = TestsRunner.read_conf()
        classes = get_all_tests(test_names)
        self._tests = [c(conf) for c in classes]

    @property
    def tests(self) -> [Test]:
        return self._tests

    def run(self) -> bool:
        res = True
        for test in self.tests:
            if not test.run():
                res = False
                print(Fore.RED + test.name + ' Fail')
            else:
                print(Fore.GREEN + test.name + ' OK')
        return res

    @staticmethod
    def read_conf() -> dict:
        data = yaml.load(pkg_resources.resource_stream('tester.resources', 'services.yml'))
        return data
