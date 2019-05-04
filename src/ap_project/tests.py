#! /usr/bin/env/ python3

from os.path import exists, join
from os import remove
from unittest import TestCase

from luigi import Parameter, build, LocalTarget

from ap_project.tasks import ClinicData


class ClinicDataTest(ClinicData):
    file = Parameter()

    def input(self):
        return LocalTarget(join('.',self.file))
    def requires(self):
        pass


class TestTask(TestCase):
    def test_data(self):
        # file = 'data_test_case.csv'
        root = join('.','tests')
        build([ClinicDataTest(file='QI_T1D_xtest_case.csv', ROOT=root)], local_scheduler=True)
        self.assertTrue(exists(join('.','tests', 'CLINIC_DATA_xtest_case.csv')))
        remove(join('.','tests', 'CLINIC_DATA_xtest_case.csv'))

