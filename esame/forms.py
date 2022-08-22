from django import forms


class FormFiltro(forms.Form):
    SCELTE = (('bar', 'Barzellette'),
              ('bsq', 'Battute squallide'),
              ('sat', 'Satira'),
              ('bhu', 'Black humor'))

    tipo = forms.ChoiceField(required=True, choices=SCELTE, label='Selezionare il tipo di battute')
