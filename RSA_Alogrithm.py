import time

def gcd(a, b):
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a

def eulerTotient(p, q):
    return (p - 1) * (q - 1)

def findCoprime(phi):
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            yield e

def modPow(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2
    return result

def modInverse(e, phi):
    for d in range(1, phi):
        if (d * e) % phi == 1:
            return d
    return -1  # Error: No modular inverse found

def measure_key_generation_time(p, q):
    start_time = time.time()
    
    n = p * q
    phi = eulerTotient(p, q)
    
    e_values = list(findCoprime(phi))
    
    # Choose a value of e
    chosen_e = e_values[0] if e_values else 0
    
    d = modInverse(chosen_e, phi)
    
    key_generation_time = time.time() - start_time
    return key_generation_time

if __name__ == "__main__":
    # Input prime numbers p and q
    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))
    
    # Measure key generation time
    key_generation_time = measure_key_generation_time(p, q)
    print(f"Key Generation Time: {key_generation_time} seconds")

    # Display n and phi
    n = p * q
    phi = eulerTotient(p, q)
    print(f"n = {n}")
    print(f"Euler's totient function (phi) = {phi}")

    # Display possible values of e
    print("Possible values of e:", end=" ")
    e_values = list(findCoprime(phi))
    print(e_values)

    # Input user choice for e
    while True:
        try:
            chosen_e = int(input("Choose a value of e from the above range: "))
            if chosen_e in e_values:
                break
            else:
                print("Wrong value of e chosen. Please choose from the displayed range.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Convert plaintext to ASCII values
    plaintext_str = input("Enter plaintext message (alphabetical format): ")
    plaintext = [ord(char) for char in plaintext_str]

    # Encryption - Measure time taken
    start_time = time.time()
    ciphertext = [modPow(char, chosen_e, n) for char in plaintext]
    encryption_time = time.time() - start_time

    # Calculate private key 'd'
    d = modInverse(chosen_e, phi)

    if d == -1:
        print("Error: No modular inverse found for the given e and phi.")
        exit(1)

    # Decryption - Measure time taken
    start_time = time.time()
    decrypted_message = [modPow(char, d, n) for char in ciphertext]
    decryption_time = time.time() - start_time

    # Display the result and time taken
    print(f"Public key (e, n): ({chosen_e}, {n})")
    print(f"Private key (d, n): ({d}, {n})")
    print("Ciphertext:", ciphertext)
    print("Decrypted Message:", "".join(chr(char) for char in decrypted_message))
    print(f"Encryption Time: {encryption_time} seconds")
    print(f"Decryption Time: {decryption_time} seconds")
