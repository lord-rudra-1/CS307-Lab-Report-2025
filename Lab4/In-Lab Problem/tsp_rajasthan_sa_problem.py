import math
import random
import time
import matplotlib.pyplot as plt

# --------------------- Utility ---------------------
def haversine(a, b):
    """Calculate great-circle distance between two coordinates (lat, lon)."""
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    R = 6371.0
    hav = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(hav))

# --------------------- Rajasthan Dataset ---------------------
cities = {
    "Jaipur": (26.915, 75.820),
    "Udaipur": (24.57127, 73.691544),
    "Jodhpur": (26.263863, 73.008957),
    "Jaisalmer": (26.911661, 70.922928),
    "Bikaner": (28.01667, 73.31194),
    "Ajmer": (26.4521, 74.6387),
    "Pushkar": (26.487652, 74.555922),
    "Mount Abu": (24.5925, 72.7083),
    "Ranthambore": (26.0210, 76.3590),
    "Chittorgarh": (24.888744, 74.626923),
    "Bundi": (25.4386, 75.6374),
    "Alwar": (27.5625, 76.625),
    "Bharatpur": (27.2362221, 77.4910925),
    "Kota": (25.1921831, 75.8508374),
    "Neemrana": (27.98889, 76.38833),
    "Mandawa": (28.050017, 75.1487007),
    "Ranakpur": (25.1384, 73.4681),
    "Nathdwara": (24.9324, 73.825996),
    "Barmer": (25.753155, 71.418060),
    "Kumbhalgarh": (25.142459, 73.578606)
}

names = list(cities.keys())
n = len(names)

# Precompute distance matrix
dist = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i != j:
            dist[i][j] = haversine(cities[names[i]], cities[names[j]])

def tour_length(tour):
    return sum(dist[tour[i]][tour[(i+1)%len(tour)]] for i in range(len(tour)))

# --------------------- Simulated Annealing ---------------------
def simulated_annealing(alpha=0.99, iterations=50000, T0=4000.0, seed=42):
    random.seed(seed)
    curr = list(range(n))
    random.shuffle(curr)
    best = curr.copy()
    curr_len = tour_length(curr)
    best_len = curr_len
    T = T0

    for _ in range(iterations):
        i = random.randrange(0, n-1)
        j = random.randrange(i+1, n)
        neigh = curr.copy()
        neigh[i:j+1] = reversed(neigh[i:j+1])
        neigh_len = tour_length(neigh)
        delta = neigh_len - curr_len

        if delta < 0 or random.random() < math.exp(-delta / T):
            curr, curr_len = neigh, neigh_len
            if curr_len < best_len:
                best, best_len = curr.copy(), curr_len
        T *= alpha
        if T < 1e-8:
            break

    return best, best_len

# --------------------- Plotting Function ---------------------
def plot_tour(tour, best_len, alpha):
    x = [cities[names[i]][1] for i in tour] + [cities[names[tour[0]]][1]]
    y = [cities[names[i]][0] for i in tour] + [cities[names[tour[0]]][0]]

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, 'go-', linewidth=2)
    for i, idx in enumerate(tour):
        plt.text(x[i]+0.05, y[i]+0.05, names[idx], fontsize=8)
    plt.title(f"Optimal Tour — Total Distance: {best_len:.2f} km\nα = {alpha}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --------------------- Run Experiments ---------------------
if __name__ == "__main__":
    alphas = [0.99, 0.95, 0.90]
    results = []

    for a in alphas:
        print(f"\nRunning SA with α = {a} ...")
        best_tour, best_len = simulated_annealing(alpha=a)
        results.append((a, best_tour, best_len))
        plot_tour(best_tour, best_len, a)

    print("\n=== Summary of Cooling Rates ===")
    for a, _, best_len in results:
        print(f"α = {a} → Best Distance = {best_len:.2f} km")
