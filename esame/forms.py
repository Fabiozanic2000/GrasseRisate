from django import forms


class FormFiltro(forms.Form):
    SCELTE = (('Bar', 'Barzellette'),
              ('Bsq', 'Battute squallide'),
              ('Sat', 'Satira'),
              ('Bhu', 'Black humor'))

    tipo = forms.ChoiceField(required=True, choices=SCELTE, label='Selezionare il tipo di battute')
