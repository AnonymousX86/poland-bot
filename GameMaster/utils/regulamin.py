# -*- coding: utf-8 -*-
def _rules():
    return {
        1: 'Zakazane są treści niezgodne z prawem.',
        2: 'Zakazuje się mowy nienawiści oraz wyśmiewania innych użytkowników ze względu na ich poglądy, przekonania,'
           ' charakter itp. Pozwólmy każdemu być sobą.',
        3: 'Nie tolerujemy nadmiernego spamu.',
        4: 'Panuje zakaz wrzucania treści nazistowskich, faszystowskich, gore, porno, antyreligijnych,'
           ' oraz linków/filmów z zbyt głośną fonią bez ostrzeżenia. W tym także innych materiałów,'
           ' które zabrania zdrowy rozsądek i regulamin Discorda.',
        5: 'Reklamowanie się tylko za uprzednią zgodą moderacji.',
        6: 'Nie wykorzystuj błędów serwera do celów własnych.',
        7: 'Nie prowokuj do kłótni, ani jej nie ciągnij, dbaj o porządek na czacie, w tym także na kanałach głosowych.',
        8: 'Nie obrażaj nikogo ze względu na kolor skóry/narodowość/religię/płeć itp.',
        9: 'W przypadku wulgarnych i nieodpowiednich nicków/awatarów, możemy cię poprosić o jego zmianę,'
           ' odmowa może poskutkować wyrzuceniem.',
        10: 'Regulamin może ulec zmianie, jeżeli uważasz że zostałeś ukarany niesłusznie, zawsze możesz się odwołać.'
    }


def get_rule(point: int):
    try:
        r = f'**{point})** {_rules()[point]}'
    except KeyError:
        r = f'Brak punktu {point}.'
    return r
