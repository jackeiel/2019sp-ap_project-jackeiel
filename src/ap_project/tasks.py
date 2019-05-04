from os.path import join, exists
from os import mkdir
from glob import glob
import shutil

import luigi
import pandas as pd
import numpy as np
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
            weeks = provider_data.WEEK.max()
            data = provider_data.groupby(['WEEK']).mean()
            GOAL = 0.85

            f, [[ax1, ax2], [ax3, ax4]] = plt.subplots(nrows=2, ncols=2, sharey=True, sharex=True)
            plt.subplots_adjust(hspace=0.3)

            ax1.set_ylim([.3, 1])
            ax1.set_xticks(np.arange(1, weeks + 1, 2))

            ax1.axhline(GOAL, linestyle='--', color='green')
            ax1.axhline(data.HBA1C_WITHIN_3_MONTHS.mean(), linestyle='-.', color='orange')
            ax1.set_title('HBA1C within 3 Months')
            ax1.plot(data.index, data.HBA1C_WITHIN_3_MONTHS)

            ax2.axhline(GOAL, linestyle='--', color='green')
            ax2.axhline(data.LIPID_WITHIN_YEAR.mean(), linestyle='-.', color='orange')
            ax2.set_title('Lipids within year')
            ax2.plot(data.index, data.LIPID_WITHIN_YEAR)

            ax3.axhline(GOAL, linestyle='--', color='green')
            ax3.axhline(data.MICROALBUMIN_WITHIN_YEAR.mean(), linestyle='-.', color='orange')
            ax3.set_title('Microalbumin within year')
            ax3.set_xlabel('Week')
            ax3.plot(data.index, data.MICROALBUMIN_WITHIN_YEAR)

            ax4.axhline(GOAL, linestyle='--', color='green')
            ax4.axhline(data.BMP_CMP_WITHIN_YEAR.mean(), linestyle='-.', color='orange')
            ax4.set_title('Metabolic Panel within year')
            ax4.set_xlabel('Week')
            ax4.plot(data.index, data.BMP_CMP_WITHIN_YEAR)


            plt.suptitle('Percentage of Patients with Labs')


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
        read_data = pd.read_csv(self.input().path)
        weeks = read_data.WEEK.max()
        data = read_data.groupby(['WEEK']).mean()
        #TODO label axis, set axis, set title, add mean?, add goal
        GOAL = 0.85

        f, [[ax1, ax2], [ax3, ax4]] = plt.subplots(nrows=2, ncols=2, sharey=True, sharex=True)
        plt.subplots_adjust(hspace=0.3)

        ax1.set_ylim([.3, 1])
        ax1.set_xticks(np.arange(1, weeks + 1, 2))
        ax1.axhline(GOAL, linestyle='--', color='green')
        ax1.axhline(data.HBA1C_WITHIN_3_MONTHS.mean(), linestyle='-.', color='orange')
        ax1.set_title('HBA1C within 3 Months')
        ax1.plot(data.index, data.HBA1C_WITHIN_3_MONTHS)
        # annotation of plots
        ax1.annotate('Protocol A \nImplemented', xy=(3, data.HBA1C_WITHIN_3_MONTHS[data.index == 3]), \
                     xytext=(3, data.HBA1C_WITHIN_3_MONTHS[data.index == 3] + 0.2), \
                     arrowprops=dict(facecolor='black', shrink=0.2, width=3, \
                                     headwidth=7))

        # ax2.set_ylim([.3,1])
        ax2.axhline(GOAL, linestyle='--', color='green')
        ax2.axhline(data.LIPID_WITHIN_YEAR.mean(), linestyle='-.', color='orange')
        ax2.set_title('Lipids within year')
        ax2.plot(data.index, data.LIPID_WITHIN_YEAR)
        ax2.annotate('Protocol A \nImplemented', xy=(3, data.LIPID_WITHIN_YEAR[data.index == 3]), \
                     xytext=(3, data.LIPID_WITHIN_YEAR[data.index == 3] + 0.2), \
                     arrowprops=dict(facecolor='black', shrink=0.2, width=3, \
                                     headwidth=7))

        # ax3.set_ylim([.3,1])
        ax3.axhline(GOAL, linestyle='--', color='green')
        ax3.axhline(data.MICROALBUMIN_WITHIN_YEAR.mean(), linestyle='-.', color='orange')
        ax3.set_title('Microalbumin within year')
        ax3.set_xlabel('Week')
        ax3.plot(data.index, data.MICROALBUMIN_WITHIN_YEAR)
        ax3.annotate('Protocol A \nImplemented', xy=(3, data.MICROALBUMIN_WITHIN_YEAR[data.index == 3]), \
                     xytext=(3, data.MICROALBUMIN_WITHIN_YEAR[data.index == 3] + 0.2), \
                     arrowprops=dict(facecolor='black', shrink=0.2, width=3, \
                                     headwidth=7))

        # ax4.set_ylim([.3,1])
        ax4.axhline(GOAL, linestyle='--', color='green')
        ax4.axhline(data.BMP_CMP_WITHIN_YEAR.mean(), linestyle='-.', color='orange')
        ax4.set_title('Metabolic Panel within year')
        ax4.set_xlabel('Week')
        ax4.plot(data.index, data.BMP_CMP_WITHIN_YEAR)
        ax4.annotate('Protocol A \nImplemented', xy=(3, data.BMP_CMP_WITHIN_YEAR[data.index == 3]), \
                     xytext=(3, data.BMP_CMP_WITHIN_YEAR[data.index == 3] - 0.4), \
                     arrowprops=dict(facecolor='black', shrink=0.2, width=3, \
                                     headwidth=7))

        plt.suptitle('Percentage of Patients with Labs')

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
