import hashlib
import time
import multiprocessing as mp
import os

def sha256d(data: bytes) -> str:
    """Aplica doble SHA-256 al bloque de datos (igual que Bitcoin)."""
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

def mine_worker(target_prefix, start_nonce, step, stop_event, result_queue):
    """
    Proceso de un minero: prueba nonces en saltos definidos por `step`.
    """
    version = "20000000"
    prev_block_hash = "0000000000000000000b4d0f1f95c8a0af6cbe33e0e6a6e3c1d5a65a4c9d1c22"
    merkle_root = "4a5e1e4baab89f3a32518a88e9d2f57f8c18fda97f6c6f24bdbf4c5e7a3c5b72"
    bits = "17000000"
    timestamp = int(time.time())

    attempts = 0
    nonce = start_nonce

    while not stop_event.is_set():
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
            # Guardar resultado y notificar al resto que se detengan
            result_queue.put({
                "miner": os.getpid(),
                "nonce": nonce,
                "hash": h,
                "attempts": attempts
            })
            stop_event.set()
            return

        nonce += step  # cada minero prueba nonces distintos

def mine_with_miners(target_prefix="000", num_miners=4):
    """
    Lanza varios procesos de mineros y devuelve el tiempo total y el ganador.
    """
    print(f"\n⛏️ Simulación con {num_miners} mineros...")
    print(f"Objetivo: hash que empiece con {target_prefix}\n")

    stop_event = mp.Event()
    result_queue = mp.Queue()
    processes = []
    start_time = time.time()

    # Crear procesos (cada uno con nonces diferentes)
    for i in range(num_miners):
        p = mp.Process(
            target=mine_worker,
            args=(target_prefix, i, num_miners, stop_event, result_queue)
        )
        processes.append(p)
        p.start()

    # Esperar al primero que encuentre solución
    winner = result_queue.get()
    elapsed = time.time() - start_time

    print("✅ ¡Bloque minado!")
    print(f"Minero ganador (PID): {winner['miner']}")
    print(f"Nonce encontrado: {winner['nonce']}")
    print(f"Hash válido: {winner['hash']}")
    print(f"Intentos de ese minero: {winner['attempts']}")
    print(f"⏱️ Tiempo total: {elapsed:.2f} segundos")

    # Detener todos los procesos
    stop_event.set()
    for p in processes:
        p.terminate()
    for p in processes:
        p.join()

    return elapsed

if __name__ == "__main__":
    miners_list = [1, 2, 4]  # distintas configuraciones
    results = {}

    for m in miners_list:
        elapsed = mine_with_miners(target_prefix="0000", num_miners=m)
        results[m] = elapsed

    print("\n📊 Comparación de tiempos:")
    for m, t in results.items():
        print(f" - {m} mineros: {t:.2f} segundos")
