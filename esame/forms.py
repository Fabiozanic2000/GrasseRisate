from django import forms


class FormFiltro(forms.Form):
    SCELTE = (('Barzelletta', 'Barzellette'),
              ('Battuta squallida', 'Battute squallide'),
              ('Satira', 'Satira'),
              ('Black humor', 'Black humor'),
              ('Notizia divertente', 'Notizie divertenti'),
              ('Gioco di parole', 'Giochi di parole'))

    tipo = forms.ChoiceField(required=True, choices=SCELTE, label='Tipo')


class FormRicercaProfilo(forms.Form):
    nick = forms.CharField(required=True, label="Username")
