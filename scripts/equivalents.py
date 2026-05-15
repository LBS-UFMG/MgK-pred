
# =========================================================
# Arquivos de entrada
# =========================================================
file1 = "8b0x_mg.cif"
file2 = "9q87_mg.cif"

# Distância máxima para considerar equivalência (Å)
cutoff = 2

# =========================================================
# Função para carregar átomos
# =========================================================
atoms1 = {}
atoms2 = {}

with open(file1) as f:
    linhas = f.readlines()
    for line in linhas:
        data = line.split()
        atoms1[data[1]] = data[10], data[11], data[12]

with open(file2) as f:
    linhas = f.readlines()
    for line in linhas:
        data = line.split()
        atoms2[data[1]] = data[10], data[11], data[12]


# =========================================================
# Matriz de distâncias
# =========================================================
def dist(x1,y1,z1,x2,y2,z2):
    return round(((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**(1/2),2)

eq1 = {}
eq2 = {}


for i in atoms1:
    x1,y1,z1 = float(atoms1[i][0]),float(atoms1[i][1]),float(atoms1[i][2])
    #print(x1,y1,z1)
    menor = 99999
    for j in atoms2:
        x2,y2,z2 = float(atoms2[j][0]),float(atoms2[j][1]),float(atoms2[j][2])

        d = dist(x1,y1,z1,x2,y2,z2)
        #print(i,j,d, end=',')

        if d < menor:
            menor = d

            if i not in eq1:
                eq1[i] = [j, d]
            else:
                eq1[i] = [j, d]

cont = 0
for x in eq1:
    if eq1[x][1] > 2:
        cont+=1
        print(x, eq1[x][0], eq1[x][1])

print(cont)





for i in atoms2:
    x2,y2,z2 = float(atoms2[i][0]),float(atoms2[i][1]),float(atoms2[i][2])
    #print(x1,y1,z1)
    menor = 99999
    for j in atoms1:
        x1,y1,z1 = float(atoms1[j][0]),float(atoms1[j][1]),float(atoms1[j][2])
        d = dist(x1,y1,z1,x2,y2,z2)
        #print(i,j,d, end=',')
        if d < menor:
            menor = d
            if i not in eq2:
                eq2[i] = [j, d]
            else:
                eq2[i] = [j, d]
cont = 0
for x in eq2:
    if eq2[x][1] > 2:
        cont+=1
        print(x, eq2[x][0], eq2[x][1])

print(cont)

exit()


# =========================================================
# Plotar matriz
# =========================================================
plt.figure(figsize=(10, 8))

im = plt.imshow(dist_matrix, aspect='auto')
plt.colorbar(im, label="Distância Euclidiana (Å)")

plt.xlabel("Átomos 9q87")
plt.ylabel("Átomos 8b0x")

plt.xticks(
    np.arange(len(atoms2)),
    [a["serial"] for a in atoms2],
    rotation=90,
    fontsize=6
)

plt.yticks(
    np.arange(len(atoms1)),
    [a["serial"] for a in atoms1],
    fontsize=6
)

plt.tight_layout()
plt.savefig("distance_matrix.png", dpi=300)
plt.show()

# =========================================================
# Determinar equivalências
# =========================================================
used_atoms2 = set()

equivalences = []
unmatched_1 = []
unmatched_2 = set(a["serial"] for a in atoms2)

for i, atom1 in enumerate(atoms1):

    row = dist_matrix[i]

    j = np.argmin(row)
    min_dist = row[j]

    atom2_serial = atoms2[j]["serial"]

    if min_dist <= cutoff and atom2_serial not in used_atoms2:
        equivalences.append(
            (atom1["serial"], atom2_serial, min_dist)
        )

        used_atoms2.add(atom2_serial)

        if atom2_serial in unmatched_2:
            unmatched_2.remove(atom2_serial)

    else:
        unmatched_1.append(atom1["serial"])

# =========================================================
# Criar CSV no formato solicitado
# =========================================================
csv_rows = []

csv_rows.append(["8b0x", "9q87"])

for eq in equivalences:
    csv_rows.append([eq[0], eq[1]])

for atom in unmatched_1:
    csv_rows.append([atom, ""])

for atom in unmatched_2:
    csv_rows.append(["", atom])

csv_df = pd.DataFrame(csv_rows)

csv_df.to_csv(
    "equivalent_atoms.csv",
    index=False,
    header=False
)

# =========================================================
# Mostrar equivalências
# =========================================================
print("\nEquivalências encontradas:\n")

for eq in equivalences:
    print(
        f"{eq[0]}  <-->  {eq[1]}   "
        f"(distância = {eq[2]:.3f} Å)"
    )

print("\nÁtomos sem equivalente em 9q87:")
for atom in unmatched_1:
    print(atom)

print("\nÁtomos sem equivalente em 8b0x:")
for atom in unmatched_2:
    print(atom)

print("\nArquivo CSV salvo como:")
print("equivalent_atoms.csv")

print("\nFigura salva como:")
print("distance_matrix.png")