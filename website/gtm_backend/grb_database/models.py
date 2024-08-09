from django.db import models

class GRB(models.Model):
    name = models.CharField('GRB', max_length=50, blank=False)
    position_ra_deg = models.CharField('RA (deg)', max_length=20, blank=False)
    position_dec_deg = models.CharField('DEC (def)', max_length=20, blank=False)
    time_trigger_utc = models.CharField('Trigger UTC', max_length=50, blank=False)
    time_t50_s = models.CharField('T50 (s)', max_length=20, blank=False)
    time_t90_s = models.CharField('T90 (s)', max_length=20, blank=False)
    note = models.TextField('Note', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
