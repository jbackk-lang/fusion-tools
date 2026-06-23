import matplotlib.pyplot as plt

def plot_timdr(original, reduced):
    plt.figure(figsize=(12,5))
    plt.plot(original, label="Oryginał", alpha=0.5)
    plt.plot(reduced, label="TIMDR", linewidth=2)
    plt.legend()
    plt.title("TIMDR – redukcja informacji")
    plt.xlabel("próbka")
    plt.ylabel("wartość")
    plt.grid(True)
    plt.show()
