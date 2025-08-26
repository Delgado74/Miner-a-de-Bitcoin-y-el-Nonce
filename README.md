# ⛏️ Minería de Bitcoin y el Nonce

## 🔑 ¿Qué es el nonce en minería?

En minería de **Bitcoin**, el **nonce** es un número arbitrario que los
mineros cambian repetidamente dentro del encabezado del bloque para
intentar encontrar una solución al **problema de prueba de trabajo
(PoW)**.

El objetivo es encontrar un **hash SHA-256 doble del encabezado del
bloque** que sea **menor** a un valor llamado **target** (objetivo de
dificultad).

------------------------------------------------------------------------

## 📦 Estructura del encabezado de bloque (80 bytes)

El encabezado contiene: 1. **Versión** (4 bytes) 2. **Hash del bloque
anterior** (32 bytes) 3. **Merkle root** (32 bytes, raíz de las
transacciones incluidas) 4. **Marca de tiempo (timestamp)** (4 bytes) 5.
**Bits (dificultad)** (4 bytes) 6. **Nonce** (4 bytes)

El **nonce es la última parte**: un número de 32 bits (0 a
4,294,967,295).

------------------------------------------------------------------------

## ⚙️ ¿Cómo funciona?

1.  El minero arma el encabezado con todos los datos del bloque.\

2.  Cambia el **nonce** (empieza en 0, luego 1, 2, 3, ...).\

3.  Calcula el hash SHA-256 dos veces:

    ``` python
    import hashlib

    def sha256d(data: bytes) -> str:
        return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()
    ```

4.  Si el hash es **menor que el target**, 🎉 ¡bloque válido
    encontrado!\

5.  Si no, incrementa el nonce y vuelve a probar.

------------------------------------------------------------------------

## 🤔 ¿Qué pasa si se acaban los nonces?

-   El nonce tiene solo **32 bits**, entonces puede agotarse rápido
    (unos 4 mil millones de intentos).\
-   Cuando eso pasa, el minero cambia **otro campo del encabezado** (por
    ejemplo, el **timestamp** o el orden de las transacciones en el
    Merkle root) para resetear el espacio de búsqueda.\
-   Así tienen efectivamente **muchos más nonces posibles**.

------------------------------------------------------------------------

## ⏱️ El timestamp

El **timestamp** lo elige el minero para su bloque.\
Debe cumplir con dos reglas: - Ser mayor al *MedianTimePast* (el
promedio de los últimos 11 bloques).\
- No estar más de 2 horas en el futuro respecto al tiempo real.

El minero puede modificarlo para ampliar aún más el espacio de búsqueda
de hashes.

Ejemplo en Python mostrando cómo cambiar el timestamp cambia totalmente
el hash:

``` python
import hashlib, time

def sha256d(data: bytes) -> str:
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

version = "20000000"
prev_block_hash = "0000000000000000000b4d0f1f95c8a0af6cbe33e0e6a6e3c1d5a65a4c9d1c22"
merkle_root = "4a5e1e4baab89f3a32518a88e9d2f57f8c18fda97f6c6f24bdbf4c5e7a3c5b72"
bits = "17000000"
nonce = "00000001"

for ts_offset in range(3):
    timestamp = format(int(time.time()) + ts_offset, "08x")
    header = version + prev_block_hash + merkle_root + timestamp + bits + nonce
    h = sha256d(bytes.fromhex(header))
    print(timestamp, h)
```

------------------------------------------------------------------------

## 📉 Relación con la dificultad

-   La red ajusta la **dificultad** cada 2016 bloques (\~2 semanas).\
-   Esto cambia el **target** → mientras más baja es la meta, más
    difícil es que un hash encaje.\
-   Más ceros al inicio del hash representan **mayor dificultad**.

Ejemplo actual (2025): los bloques válidos suelen tener entre **18 y 19
ceros hexadecimales al inicio** del hash.

------------------------------------------------------------------------

## 📊 Probabilidades simuladas

Ejemplo de la probabilidad de encontrar un hash válido según los ceros
requeridos:

``` python
import hashlib, random

def sha256d(data: bytes) -> str:
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

def simulate_probability(prefix_zeros: int, trials: int = 100000) -> float:
    target_prefix = "0" * prefix_zeros
    hits = 0
    for _ in range(trials):
        header = random.randbytes(80)
        h = sha256d(header)
        if h.startswith(target_prefix):
            hits += 1
    return hits / trials

for zeros in [1, 2, 3, 4, 5]:
    print(zeros, simulate_probability(zeros, trials=20000))
```

Resultados obtenidos en una simulación: - **1 cero inicial:** ≈ 6.4 %\
- **2 ceros iniciales:** ≈ 0.45 %\
- **3 ceros iniciales:** ≈ 0.065 %\
- **4 ceros iniciales:** prácticamente 0 en 20,000 intentos\
- **5 ceros iniciales:** prácticamente 0

Esto muestra cómo la probabilidad cae **exponencialmente** con cada cero
adicional.

------------------------------------------------------------------------

## 🔄 Diferencia con el nonce en firmas ECDSA

-   En **firmas ECDSA**, el nonce es un número secreto que no debe
    repetirse porque asegura la seguridad de la clave privada.\
-   En **minería**, el nonce no necesita ser secreto: es simplemente un
    contador que ayuda a los mineros a explorar el espacio de hashes.

------------------------------------------------------------------------

## 🔍 Resumen

-   El nonce en minería es un número que los mineros cambian para
    encontrar un hash válido.\
-   Cuando se agota, ajustan también el timestamp o el Merkle root.\
-   Más ceros al inicio del hash = mayor dificultad.\
-   Hoy en día se requieren ≈ 18--19 ceros al inicio, lo que obliga a
    los mineros a realizar **miles de millones de intentos por
    segundo**.
