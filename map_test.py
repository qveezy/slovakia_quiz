import random
import geopandas as gpd
import matplotlib.pyplot as plt
import unicodedata as uni


gdf = gpd.read_file("data/GeoJSON/epsg_3395/districts_epsg_3395.geojson")


indices = random.sample(range(len(gdf)), len(gdf))
score = 0

plt.ion()
fig, ax = plt.subplots(figsize=(10, 10))

correct_indices = []
wrong_indices = []


def normalize_name(text: str) -> str:
    decomposed = uni.normalize("NFD", text)
    clean_chars = [char for char in decomposed if uni.category(char) != "Mn"]
    clean_str = "".join(clean_chars).lower()
    clean_str = clean_str.replace("-", " ")
    return " ".join(clean_str.split())


def screen():
    ax.clear()
    gdf.plot(ax=ax, color="lightgray", edgecolor="white", linewidth=0.5)


while indices:
    target = indices.pop()
    name = gdf.iloc[target]["NM3"]

    menu = input("Choose mode(1.Normal/2.4 variants): ")

    screen()

    if correct_indices:
        gdf.iloc[correct_indices].plot(
            ax=ax, color="seagreen", edgecolor="white", linewidth=0.8)
    if wrong_indices:
        gdf.iloc[wrong_indices].plot(
            ax=ax, color="indianred", edgecolor="white", linewidth=0.8)
    gdf.iloc[[target]].plot(ax=ax, color="gold",
                            edgecolor="black", linewidth=0.8)

    ax.set_title(f"Score: {score} | Left: {len(indices) + 1}")
    ax.set_axis_off()
    fig.canvas.draw()
    plt.pause(0.1)
    guess = input("Enter(q): ").strip()
    if guess.lower() == "q":
        print("Exiting")
        break
    if normalize_name(guess) == normalize_name(name):
        score += 1
        print("Correct")
        correct_indices.append(target)
    else:
        print(f"Wrong,It is: {name}")
        wrong_indices.append(target)
    if wrong_indices and not indices:
        wrong_names = gdf.iloc[wrong_indices]["NM3"].tolist()
        print("Mistakes in:", ", ".join(wrong_names))
        again = input("Do you want to try again?(y/n): ").lower().strip()
        if again == "y":
            indices[:] = wrong_indices
            wrong_indices.clear()
            random.shuffle(indices)
        elif again == "n":
            print("exiting")
            break


print("\n--- Game Over ---")
print(f"Correct: {len(correct_indices)} | Wrong: {len(wrong_indices)}")


plt.ioff()
plt.close(fig)


gdf = gpd.read_file("data/GeoJSON/epsg_3395/districts_epsg_3395.geojson")


indices = random.sample(range(len(gdf)), len(gdf))
score = 0

menu = input("Choose mode(1.Normal/2.4 variants): ").strip()
plt.ion()
fig, ax = plt.subplots(figsize=(10, 10))

correct_indices = []
wrong_indices = []
all_names = gdf["NM3"].tolist()


def normalize_name(text: str) -> str:


        decomposed = uni.normalize("NFD", text)
        clean_chars = [char for char in decomposed if uni.category(char) != "Mn"]
        clean_str = "".join(clean_chars).lower()
        clean_str = clean_str.replace("-", " ")
        return " ".join(clean_str.split())


def screen():


        ax.clear()
        gdf.plot(ax=ax, color="lightgray", edgecolor="white", linewidth=0.5)


while indices:
        target = indices.pop()
        name = gdf.iloc[target]["NM3"]

        screen()

        if menu == "2":
                wrong_pool = [n for n in all_names if n != name]
                variants = random.sample(wrong_pool, 3)
                variants.append(name)
                random.shuffle(variants)
                for i, option in enumerate(variants, start=1):
                         print(f"{i}. {option}")    
         if correct_indices:
                gdf.iloc[correct_indices].plot(ax=ax, color="seagreen", edgecolor="white", linewidth=0.8)
        if wrong_indices:
            	gdf.iloc[wrong_indices].plot(ax=ax, color="indianred", edgecolor="white", linewidth=0.8)
        gdf.iloc[[target]].plot(ax=ax, color="gold", edgecolor="black", linewidth=0.8)


        target_area = gdf.iloc[[target]].area.iloc[0]
        if target_area < 150_000_000:
                minx, miny, maxx, maxy = gdf.iloc[[target]].total_bounds
                pad = 15000
                ax.set_xlim(minx - pad, maxx + pad)
                ax.set_ylim(miny - pad, maxy + pad)
        ax.set_title(f"Score: {score} | Left: {len(indices) + 1}")
        ax.set_axis_off()
        fig.canvas.draw()
        plt.pause(0.1)
        while True:
                guess = input("Enter(q): ").strip()
                if guess.lower() == "hint":
                         print(f"Hint: starting with {name[0]}")
                         continue
                 break
         if guess.lower() == "q":
                 print("Exiting")
                 break
    
        if normalize_name(guess) == normalize_name(name):
                score += 1
                print("Correct")
                correct_indices.append(target)
        else:
                 print(f"Wrong,It is: {name}")
                wrong_indices.append(target)
        if wrong_indices and not indices:
                wrong_names = gdf.iloc[wrong_indices]["NM3"].tolist()
                print("Mistakes in:", ", ".join(wrong_names))
                again = input("Do you want to try again?(y/n): ").lower().strip()
                 if again == "y":
                        indices[:] = wrong_indices
                        wrong_indices.clear()
                        random.shuffle(indices)
                elif again == "n":
                         print("exiting")
                         break


print("\n--- Game Over ---")
print(f"Correct: {len(correct_indices)} | Wrong: {len(wrong_indices)}")


plt.ioff()
plt.close(fig)
