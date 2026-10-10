import math


ENTRADAS = """"""

PI = math.pi
EPS = 1e-12
CAMBIO = {'a': 'b', 'b': 'a', 'c': 'c', 'A': 'B', 'B': 'A', 'C': 'C'}


def acos(x):
    if not math.isfinite(x) or abs(x) > 1 + EPS:
        raise ValueError('No existe un triangulo con esos datos.')
    return math.acos(max(-1, min(1, x)))


def convertir(texto):
    partes = texto.replace(',', '.').split()
    if not 1 <= len(partes) <= 3:
        raise ValueError('Escribe grados minutos segundos: ejemplo 121 42 30.')
    valores = [float(p) for p in partes]
    valores += [0.0] * (3 - len(valores))
    g, m, s = valores
    if not all(math.isfinite(v) for v in valores):
        raise ValueError('Introduce numeros finitos.')
    if g < 0 or not 0 <= m < 60 or not 0 <= s < 60:
        raise ValueError('Minutos y segundos deben estar entre 0 y menos de 60.')
    grados = g + m / 60 + s / 3600
    if not 0 < grados < 180:
        raise ValueError('Cada medida debe estar entre 0 y 180 grados, sin incluirlos.')
    return math.radians(grados)


def gms(x):
    total = round(math.degrees(x) * 360000)
    g, resto = divmod(total, 360000)
    m, s = divmod(resto, 6000)
    return f'{g}° {m:02d}\' {s / 100:05.2f}"'


def desde_ab(a, b):
    c = acos(math.cos(a) * math.cos(b))
    A = math.atan2(math.sin(a), math.cos(a) * math.sin(b))
    B = math.atan2(math.sin(b), math.cos(b) * math.sin(a))
    return dict(a=a, b=b, c=c, A=A, B=B, C=PI/2)


def desde_AB(A, B):
    a = acos(math.cos(A) / math.sin(B))
    b = acos(math.cos(B) / math.sin(A))
    c = acos(math.cos(A)*math.cos(B) / (math.sin(A)*math.sin(B)))
    return dict(a=a, b=b, c=c, A=A, B=B, C=PI/2)


def candidatos(d):
    par = set(d)
    # Intercambiar a con b y A con B permite reutilizar las formulas.
    if par in ({'a', 'c'}, {'c', 'B'}, {'b', 'B'}, {'a', 'B'}):
        nuevos = {CAMBIO[k]: v for k, v in d.items()}
        return [{CAMBIO[k]: v for k, v in r.items()}
                for r in candidatos(nuevos)]

    if par == {'a', 'b'}:
        return [desde_ab(d['a'], d['b'])]

    if par == {'A', 'B'}:
        return [desde_AB(d['A'], d['B'])]

    if par == {'b', 'c'}:
        b, c = d['b'], d['c']
        if abs(math.cos(b)) < EPS:
            if abs(math.cos(c)) < EPS:
                raise ValueError('Infinitas soluciones: necesitas un tercer dato.')
            raise ValueError('Con b = 90 grados, c debe ser 90 grados.')
        a = acos(math.cos(c) / math.cos(b))
        return [desde_ab(a, b)]

    if par == {'c', 'A'}:
        c, A = d['c'], d['A']
        if abs(math.cos(A)) < EPS:
            if abs(math.cos(c)) < EPS:
                raise ValueError('Infinitas soluciones: necesitas un tercer dato.')
            raise ValueError('Con A = 90 grados, c debe ser 90 grados.')
        # cot(B) = cos(c) tan(A), evaluado sin dividir por cos(A).
        B = math.atan2(math.cos(A), math.cos(c)*math.sin(A))
        if B < 0:
            B += PI
        return [desde_AB(A, B)]

    if par == {'b', 'A'}:
        b, A = d['b'], d['A']
        B = acos(math.sin(A) * math.cos(b))
        return [desde_AB(A, B)]

    if par == {'a', 'A'}:
        a, A = d['a'], d['A']
        if abs(math.cos(a)) < EPS:
            if abs(math.cos(A)) < EPS:
                raise ValueError('Infinitas soluciones: necesitas un tercer dato.')
            raise ValueError('El lado y su angulo opuesto deben coincidir en cuadrante.')
        seno_B = math.cos(A) / math.cos(a)
        if seno_B <= 0 or seno_B > 1 + EPS:
            raise ValueError('No existe un triangulo con esos datos.')
        B = math.asin(min(1, seno_B))
        return [desde_AB(A, B), desde_AB(A, PI-B)]

    raise ValueError('Elige dos letras distintas entre a, b, c, A y B.')


def valido(r, datos):
    if not all(EPS < v < PI-EPS for v in r.values()):
        return False
    a, b, c, A, B = (r[k] for k in ('a', 'b', 'c', 'A', 'B'))
    errores = [
        math.cos(c) - math.cos(a)*math.cos(b),
        math.cos(a) - math.cos(b)*math.cos(c) - math.sin(b)*math.sin(c)*math.cos(A),
        math.cos(b) - math.cos(a)*math.cos(c) - math.sin(a)*math.sin(c)*math.cos(B),
        math.sin(a) - math.sin(A)*math.sin(c),
        math.sin(b) - math.sin(B)*math.sin(c)
    ]
    return (max(map(abs, errores)) < 1e-8 and
            all(abs(r[k]-v) < 1e-8 for k, v in datos.items()))


def resolver(datos):
    soluciones = []
    for r in candidatos(datos):
        if valido(r, datos) and not any(
            max(abs(r[k]-otra[k]) for k in r) < 1e-8
            for otra in soluciones
        ):
            soluciones.append(r)
    if not soluciones:
        raise ValueError('No existe un triangulo no degenerado con esos datos.')
    return soluciones


def main():
    lineas = iter(ENTRADAS.strip().splitlines()) if ENTRADAS.strip() else None

    def pedir(mensaje):
        if lineas is None:
            return input(mensaje).strip()
        try:
            respuesta = next(lineas).strip()
        except StopIteration:
            raise EOFError('Faltan lineas en ENTRADAS.')
        print(mensaje + respuesta)
        return respuesta

    print('CALCULADORA DE TRIANGULOS ESFERICOS RECTANGULOS')
    print('C = 90 grados. Lados: a, b, c. Angulos: A, B.')
    print('Respeta las MAYUSCULAS y minusculas.')
    print('Formato: grados minutos segundos, sin simbolos.')
    print('Ejemplos equivalentes: 121 42 30  o  121 42.5 0\n')

    datos = {}
    while len(datos) < 2:
        nombre = pedir(f'Nombre del dato {len(datos)+1} (a, b, c, A o B): ')
        if nombre not in ('a', 'b', 'c', 'A', 'B') or nombre in datos:
            print('Elige una letra valida que no hayas ingresado.')
            continue
        try:
            datos[nombre] = convertir(pedir(f'Valor de {nombre} (grados minutos segundos): '))
        except ValueError as error:
            print(error)

    soluciones = resolver(datos)
    print(f'\nSOLUCIONES VALIDAS: {len(soluciones)}')
    for numero, r in enumerate(soluciones, 1):
        print(f'\n--- SOLUCION {numero} ---')
        print('VALORES QUE FALTABAN:')
        for k in ('a', 'b', 'c', 'A', 'B'):
            if k not in datos:
                print(f'  {k} = {gms(r[k])}')
        print('DATOS INGRESADOS:')
        for k, v in datos.items():
            print(f'  {k} = {gms(v)}')
        print('  C = 90° 00\' 00.00" (fijo)')
        print('Verificacion matematica: CORRECTA')
    print('\nPara otro calculo, vuelve a ejecutar el programa.')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, OSError):
        print('\nEl editor no permite leer datos o faltan entradas.')
        print('Introduce las cuatro lineas en el panel STDIN del editor,')
        print('o dentro de las triples comillas de ENTRADAS al principio.')
    except (ValueError, ZeroDivisionError) as error:
        print('\nNo se pudo resolver:', error)
