import hashlib
import time

def sha256d(data: bytes) -> str:
    """Aplica doble SHA-256 al bloque de datos (igual que Bitcoin)."""
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

def mine_block(target_prefix="0000", max_nonce=2**32):
    """
    Simulación simplificada de minería.
    En vez de calcular un target real, buscamos un hash que empiece con `target_prefix`.
    """
    print("🔹 Iniciando simulación de minería...")
    print("Objetivo: encontrar un hash que empiece con", target_prefix)
    print("Cada intento cambia el 'nonce' y, si se agotan, también el 'timestamp'.\n")

    # --- Campos básicos de un encabezado de bloque ---
    version = "20000000"
    prev_block_hash = "0000000000000000000b4d0f1f95c8a0af6cbe33e0e6a6e3c1d5a65a4c9d1c22"
    merkle_root = "4a5e1e4baab89f3a32518a88e9d2f57f8c18fda97f6c6f24bdbf4c5e7a3c5b72"
    bits = "17000000"

    print("📦 Estructura del bloque:")
    print(f" - Versión: {version}")
    print(f" - Hash bloque previo: {prev_block_hash[:20]}...")  # abreviado
    print(f" - Merkle root: {merkle_root[:20]}...")
    print(f" - Bits (dificultad simplificada): {bits}\n")

    timestamp = int(time.time())
    attempts = 0
    start_time = time.time()  # medir tiempo de minería

    while True:
        for nonce in range(max_nonce):
            header = (
                version
                + prev_block_hash
                + merkle_root
                + format(timestamp, "08x")
                + bits
                + format(nonce, "08x")
            )

            h = sha256d(bytes.fromhex(header))
            attempts += 1

            if h.startswith(target_prefix):
                elapsed = time.time() - start_time
                print("✅ ¡Bloque minado!")
                print(f"Timestamp usado: {timestamp}")
                print(f"Nonce encontrado: {nonce}")
                print(f"Hash válido: {h}")
                print(f"Intentos totales: {attempts}")
                print(f"⏱️ Tiempo total: {elapsed:.2f} segundos")
                return h, attempts, elapsed

            # Para no imprimir cada intento, mostramos progreso cada 100k
            if attempts % 100000 == 0:
                print(f"Intentos: {attempts}, último hash: {h[:16]}...")

        timestamp += 1
        print(f"⏩ Nonces agotados, cambiando timestamp a {timestamp}")


if __name__ == "__main__":
    # Probar con distintas dificultades
    for zeros in [3, 4, 5]:
        print("\n" + "="*40)
        print(f"⛏️  Probando dificultad: {zeros} ceros iniciales")
        mine_block(target_prefix="0" * zeros)
