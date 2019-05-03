from os.path import join, exists
from os import mkdir
from glob import glob
import shutil

import luigi
import pandas as pd
from matplotlib import pyplot as plt

# retrieve new file
class ReadData(luigi.ExternalTask):
    ROOT = './data/'
    file = luigi.Parameter('file')

    def output(self):
        return luigi.LocalTarget(join(self.ROOT, self.file))

# output clinical data file
class ClinicData(luigi.Task):
    ROOT = './data/CLINIC/'
    file = luigi.Parameter('file')

    # create master file
    def requires(self):
        return ReadData(file = self.file)
    def output(self):
        d = self.file.rstrip('.csv').lstrip('QI_T1D_')
        return luigi.LocalTarget(join(self.ROOT,'CLINIC_DATA_'+ d +'.csv'))
    def run(self):
        month_data = pd.read_csv(join('./data/', self.file), parse_dates=['VISIT_DATE'])
        month_data = month_data.fillna('0')
        month_data['WEEK'] = month_data.VISIT_DATE.dt.week
        clinic_data_path = glob('./data/CLINIC/*')
        clinic_data = pd.read_csv(clinic_data_path[0])
        clinic_data = pd.concat([clinic_data, month_data], axis=0, sort=False, ignore_index=True)
        shutil.move(clinic_data_path[0], './data/old_data')
        clinic_data.to_csv(self.output().path)


# output provider data files
class ProviderFiles(luigi.Task):
    file = luigi.Parameter('file')
    task_complete = False

    def requires(self):
        return ClinicData(file = self.file)
    def output(self, name = ''):
        # output type of plt plots?
        return luigi.LocalTarget(join('.','data','PROVIDERS', name, name+'.csv'))
    def run(self):
        data = pd.read_csv(self.input().path)
        for i in data.LAST_VISIT_PROVIDER.unique():
            name = str(i).replace(', ', '_')
            if not exists(join('.','data','PROVIDERS',name)):
                mkdir(join('.','data','PROVIDERS',name))
            provider_data = data[data.LAST_VISIT_PROVIDER==i]
            provider_data.to_csv(self.output(name=name).path)
        self.task_complete = True
    def complete(self):
        return self.task_complete


class ProviderPlots(luigi.Task):
    file = luigi.Parameter('file')
    task_complete = False

    def requires(self):
        return ClinicData(file = self.file)
    def output(self, name=''):
        return luigi.LocalTarget(join('.','data','PROVIDER_RUN_CHARTS', name, name+'.png'))
    def run(self):
        all_data = pd.read_csv(self.input().path)
        for i in all_data.LAST_VISIT_PROVIDER.unique():
            provider_data = all_data[all_data.LAST_VISIT_PROVIDER == i]
            name = str(i).replace(', ', '_')
            data = provider_data.groupby(['WEEK']).mean()
            plt.subplot(221)
            plt.plot(data.index, data.HBA1C_WITHIN_3_MONTHS)
            plt.subplot(222)
            plt.plot(data.index, data.LIPID_WITHIN_YEAR)
            plt.subplot(223)
            plt.plot(data.index, data.MICROALBUMIN_WITHIN_YEAR)
            plt.subplot(224)
            plt.plot(data.index, data.BMP_CMP_WITHIN_YEAR)
            if not exists(join('.', 'data', 'PROVIDER_RUN_CHARTS', name)):
                mkdir(join('.', 'data', 'PROVIDER_RUN_CHARTS', name))
            plt.savefig(self.output(name=name).path)
            plt.close()
        self.task_complete = True
    def complete(self):
        return self.task_complete


# output clinic plots
class ClinicPlots(luigi.Task):
    file = luigi.Parameter('file')
    task_complete = False

    def requires(self):
        return ClinicData(file=self.file)
    def output(self, date = ''):
        out_path = join('.','data','CLINIC_RUN_CHARTS','CLINIC_RUN_CHARTS_'+ date+'.png')
        return luigi.LocalTarget(out_path)
    def run(self):
        data = pd.read_csv(self.input().path)
        data = data.groupby(['WEEK']).mean()
        #TODO label axis, set axis, set title,
        plt.subplot(221)
        plt.plot(data.index, data.HBA1C_WITHIN_3_MONTHS)
        plt.subplot(222)
        plt.plot(data.index, data.LIPID_WITHIN_YEAR)
        plt.subplot(223)
        plt.plot(data.index, data.MICROALBUMIN_WITHIN_YEAR)
        plt.subplot(224)
        plt.plot(data.index, data.BMP_CMP_WITHIN_YEAR)
        d = self.input().path.split('DATA_')[-1].rstrip('.csv')
        plt.savefig(self.output(date=d).path)
        plt.close()
        self.task_complete = True
    def complete(self):
        return self.task_complete
    
class RunReport(luigi.WrapperTask):
    file = luigi.Parameter('file')

    def requires(self):
        yield ProviderFiles(file=self.file)
        yield ProviderPlots(file=self.file)
        yield ClinicPlots(file=self.file)
