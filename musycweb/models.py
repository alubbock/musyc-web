from django.db import models
from django.conf import settings
from django_celery_results.models import TaskResult
import json
import io


class Dataset(models.Model):
    ORIENTATION_CHOICES = (
        (0, 'Emax<E0'),
        (1, 'Emax>E0')
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    name = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='_state/datasets', editable=False)
    orientation = models.PositiveSmallIntegerField(
        choices=ORIENTATION_CHOICES,
        default=1,
        editable=False
    )
    metric_name = models.TextField(default='Percent effect', editable=False)

    def __str__(self):
        return f'[{self.id}] {self.name} <{self.owner.email}>'


class DatasetTask(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    drug1 = models.TextField()
    drug2 = models.TextField()
    sample = models.TextField()
    task = models.ForeignKey(TaskResult, on_delete=models.CASCADE, null=True)
    task_uuid = models.TextField()
    FIELDS_CSV = (
        'dataset_name', 'task_uuid',
        'sample', 'expt', 'fit_method', 'drug1_name', 'drug2_name',
        'metric_name', 'init_rndm_seed', 'fit_beta', 'boundary_sampling',
        'max_conc_d1', 'max_conc_d2', 'min_conc_d1', 'min_conc_d2',
        'd1_init_pval', 'd2_init_pval', 'E0', 'E1', 'E2', 'E3', 'log_C1',
        'log_C2', 'log_h1', 'log_h2', 'E0_std', 'E1_std', 'E2_std', 'E3_std',
        'beta', 'beta_std', 'log_C1_std', 'log_C2_std', 'log_h1_std',
        'log_h2_std', 'log_alpha1', 'log_alpha1_std', 'log_alpha2',
        'log_alpha2_std', 'r1', 'r2', 'r1_std', 'r2_std', 'asym_ci', 'E0_ci',
        'E1_ci', 'E2_ci', 'E3_ci', 'log_C1_ci', 'log_C2_ci', 'log_h1_ci',
        'log_h2_ci', 'log_alpha1_ci', 'log_alpha2_ci', 'r1_ci', 'r2_ci',
        'beta_obs_ci', 'beta_ci', 'E1_obs_ci', 'E2_obs_ci', 'E3_obs_ci',
        'log_like_best', 'selected_fit_alg', 'model_level', 'converge_mc_nlls',
        'log_like_mc_nlls', 'converge_percnt_mc_nlls', 'h1', 'h2', 'C1', 'C2',
        'R2', 'E2_obs', 'E1_obs', 'E3_obs', 'E2_obs_std', 'E1_obs_std',
        'E3_obs_std', 'beta_obs', 'beta_obs_std', 'time_total', 'time_musyc',
        'num_parms_fit', 'drug1_units', 'drug2_units'
    )

    def __str__(self):
        return f'{self.task_uuid} [DS:{self.dataset_id}] ' \
               f'<{self.dataset.owner.email}>'

    def _task_set(self):
        if self.task:
            return True
        try:
            tr = TaskResult.objects.get(task_id=self.task_uuid)
            self.task = tr
            self.save()
            return True
        except TaskResult.DoesNotExist:
            return False

    @property
    def status(self):
        if not self._task_set():
            return 'QUEUED'

        return self.task.status

    @property
    def result_dict(self):
        if not self._task_set():
            return None

        if self.task.status != 'SUCCESS':
            return None

        d = json.loads(self.task.result)
        d['dataset_name'] = self.dataset.name
        d['task_uuid'] = self.task_uuid
        return d

    @property
    def result_csv_header(self):
        return ','.join(f'"{f}"' for f in self.FIELDS_CSV)

    @property
    def result_csv_line(self):
        d = self.result_dict
        return ','.join('"'+str(d[k]).replace('"', '\"')+'"'
                        for k in self.FIELDS_CSV)

    @property
    def result_csv(self):
        return f'{self.result_csv_header}\n{self.result_csv_line}'
